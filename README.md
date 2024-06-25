# TomplayBot

This is a WIP project that automates the creation of accounts with a free trial on https://tomplay.com

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