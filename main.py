import yaml
import requests
import time
import logging
from collections import defaultdict
from urllib.parse import urlparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

# Function to load configuration from the YAML file
def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            
            if not isinstance(config, list):
                raise ValueError("Config must be a list of endpoints")
                
            for endpoint in config:
                if not isinstance(endpoint, dict):
                    raise ValueError("Each endpoint must be a dictionary")
                if 'name' not in endpoint or not isinstance(endpoint['name'], str):
                    raise ValueError("Each endpoint must have a 'name' string")
                if 'url' not in endpoint or not isinstance(endpoint['url'], str):
                    raise ValueError("Each endpoint must have a 'url' string")
                if 'method' in endpoint and not isinstance(endpoint['method'], str):
                    raise ValueError("Method must be a string")
                if 'headers' in endpoint and not isinstance(endpoint['headers'], dict):
                    raise ValueError("Headers must be a dictionary")
                if 'body' in endpoint and not isinstance(endpoint['body'], str):
                    raise ValueError("Body must be a string")
                    
            return config
    except yaml.YAMLError as e:
        logging.error(f"Invalid YAML file: {str(e)}")
        raise

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = endpoint.get('body')
    
    try:
        start_time = time.time()
        response = requests.request(
            method,
            url,
            headers=headers,
            json=body,
            timeout=0.55  
        )
        response_time = (time.time() - start_time) * 1000 
        
        if 200 <= response.status_code < 300 and response_time <= 500:
            logging.info(f"Endpoint {url} is UP (Status: {response.status_code}, Time: {response_time:.2f}ms)")
            return "UP"
        else:
            logging.warning(f"Endpoint {url} is DOWN (Status: {response.status_code}, Time: {response_time:.2f}ms)")
            return "DOWN"
    except requests.RequestException as e:
        logging.error(f"Endpoint {url} failed with error: {str(e)}")
        return "DOWN"

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})

    while True:
        for endpoint in config:
            parsed_url = urlparse(endpoint["url"])
            domain = parsed_url.hostname
            result = check_health(endpoint)

            domain_stats[domain]["total"] += 1
            if result == "UP":
                domain_stats[domain]["up"] += 1

        # Log cumulative availability percentages
        for domain, stats in domain_stats.items():
            availability = round(100 * stats["up"] / stats["total"])
            print(f"{domain} has {availability}% availability percentage")

        print("---")
        time.sleep(15)

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        logging.error("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logging.info("\nMonitoring stopped by user.")
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        sys.exit(1)
