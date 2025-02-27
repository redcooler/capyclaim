import json
import requests
import argparse
import sys
import time
from PIL import Image

# ANSI color codes
class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

# Emoji constants
class Emoji:
    INFO = "ℹ️ "
    SUCCESS = "✅ "
    ERROR = "❌ "
    WARNING = "⚠️ "
    GIFT = "🎁 "
    WAIT = "⏳ "
    LOCK = "🔒 "
    KEY = "🔑 "
    ROBOT = "🤖 "
    HOURGLASS = "⌛ "
    SPARKLES = "✨ "
    MAGNIFY = "🔍 "
    IMAGE = "🖼️ "
    CHECK = "✓ "
    STAR = "⭐ "
    QUESTION = "❓ "
    DEBUG = "🐞 "

# Set to make it easy for one user
DEFAULTUSER = True
# Replace with your user ID
DEFAULTUSER_id = "12345678"

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Gift code claiming script with wordlist support')
    parser.add_argument('wordlist', type=str, help='Path to wordlist file containing gift codes')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between attempts in seconds (default: 1.0)')
    parser.add_argument('--user-id', type=str, help='Override the default user ID')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for detailed output')
    args = parser.parse_args()

    # Set debug mode based on parameter
    DEBUG = args.debug
    
    # Override default user ID if provided
    user_id = args.user_id if args.user_id else DEFAULTUSER_id

    # Print banner
    print_banner()

    # Base URL for the API
    base_url = "https://mail.advrpg.com"
    origin = "https://gift.capybarago.io"
    referer = "https://gift.capybarago.io/"

    # Headers for API requests
    headers = {
        "authority": "mail.advrpg.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "origin": origin,
        "referer": referer,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    if DEBUG:
        print(f"{Colors.CYAN}{Emoji.DEBUG} Debug mode enabled{Colors.RESET}")
        print(f"{Colors.CYAN}{Emoji.DEBUG} Using user ID: {user_id}{Colors.RESET}")

    # Try to open and read the wordlist file
    try:
        with open(args.wordlist, 'r') as file:
            gift_codes = [line.strip() for line in file if line.strip()]
        print(f"{Colors.GREEN}{Emoji.SUCCESS} Loaded {len(gift_codes)} gift codes from {args.wordlist}{Colors.RESET}")
        if DEBUG and len(gift_codes) < 10:
            print(f"{Colors.CYAN}{Emoji.DEBUG} Gift codes: {gift_codes}{Colors.RESET}")
    except FileNotFoundError:
        print(f"{Colors.RED}{Emoji.ERROR} Error: Wordlist file '{args.wordlist}' not found.{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}{Emoji.ERROR} Error reading wordlist file: {e}{Colors.RESET}")
        sys.exit(1)

    # Process each code in the wordlist
    success_count = 0
    for i, gift_code in enumerate(gift_codes):
        print(f"\n{Colors.BLUE}{Emoji.GIFT} Trying gift code {i+1}/{len(gift_codes)}: {gift_code}{Colors.RESET}")
        
        # Generate captcha for each attempt
        captcha_id = generate_captcha(base_url, headers, DEBUG)
        if not captcha_id:
            print(f"{Colors.RED}{Emoji.ERROR} Failed to generate captcha. Skipping this code.{Colors.RESET}")
            continue
            
        # Get captcha image
        if not get_captcha_image(base_url, origin, referer, captcha_id, DEBUG):
            print(f"{Colors.RED}{Emoji.ERROR} Failed to get captcha image. Skipping this code.{Colors.RESET}")
            continue
            
        # Prompt for captcha solution
        captcha_code = input(f"{Colors.YELLOW}{Emoji.QUESTION} Enter the captcha code shown in the image: {Colors.RESET}")
        
        # Claim the gift
        result = claim_gift(base_url, headers, user_id, captcha_id, captcha_code, gift_code, DEBUG)
        
        # Check if successful
        if result and result.get('code') == 0:
            success_count += 1
            print(f"{Colors.GREEN}{Emoji.SPARKLES} Successfully claimed code: {gift_code}{Colors.RESET}")
        
        # Delay between attempts to avoid rate limiting
        if i < len(gift_codes) - 1:
            print(f"{Colors.YELLOW}{Emoji.HOURGLASS} Waiting {args.delay} seconds before next attempt...{Colors.RESET}")
            time.sleep(args.delay)
    
    print(f"\n{Colors.GREEN}{Emoji.STAR} Completed processing {len(gift_codes)} gift codes. Successful claims: {success_count}{Colors.RESET}")

def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}╔═════════════════════════════════════════════════╗
║  {Emoji.GIFT} {Emoji.GIFT} {Emoji.GIFT}  GIFT CODE CLAIMER  {Emoji.GIFT} {Emoji.GIFT} {Emoji.GIFT}\t  ║
╚═════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def generate_captcha(base_url, headers, DEBUG):
    print(f"{Colors.BLUE}{Emoji.ROBOT} Generating captcha...{Colors.RESET}")
    response = requests.post(f"{base_url}/api/v1/captcha/generate", headers=headers)
    
    # Save the response to a file if in debug mode
    if DEBUG:
        with open("captcha_response.json", "w") as f:
            f.write(response.text)
        print(f"{Colors.CYAN}{Emoji.DEBUG} Response saved to captcha_response.json{Colors.RESET}")
        print(f"{Colors.CYAN}{Emoji.DEBUG} Response status code: {response.status_code}{Colors.RESET}")

    # Try to extract captchaId
    try:
        response_json = response.json()
        if DEBUG:
            print(f"{Colors.CYAN}{Emoji.DEBUG} JSON response: {json.dumps(response_json, indent=2)[:200]}...{Colors.RESET}")
        captcha_id = response_json.get('data', {}).get('captchaId')
        if captcha_id:
            print(f"{Colors.GREEN}{Emoji.SUCCESS} Successfully extracted captchaId: {captcha_id}{Colors.RESET}")
            return captcha_id
    except json.JSONDecodeError:
        print(f"{Colors.YELLOW}{Emoji.WARNING} Response is not valid JSON. Trying alternative extraction method...{Colors.RESET}")

    # Fallback method using string search if JSON parsing failed
    import re
    match = re.search(r'"captchaId":"([^"]*)"', response.text)
    if match:
        captcha_id = match.group(1)
        print(f"{Colors.GREEN}{Emoji.SUCCESS} Extracted captchaId using regex: {captcha_id}{Colors.RESET}")
        return captcha_id
    else:
        print(f"{Colors.RED}{Emoji.ERROR} Failed to extract captchaId.{Colors.RESET}")
        if DEBUG:
            print(f"{Colors.CYAN}{Emoji.DEBUG} First 200 characters of response:{Colors.RESET}")
            print(f"{Colors.CYAN}{response.text[:200]}{Colors.RESET}")
        return None

