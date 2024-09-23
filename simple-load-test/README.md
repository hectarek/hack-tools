# Simple Load Tester with Logging and Time-Based Execution

An enhanced Python script to perform a load test by sending HTTP requests for a specified duration and generating a detailed log/report.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage Instructions](#usage-instructions)
- [Updated Script Code](#updated-script-code)
- [Script Explanation](#script-explanation)
- [Understanding the Log/Report](#understanding-the-logreport)
- [Performance Implications](#performance-implications)
- [Considerations](#considerations)
- [Disclaimer](#disclaimer)

---

## Overview

This updated load testing script allows you to:

- **Run the test for a specified amount of time** instead of a fixed number of requests.
- **Generate a log file** containing detailed information about each request.
- **Produce a summary report** at the end of the test.

This enhancement helps in understanding the application's performance over time and analyzing any issues that may occur during sustained load.

## Prerequisites

- **Python 3.x** installed on your system.
- The **requests** library installed:
  ```bash
  pip install requests
  ```
- Basic understanding of threading, logging, and web server performance metrics.

## Usage Instructions

1. **Install Dependencies:**

   ```bash
   pip install requests
   ```

2. **Save the Script:**

   Save the following script as `load_tester_with_logging.py`.

3. **Run the Script:**

   ```bash
   python load_tester_with_logging.py
   ```

4. **Input Parameters:**

   - **URL to Load Test:** Enter the full URL of the endpoint you want to test.
   - **Test Duration (seconds):** Specify how long you want the test to run (e.g., `60` for 1 minute).
   - **Number of Threads:** Specify how many threads to use for sending requests concurrently.

5. **View Results:**

   - **Log File:** A log file named `load_test_log.txt` will be generated containing detailed request information.
   - **Summary Report:** At the end of the test, a summary report will be displayed in the console.

## Updated Script Code

```python
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
```

## Script Explanation

- **Logging Configuration:**
  - Uses the `logging` module to write detailed logs to `load_test_log.txt`.
  - Logs include timestamp, log level, status code, and response time.

- **send_requests Function:**
  - Runs in each thread, sending requests until the specified duration elapses.
  - Records response times and updates shared statistics.

- **Shared Statistics Dictionary (`stats`):**
  - **total_requests:** Total number of requests made.
  - **successful_requests:** Number of requests with a `200` status code.
  - **failed_requests:** Number of failed requests (exceptions or non-200 status codes).
  - **response_times:** List of response times for calculating averages.

- **Main Function:**
  - Collects user input for URL, duration, and number of threads.
  - Starts the specified number of threads.
  - Waits for all threads to finish.
  - Calculates and displays a summary report.

## Understanding the Log/Report

### Log File (`load_test_log.txt`)

- **Entries Format:**
  ```
  YYYY-MM-DD HH:MM:SS,mmm - LEVEL - Message
  ```

- **Example Entries:**
  ```
  2023-10-10 12:00:01,123 - INFO - Status Code: 200, Response Time: 0.2345 seconds
  2023-10-10 12:00:01,456 - ERROR - Request failed: [Error Details]
  ```

### Summary Report

- **Total Test Duration:** Actual time the test ran.
- **Total Requests Made:** Total number of HTTP requests sent.
- **Successful Requests:** Number of requests that received a `200 OK` response.
- **Failed Requests:** Number of requests that failed or received non-200 responses.
- **Average Response Time:** Mean time taken for all requests.
- **Requests per Second:** Throughput of the application during the test.

### Interpreting Results

- **High Average Response Time:**
  - May indicate server overload or performance bottlenecks.
- **High Failed Requests Count:**
  - Could be due to application errors, server capacity limits, or network issues.
- **Low Requests per Second:**
  - May suggest the application cannot handle high concurrency.

## Performance Implications

- **Consistent Performance:**
  - If response times remain low and consistent, and error rates are minimal, the application is handling the load well.

- **Degrading Performance Over Time:**
  - If response times increase and error rates rise during the test, it may indicate memory leaks, resource exhaustion, or scalability issues.

- **Immediate Failures:**
  - High initial error rates could point to configuration issues or insufficient server resources.

## Considerations

- **Threading Limitations:**
  - Python's Global Interpreter Lock (GIL) can limit the effectiveness of threading in CPU-bound tasks but is generally acceptable for I/O-bound tasks like network requests.

- **System Resources:**
  - Running a large number of threads may consume significant system resources on the client machine running the test.

- **Network Bandwidth:**
  - Ensure the client machine has sufficient network bandwidth to generate the desired load without becoming a bottleneck.

- **Server Impact:**
  - Be cautious not to overwhelm the server, especially in production environments.

- **Test Environment:**
  - Ideally, perform load testing in a controlled environment that mirrors production.

## Disclaimer

**Important:** Only perform load testing on systems you own or have explicit permission to test. Unauthorized load testing can be considered a denial-of-service attack and may have legal consequences.

---

**Note:** This script provides a basic load testing mechanism with logging capabilities. For more comprehensive load testing and reporting features, consider using specialized tools like **Apache JMeter**, **Locust**, or **Gatling**.

If you need further customization or assistance in interpreting the results, feel free to ask!