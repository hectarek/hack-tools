# Enhanced Load Tester with Randomized User-Agents and Variable Request Rates

An advanced Python script to perform load testing by simulating real user behavior, including:

- Randomized **User-Agent** headers to mimic different browsers/devices.
- Variable request rates to simulate natural user interaction with random delays.
- Detailed logging and reporting for analyzing application performance.
- Guidance on interpreting results in the context of real-world traffic.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage Instructions](#usage-instructions)
- [Updated Script Code](#updated-script-code)
- [Script Explanation](#script-explanation)
- [Understanding the Log/Report](#understanding-the-logreport)
- [Interpreting Results in Real-World Context](#interpreting-results-in-real-world-context)
- [Considerations](#considerations)
- [Disclaimer](#disclaimer)

---

## Overview

This enhanced load testing script allows you to:

- **Simulate real user behavior** by randomizing User-Agent headers and introducing random delays between requests.
- **Run the test for a specified duration** or **number of requests**.
- **Generate detailed logs** containing information about each request.
- **Produce a summary report** to help you understand how many users your application can handle concurrently.

## Prerequisites

- **Python 3.x** installed on your system.
- Install required libraries:
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

   Save the following script as `enhanced_load_tester.py`.

3. **Run the Script:**

   ```bash
   python enhanced_load_tester.py
   ```

4. **Input Parameters:**

   - **URL to Load Test:** Enter the full URL of the endpoint you want to test.
   - **Test Duration (seconds):** Specify how long you want the test to run (e.g., `60` for 1 minute).
   - **Number of Threads (Concurrent Users):** Specify how many threads to use for sending requests concurrently (e.g., `50` to simulate 50 concurrent users).
   - **Minimum Think Time (seconds):** Minimum delay between requests per thread (e.g., `1` second).
   - **Maximum Think Time (seconds):** Maximum delay between requests per thread (e.g., `5` seconds).

5. **View Results:**

   - **Log File:** A log file named `load_test_log.txt` will be generated containing detailed request information.
   - **Summary Report:** At the end of the test, a summary report will be displayed in the console.

## Updated Script Code

```python
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
```

## Script Explanation

### Randomizing User-Agents

- **Purpose:** Simulate requests coming from different browsers and devices.
- **Implementation:**
  - A list `USER_AGENTS` contains various User-Agent strings.
  - For each request, a User-Agent is randomly selected using `random.choice(USER_AGENTS)`.

### Variable Request Rates (Think Time)

- **Purpose:** Mimic natural user behavior by introducing random delays between requests.
- **Implementation:**
  - After each request, the thread sleeps for a random duration between `min_think_time` and `max_think_time` seconds.
  - Uses `random.uniform(min_think_time, max_think_time)` to generate the delay.

### Updated Input Parameters

- **Minimum Think Time (seconds):** The shortest time a simulated user waits before making the next request.
- **Maximum Think Time (seconds):** The longest time a simulated user waits before making the next request.

### Logging Enhancements

- **User-Agent in Logs:**
  - The User-Agent used for each request is included in the log entries.
- **Error Handling:**
  - On exceptions, the script logs the error and increments the failed requests count.
  - The thread sleeps for a random think time before retrying.

## Understanding the Log/Report

### Log File (`load_test_log.txt`)

- **Entries Include:**
  - Timestamp
  - Log level (INFO or ERROR)
  - Status Code
  - Response Time
  - User-Agent

- **Example Entry:**
  ```
  2023-10-10 12:00:01,123 - INFO - Status Code: 200, Response Time: 0.2345 seconds, User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
  ```

### Summary Report

- **Total Test Duration:** Actual duration of the test.
- **Total Requests Made:** Total number of HTTP requests sent across all threads.
- **Successful Requests:** Number of requests that received a `200 OK` response.
- **Failed Requests:** Number of requests that failed or received non-200 responses.
- **Average Response Time:** Mean response time for all requests.
- **Requests per Second:** Overall throughput during the test.

## Interpreting Results in Real-World Context

### Simulating Concurrent Users

- **Number of Threads:** Each thread represents a simulated user.
- **Think Time:** Represents the delay between actions a user might naturally take.

**Example:**

- **50 Threads:** Simulates 50 concurrent users interacting with the application.
- **Think Time between 1 and 5 seconds:** Users take between 1 to 5 seconds before performing the next action.

### Calculating Requests per Second (RPS)

- **Formula:**
  ```
  RPS = Total Requests Made / Total Test Duration
  ```

- **Interpreting RPS:**
  - Provides an average of how many requests your application can handle per second under the simulated load.
  - Helps in understanding peak loads and capacity planning.

### Estimating Users and Traffic

- **Concurrent Users:** Equal to the number of threads.
- **Total Users Over Time:** Can be estimated based on the total requests and average think time.

**Example Calculation:**

- **Test Duration:** 60 seconds
- **Concurrent Users:** 50
- **Total Requests Made:** 500
- **Average Think Time:** 3 seconds (average of min and max think times)

- **Requests per User:**
  ```
  Requests per User = Total Requests Made / Concurrent Users
                   = 500 / 50
                   = 10 requests per user over 60 seconds
  ```

- **Average Time Between Requests per User:**
  ```
  Average Time Between Requests = Test Duration / Requests per User
                               = 60 / 10
                               = 6 seconds
  ```

  (Note: This includes both the think time and the time taken to process the request.)

- **Interpreting Results:**
  - If your application maintains acceptable performance metrics (e.g., low response times, minimal errors) during the test, it suggests that it can handle 50 concurrent users generating a total of 500 requests over 60 seconds.
  - Scaling the number of threads can help you understand how your application performs under different user loads.

### Relating to Real-World Traffic

- **Peak Hours Simulation:**
  - By adjusting the number of threads and think times, you can simulate peak traffic conditions.
- **User Behavior Patterns:**
  - Varying think times can simulate different user interaction patterns (e.g., quick browsing vs. in-depth reading).

### Capacity Planning

- Use the results to estimate how many servers or resources are needed to support the expected number of users.
- **Example:**
  - If the application starts to degrade at 100 concurrent users, consider load balancing or scaling up resources to handle higher loads.

## Considerations

- **Accuracy of Simulation:**
  - While this script enhances realism, it remains a simulation. Real-world user behavior can be more complex.
- **Network Limitations:**
  - The client machine's network bandwidth may limit the load you can generate.
- **Server Impact:**
  - Ensure the server can handle the test load without adversely affecting production users.
- **Ethical Testing:**
  - Only perform load tests on applications and systems you have permission to test.

## Disclaimer

**Important:** Only perform load testing on systems you own or have explicit permission to test. Unauthorized load testing can be considered a denial-of-service attack and may have legal consequences.

---

**Note:** For more comprehensive load testing and advanced features like distributed testing, complex scenarios, and detailed analytics, consider using specialized tools such as **Apache JMeter**, **Locust**, or **Gatling**.

If you have any questions or need further assistance in customizing the script or interpreting the results, feel free to ask!