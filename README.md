# TomplayBot

This is a proof of concept project that automates the creation of accounts with a free trial on https://tomplay.com

Although this program uses a variety of both behavorial and environmental evasion techniques to avoid bot detection, due to the, well, 'bot' nature of this project detection is still possible.

Due to a lack of credit cards for testing, this project has had it's development paused until further notice.

## Currently functioning
- Dynamic input system for credit card credentials
- Color-coded logger
- Account creation, input of credentials and claiming of trial.

## To do
I can currently not implement these as I have no credit cards available to me for testing. Pull requests are welcome :)
- Cancel trial(so no billing)
- Remove payment method

## Usage

```sh
git clone https://github.com/DatCodeMania/TomplayBot.git
cd TomplayBot
# I would suggest reading OPTIONS.md and altering the constants INSTRUMENT and LEVEL at the start of main.py to match your purposes
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.example .env
# (Optionally) alter the email domain used by the script in .env
python3 main.py
```

## Disclaimer

This project is intended for educational and proof-of-concept purposes only. The use of this project in violation of any applicable laws or terms of service is strictly prohibited.

By using this project, you agree that the author(s) and contributors are not responsible for any misuse or consequences that arise from using this project. Any actions taken using this project are solely your responsibility.

**Do not use this project if you are unsure about the legality or terms of use.**