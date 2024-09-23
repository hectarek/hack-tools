import requests

def check_cookie_security(url):
    try:
        response = requests.get(url)
        cookies = response.cookies
        for cookie in cookies:
            print(f"Cookie Name: {cookie.name}")
            if not cookie.secure:
                print(" - Secure flag: Missing")
            else:
                print(" - Secure flag: Present")
            if not cookie.has_nonstandard_attr('HttpOnly'):
                print(" - HttpOnly flag: Missing")
            else:
                print(" - HttpOnly flag: Present")
    except Exception as e:
        print(f"Error checking cookies: {e}")

if __name__ == "__main__":
    url = input("Enter the URL to check cookies: ")
    check_cookie_security(url)