# TomplayBot

This is a WIP POC project that automates the creation of accounts with a free trial on https://tomplay.com

I do not advise the usage of this, this is merely a POC created for educational purposes.

This script uses a variety of evasion techniques, both behavioral and environmental changes to avoid bot detection.
Proxies are not implemented as in the assumed use case (script ran every two weeks once trial is done) proxies are not needed. You are welcome to submit a PR implementing them.

## Currently functioning
- Dynamic input system for credit card credentials
- Color-coded logger
- Account creation, no claiming of trial yet though.

## TODO
- Add payment method
- Claim trial
- Cancel trial(so no billing)
- Remove payment method

## Usage

```sh
git clone https://github.com/DatCodeMania/TomplayBot.git
cd TomplayBot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv .env.example .env
python3 main.py
```