def get_captcha_image(base_url, origin, referer, captcha_id, DEBUG):
    print(f"{Colors.BLUE}{Emoji.MAGNIFY} Fetching captcha image with ID: {captcha_id}{Colors.RESET}")
    img_headers = {
        "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        "origin": origin,
        "referer": referer,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }
    img_response = requests.get(f"{base_url}/api/v1/captcha/image/{captcha_id}", headers=img_headers)

    if DEBUG:
        print(f"{Colors.CYAN}{Emoji.DEBUG} Image request status code: {img_response.status_code}{Colors.RESET}")
        print(f"{Colors.CYAN}{Emoji.DEBUG} Image response content type: {img_response.headers.get('Content-Type')}{Colors.RESET}")

    # Check if image was successfully downloaded
    if img_response.status_code == 200:
        with open("captcha.png", "wb") as f:
            f.write(img_response.content)
        print(f"{Colors.GREEN}{Emoji.IMAGE} Captcha image saved as captcha.png{Colors.RESET}")

        # Try to open the image to verify it's valid
        try:
            image = Image.open("captcha.png")
            if DEBUG:
                print(f"{Colors.CYAN}{Emoji.DEBUG} Image format: {image.format}, Size: {image.size}, Mode: {image.mode}{Colors.RESET}")
            image.show()  # This will open the image in the default image viewer
            return True
        except Exception as e:
            print(f"{Colors.YELLOW}{Emoji.WARNING} Could not open the image: {e}{Colors.RESET}")
            return False
    else:
        print(f"{Colors.RED}{Emoji.ERROR} Failed to download captcha image. Status code: {img_response.status_code}{Colors.RESET}")
        if DEBUG:
            print(f"{Colors.CYAN}{Emoji.DEBUG} Response: {img_response.text}{Colors.RESET}")
        return False

