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