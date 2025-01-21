import concurrent.futures
import time
from pathlib import Path
import logging
from functools import partial
import json
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    'repo_owner': 'kubernetes',
    'repo_name': 'kubernetes',
    'data_dir': Path('data'),
    'max_retries': 3,
    'retry_delay': 5,
    'parallel_workers': 4,
    'cache_dir': Path('.cache'),
    'github_token': os.getenv('GITHUB_TOKEN')
}

# Ensure directories exist
CONFIG['data_dir'].mkdir(exist_ok=True)
CONFIG['cache_dir'].mkdir(exist_ok=True)

def get_rate_limit_status():
    """Check GitHub API rate limit status"""
    try:
        response = requests.get('https://api.github.com/rate_limit', headers={
            'Authorization': f'token {CONFIG["github_token"]}'
        })
        response.raise_for_status()
        return response.json()['resources']['core']
    except Exception as e:
        logger.warning(f"Could not check rate limit: {str(e)}")
        return None

def run_script_with_retries(script_name):
    """Run a script with retry logic and caching"""
    script_path = Path(f'scripts/{script_name}.py')
    cache_file = CONFIG['cache_dir'] / f'{script_name}.json'
    
    # Check cache first
    if cache_file.exists():
        with open(cache_file) as f:
            cached_data = json.load(f)
            if time.time() - cached_data['timestamp'] < 3600:  # 1 hour cache
                logger.info(f"Using cached data for {script_name}")
                return True
    
    for attempt in range(CONFIG['max_retries']):
        try:
            # Check rate limit before starting
            rate_limit = get_rate_limit_status()
            if rate_limit and rate_limit['remaining'] < 100:
                wait_time = (rate_limit['reset'] - time.time()) + 10
                logger.warning(f"Rate limit low ({rate_limit['remaining']} remaining). Waiting {wait_time:.1f}s")
                time.sleep(wait_time)
                rate_limit = get_rate_limit_status()
            
            start_time = time.time()
            logger.info(f"Running {script_name} (attempt {attempt + 1})")
            if rate_limit:
                logger.info(f"Rate limit: {rate_limit['remaining']}/{rate_limit['limit']} (resets in {rate_limit['reset'] - time.time():.0f}s)")
            
            # Create a copy of globals and add config
            exec_globals = globals().copy()
            exec_globals.update({
                'REPO_OWNER': CONFIG['repo_owner'],
                'REPO_NAME': CONFIG['repo_name'],
                'DATA_DIR': CONFIG['data_dir'],
                'GITHUB_TOKEN': CONFIG['github_token']
            })
            
            # Execute script with updated globals
            exec(compile(script_path.read_text(), script_path, 'exec'), exec_globals)
            
            # Update cache
            with open(cache_file, 'w') as f:
                json.dump({
                    'timestamp': time.time(),
                    'script': script_name
                }, f)
                
            logger.info(f"Completed {script_name} in {time.time() - start_time:.2f}s")
            return True
            
        except Exception as e:
            logger.error(f"Error in {script_name}: {str(e)}")
            if attempt < CONFIG['max_retries'] - 1:
                time.sleep(CONFIG['retry_delay'])
                continue
            logger.error(f"Failed {script_name} after {CONFIG['max_retries']} attempts")
            return False

def main():
    # List of scripts to run (order matters for dependencies)
    scripts = [
        'fetch_labels',
        'fetch_contributors',
        'fetch_branches',
        'fetch_issues',
        'fetch_comments',
        'fetch_pull_requests'
    ]
    
    # Check initial rate limit
    rate_limit = get_rate_limit_status()
    if rate_limit:
        logger.info(f"Initial rate limit: {rate_limit['remaining']}/{rate_limit['limit']}")
        
        # Adjust parallelism based on rate limit
        if rate_limit['remaining'] < 500:
            CONFIG['parallel_workers'] = min(2, CONFIG['parallel_workers'])
            logger.info(f"Reducing parallel workers to {CONFIG['parallel_workers']} due to low rate limit")
    
    # Run scripts with rate limit awareness
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONFIG['parallel_workers']) as executor:
        futures = {executor.submit(run_script_with_retries, script): script for script in scripts}
        
        for future in concurrent.futures.as_completed(futures):
            script = futures[future]
            try:
                future.result()
                
                # Check rate limit after each script completes
                rate_limit = get_rate_limit_status()
                if rate_limit and rate_limit['remaining'] < 100:
                    wait_time = (rate_limit['reset'] - time.time()) + 10
                    logger.warning(f"Rate limit low after {script}. Waiting {wait_time:.1f}s")
                    time.sleep(wait_time)
                    
            except Exception as e:
                logger.error(f"Unexpected error in {script}: {str(e)}")
    
    logger.info("Data pipeline completed")

if __name__ == "__main__":
    main()
