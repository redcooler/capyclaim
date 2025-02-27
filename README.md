# capyclaim
capybaraGO! android game has a code claiming system, this automates it. Capybara Go codes can be found in the discord but i will eventually add them all here for a word list to iterate, collecting all codes in a sitting for a new account. the captcha isnt automated yet. I plan to add the feature of captcha automation soon, i just havent gotten around to it but i dont think it will be to hard.

- [x] Proof of concept
- [ ] Automate CAPTCHA
- [x] Wordlist to automate all codes at once
- [x] Refactor code

Example:
`python capyclaim.py --debug ~/path/to/wordlist`
Tested on windows
Should work on linux
Sample Results
```
[*] Generating captcha...
[+] Response saved to captcha_response.json
  Successfully extracted captchaId: Oyk7C7hu7QobQiDVWglJ
    Fetching captcha image with ID: Oyk7C7hu7QobQiDVWglJ
[+] Captcha image saved as captcha.png
        Image format: PNG, Size: (240, 80), Mode: P
[*] Captcha ID: Oyk7C7hu7QobQiDVWglJ
        Enter the captcha code shown in the image: 2848
        Enter your gift code: lucky999

────────── [+] SENDING DATA [+] ──────────
{
    "userId": "12345678",
    "giftCode": "lucky999",
    "captcha": "2846",
    "captchaId": "Oyk7C7hu7QobQiDVWglJ"
}
──────────────────────────────────────────

Submitting gift code claim...

Error: Too many attempts. Please try again later.
Full response: {
  "code": 20407,
  "message": "giftcode self claimed"
}
```

**Disclaimer**: *This content is for educational purposes only. Do not attempt to replicate or apply the information in real-world scenarios. Any actions taken based on this material are at your own risk. The author assumes no responsibility for any consequences that may arise.*
