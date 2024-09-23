# Simple Load Tester

A Python script to perform a basic load test by sending multiple HTTP requests to your web application.

---

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Usage Instructions](#usage-instructions)
- [Script Code](#script-code)
- [Understanding Potential Outcomes](#understanding-potential-outcomes)
- [Performance Implications](#performance-implications)
- [Different Configurations and Estimates](#different-configurations-and-estimates)
- [Disclaimer](#disclaimer)

---

## Overview

Load testing helps you understand how your application performs under heavy usage. This script simulates concurrent users by sending multiple HTTP requests using threading. By adjusting the number of threads and requests, you can estimate how your application handles different levels of traffic.

## Prerequisites

- **Python 3.x** installed on your system.
- The **requests** library installed (`pip install requests`).
- Basic understanding of threading in Python and web server performance metrics.

## Usage Instructions

1. **Install Dependencies:**

   ```bash
   pip install requests
   ```

2. **Save the Script:**

   Save the following script as `simple_load_tester.py`.

3. **Run the Script:**

   ```bash
   python simple_load_tester.py
   ```

4. **Input Parameters:**

   - **URL to Load Test:** Enter the full URL of the endpoint you want to test (e.g., `http://yourapp.com/api/resource`).
   - **Total Number of Requests:** Specify the total number of HTTP requests to send (e.g., `1000`).
   - **Number of Threads:** Specify how many threads to use for sending requests concurrently (e.g., `50`).

5. **View Results:**

   The script will display the status codes of the responses and the total time taken for the load test.

## Script Code

```python
import requests
from threading import Thread
import time

def send_requests(url, num_requests):
    for _ in range(num_requests):
        try:
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
        except Exception as e:
            print(f"Request failed: {e}")

def main():
    url = input("Enter the URL to load test: ")
    total_requests = int(input("Enter the total number of requests: "))
    num_threads = int(input("Enter the number of threads to use: "))

    requests_per_thread = total_requests // num_threads
    threads = []

    start_time = time.time()

    for _ in range(num_threads):
        t = Thread(target=send_requests, args=(url, requests_per_thread))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.time()
    print(f"Load test completed in {end_time - start_time} seconds.")

if __name__ == "__main__":
    main()
```

## Understanding Potential Outcomes

- **Successful Responses:**

  - **Output:** `Status Code: 200`
  - **Interpretation:** The server handled the request successfully.

- **Failed Requests:**

  - **Output:** `Request failed: [Error Details]`
  - **Interpretation:** The server failed to handle the request, possibly due to overload, network issues, or application errors.

- **Completion Time:**

  - **Output:** `Load test completed in [Seconds] seconds.`
  - **Interpretation:** Total time taken to complete the load test, useful for calculating requests per second.

## Performance Implications

- **Slow Response Times:**

  - **Risk:** Indicates the server may not handle high traffic efficiently.
  - **Action:** Optimize server performance, database queries, or consider scaling resources.

- **High Error Rates:**

  - **Risk:** A high number of failed requests may indicate bottlenecks or misconfigurations.
  - **Action:** Investigate server logs for errors and adjust application settings accordingly.

- **Efficient Handling:**

  - **Benefit:** The server handles concurrent requests well without significant delays or errors.
  - **Action:** Continue monitoring but maintain current configurations.

## Different Configurations and Estimates

### Understanding Load Parameters

- **Total Number of Requests:** Represents the total simulated user interactions.
- **Number of Threads:** Represents concurrent users sending requests at the same time.
- **Requests per Thread:** Calculated as `total_requests / num_threads`.

### Estimating Users and Network Traffic

While this script is a simplified load tester, you can estimate the number of users and network traffic based on your configurations:

- **Concurrent Users:** Approximated by the number of threads.
- **Total Users:** Could be considered as the total number of requests if each request represents a unique user interaction.
- **Network Traffic:** Calculated based on the size of the requests and responses.

### Example Configurations

#### Configuration 1: Light Load

- **Total Requests:** 1,000
- **Number of Threads:** 10
- **Requests per Thread:** 100

**Estimates:**

- Simulates 10 concurrent users.
- Each thread sends 100 requests sequentially.
- Useful for testing basic performance and ensuring the application handles moderate traffic.

#### Configuration 2: Moderate Load

- **Total Requests:** 10,000
- **Number of Threads:** 100
- **Requests per Thread:** 100

**Estimates:**

- Simulates 100 concurrent users.
- Represents a scenario where the application experiences increased traffic.
- Helps identify potential bottlenecks in application code or database queries.

#### Configuration 3: Heavy Load

- **Total Requests:** 100,000
- **Number of Threads:** 500
- **Requests per Thread:** 200

**Estimates:**

- Simulates 500 concurrent users.
- Stress tests the application to observe behavior under high load.
- Useful for assessing the need for load balancing or scaling infrastructure.

### Calculating Network Traffic

To estimate network traffic, you need to know the size of the HTTP requests and responses.

- **Request Size:** Usually minimal for GET requests unless query parameters are large.
- **Response Size:** Varies based on the data returned by the endpoint.

**Example Calculation:**

- **Assumed Average Response Size:** 50 KB
- **Total Responses:** 100,000
- **Total Network Traffic:** `100,000 responses * 50 KB = 5,000,000 KB ≈ 5 GB`

### Considerations

- **Server Capacity:** Ensure your server can handle the number of concurrent connections.
- **Network Bandwidth:** High network traffic may saturate your network interface.
- **Legal and Ethical:** Only perform load testing on systems you own or have permission to test.

## Disclaimer

**Important:** Only perform load testing on systems you own or have explicit permission to test. Unauthorized load testing can be considered a denial-of-service attack and may have legal consequences.

---

**Note:** This script provides a basic load testing mechanism. For more comprehensive load testing, consider using specialized tools like **Apache JMeter**, **Locust**, or **Gatling**, which offer advanced features like distributed testing, detailed reporting, and support for various protocols.