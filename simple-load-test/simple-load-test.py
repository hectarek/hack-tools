import requests
from threading import Thread
import time
import logging

# Configure logging
logging.basicConfig(filename='load_test_log.txt', filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def send_requests(url, duration, stats):
    end_time = time.time() + duration
    while time.time() < end_time:
        try:
            start_req_time = time.time()
            response = requests.get(url)
            end_req_time = time.time()
            response_time = end_req_time - start_req_time

            # Log request details
            logging.info(f"Status Code: {response.status_code}, Response Time: {response_time:.4f} seconds")

            # Update stats
            stats['total_requests'] += 1
            if response.status_code == 200:
                stats['successful_requests'] += 1
            else:
                stats['failed_requests'] += 1
            stats['response_times'].append(response_time)
        except Exception as e:
            logging.error(f"Request failed: {e}")
            stats['failed_requests'] += 1

def main():
    url = input("Enter the URL to load test: ")
    duration = int(input("Enter the test duration in seconds: "))
    num_threads = int(input("Enter the number of threads to use: "))

    # Shared statistics dictionary
    stats = {
        'total_requests': 0,
        'successful_requests': 0,
        'failed_requests': 0,
        'response_times': []
    }

    threads = []

    print(f"Starting load test for {duration} seconds with {num_threads} threads...")
    start_time = time.time()

    # Start threads
    for _ in range(num_threads):
        t = Thread(target=send_requests, args=(url, duration, stats))
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