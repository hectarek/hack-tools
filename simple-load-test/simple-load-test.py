import requests
from threading import Thread
import time
import logging
import random

# List of common User-Agent strings
USER_AGENTS = [
    # Add more User-Agent strings as needed
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)...',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F)...',
    'Mozilla/5.0 (Windows NT 10.0; WOW64)...',
    'Mozilla/5.0 (X11; Linux x86_64)...',
    'Mozilla/5.0 (iPad; CPU OS 13_6 like Mac OS X)...',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
]

# Configure logging
logging.basicConfig(filename='load_test_log.txt', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def send_requests(url, duration, min_think_time, max_think_time, stats):
    end_time = time.time() + duration
    session = requests.Session()
    while time.time() < end_time:
        try:
            # Randomize User-Agent
            headers = {
                'User-Agent': random.choice(USER_AGENTS)
            }
            # Record start time
            start_req_time = time.time()
            response = session.get(url, headers=headers)
            end_req_time = time.time()
            response_time = end_req_time - start_req_time

            # Log request details
            logging.info(f"Status Code: {response.status_code}, Response Time: {response_time:.4f} seconds, User-Agent: {headers['User-Agent']}")

            # Update stats
            stats['total_requests'] += 1
            if response.status_code == 200:
                stats['successful_requests'] += 1
            else:
                stats['failed_requests'] += 1
            stats['response_times'].append(response_time)

            # Random delay to simulate user think time
            think_time = random.uniform(min_think_time, max_think_time)
            time.sleep(think_time)
        except Exception as e:
            logging.error(f"Request failed: {e}")
            stats['failed_requests'] += 1
            # Optional: sleep before retrying
            time.sleep(random.uniform(min_think_time, max_think_time))

def main():
    url = input("Enter the URL to load test: ")
    duration = int(input("Enter the test duration in seconds: "))
    num_threads = int(input("Enter the number of threads (concurrent users) to use: "))
    min_think_time = float(input("Enter the minimum think time (seconds): "))
    max_think_time = float(input("Enter the maximum think time (seconds): "))

    # Shared statistics dictionary
    stats = {
        'total_requests': 0,
        'successful_requests': 0,
        'failed_requests': 0,
        'response_times': []
    }

    threads = []

    print(f"\nStarting load test for {duration} seconds with {num_threads} concurrent users...")
    start_time = time.time()

    # Start threads
    for _ in range(num_threads):
        t = Thread(target=send_requests, args=(url, duration, min_think_time, max_think_time, stats))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    end_time = time.time()
    total_test_time = end_time - start_time

    # Calculate average response time
    if stats['response_times']:
        average_response_time = sum(stats['response_times']) / len(stats['response_times'])
    else:
        average_response_time = 0

    # Display summary report
    print("\nLoad Test Summary Report")
    print("----------------------------")
    print(f"Total Test Duration: {total_test_time:.2f} seconds")
    print(f"Total Requests Made: {stats['total_requests']}")
    print(f"Successful Requests: {stats['successful_requests']}")
    print(f"Failed Requests: {stats['failed_requests']}")
    print(f"Average Response Time: {average_response_time:.4f} seconds")
    print(f"Requests per Second: {stats['total_requests'] / total_test_time:.2f}")

if __name__ == "__main__":
    main()