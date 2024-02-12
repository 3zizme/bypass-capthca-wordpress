
# Captcha Solver for Accessibility

## Overview
This Python script is designed to demonstrate the automation of captcha image fetching, text detection using Google Cloud's Vision API, and submitting login forms for accessibility testing purposes. It showcases how to interact with web forms, handle sessions, and utilize OCR technologies to improve web accessibility.

## Disclaimer
This tool is for educational and ethical testing purposes only. Always seek permission before testing websites you do not own. Unauthorized use of this script against websites without explicit permission is illegal and unethical.

## Features
- Fetch captcha images from WordPress websites.
- Solve captcha using Google Cloud Vision API.
- Automate login attempts for testing website accessibility.

## Prerequisites
- Python 3.x
- Google Cloud account and Vision API enabled
- `requests` library
- `google-cloud-vision` library

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Install required Python libraries:
   ```
   pip install -r requirements.txt
   ```

## Configuration
Before using the script, you must configure it with your Google Cloud Vision API credentials. Follow the [Google Cloud Vision documentation](https://cloud.google.com/vision/docs/setup) to set up your credentials and environment variable.

## Usage
1. Update the `usernames.txt` and `passwords.txt` files with the usernames and passwords you wish to test.
2. Run the script:
   ```
   python captcha_solver.py
   ```
3. Follow the prompts to enter the target URL.

## Contributing
Contributions to improve the script or extend its functionalities are welcome. Please ensure any contributions are ethical and legal.

## License
[MIT License](LICENSE)

## Acknowledgments
- Google Cloud Vision API for providing OCR capabilities.
