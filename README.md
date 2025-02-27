# capyclaim
capybaraGO! android game has a code claiming system, this automates it. Capybara Go codes can be found in the discord but i will eventually add them all here for a word list to iterate, collecting all codes in a sitting for a new account. the captcha isnt automated yet. I plan to add the feature of captcha automation soon, i just havent gotten around to it but i dont think it will be to hard.

- [x] Proof of concept
- [ ] Automate CAPTCHA
- [x] Wordlist to automate all codes at once
- [x] Refactor code

Example:
`python .\capyclaim.py --debug .\Tools\capycodes.txt`
Tested on windows
Should work on linux
Sample Results
```

╔═════════════════════════════════════════════════╗
║  🎁  🎁  🎁   GIFT CODE CLAIMER  🎁  🎁  🎁     ║
╚═════════════════════════════════════════════════╝

🐞  Debug mode enabled
🐞  Using user ID: 12345678
✅  Loaded 104 gift codes from .\Tools\capycodes.txt

🎁  Trying gift code 1/104: capyyushui
🤖  Generating captcha...
🐞  Response saved to captcha_response.json
🐞  Response status code: 200
🐞  JSON response: {
  "code": 0,
  "data": {
    "captchaId": "obLRO7anH1jVAxE5D1iX"
  }
}...
✅  Successfully extracted captchaId: obLRO7anH1jVAxE5D1iX
🔍  Fetching captcha image with ID: obLRO7anH1jVAxE5D1iX
🐞  Image request status code: 200
🐞  Image response content type: image/png
🖼️  Captcha image saved as captcha.png
🐞  Image format: PNG, Size: (240, 80), Mode: P
❓  Enter the captcha code shown in the image: 9110

────────── 🐞  REQUEST DATA 🐞  ──────────
{
    "userId": "123445678",
    "giftCode": "capyyushui",
    "captcha": "9110",
    "captchaId": "obLRO7anH1jVAxE5D1iX"
}
──────────────────────────────────────────
🔑  Submitting gift code claim...
🐞  Claim request status code: 200
⏳  Too many attempts. Please try again later.
🐞  Full response: {
  "code": 20407,
  "message": "giftcode self claimed"
}
⌛  Waiting 1.0 seconds before next attempt...
```

**Disclaimer**: *This content is for educational purposes only. Do not attempt to replicate or apply the information in real-world scenarios. Any actions taken based on this material are at your own risk. The author assumes no responsibility for any consequences that may arise.*