def claim_gift(base_url, headers, user_id, captcha_id, captcha_code, gift_code, DEBUG):
    # Update headers for the claim request
    claim_headers = headers.copy()
    claim_headers["content-type"] = "application/json"

    # Prepare data for claim
    data = {
        "userId": user_id,
        "giftCode": gift_code,
        "captcha": captcha_code,
        "captchaId": captcha_id
    }
 
    # Show request data in debug mode
    if DEBUG:
        print(f"\n{Colors.CYAN}{'─'*10} {Emoji.DEBUG} REQUEST DATA {Emoji.DEBUG} {'─'*10}{Colors.RESET}")
        print(f"{Colors.CYAN}{json.dumps(data, indent=4)}{Colors.RESET}")
        print(f"{Colors.CYAN}{'─'*42}{Colors.RESET}")

    # Make the claim request
    print(f"{Colors.BLUE}{Emoji.KEY} Submitting gift code claim...{Colors.RESET}")
    response = requests.post(f"{base_url}/api/v1/giftcode/claim", headers=claim_headers, json=data)
    
    if DEBUG:
        print(f"{Colors.CYAN}{Emoji.DEBUG} Claim request status code: {response.status_code}{Colors.RESET}")

    # Process response
    try:
        result = response.json()
        code = result.get('code')

        # Map response codes to messages
        response_messages = {
            0: f"{Colors.GREEN}{Emoji.SPARKLES} Success! Your reward has been claimed.{Colors.RESET}",
            20001: f"{Colors.RED}{Emoji.ERROR} Invalid gift code format.{Colors.RESET}",
            20002: f"{Colors.RED}{Emoji.ERROR} Captcha verification failed.{Colors.RESET}",
            20003: f"{Colors.YELLOW}{Emoji.WARNING} Gift code has already been claimed.{Colors.RESET}",
            20401: f"{Colors.RED}{Emoji.ERROR} Gift code not found.{Colors.RESET}",
            20402: f"{Colors.RED}{Emoji.ERROR} User not found.{Colors.RESET}",
            20403: f"{Colors.RED}{Emoji.ERROR} Invalid input.{Colors.RESET}",
            20404: f"{Colors.YELLOW}{Emoji.WARNING} Gift code has expired.{Colors.RESET}",
            20409: f"{Colors.YELLOW}{Emoji.WARNING} You've already claimed this type of gift code.{Colors.RESET}",
            20407: f"{Colors.YELLOW}{Emoji.WAIT} Too many attempts. Please try again later.{Colors.RESET}",
            20410: f"{Colors.YELLOW}{Emoji.LOCK} You are not eligible for this gift code.{Colors.RESET}",
            30001: f"{Colors.RED}{Emoji.ERROR} System error. Please try again later.{Colors.RESET}"
        }

        message = response_messages.get(code, f"{Colors.RED}{Emoji.ERROR} Unknown error ({code}){Colors.RESET}")
        print(message)
        
        if DEBUG:
            print(f"{Colors.CYAN}{Emoji.DEBUG} Full response: {json.dumps(result, indent=2)}{Colors.RESET}")
            
        return result

    except json.JSONDecodeError:
        print(f"{Colors.RED}{Emoji.ERROR} Could not decode response as JSON.{Colors.RESET}")
        if DEBUG:
            print(f"{Colors.CYAN}{Emoji.DEBUG} Raw response: {response.text}{Colors.RESET}")
        return None

if __name__ == "__main__":
    main()
