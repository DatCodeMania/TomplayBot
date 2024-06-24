import re
import pyperclip
import time
import threading
from colorama import Fore

# Shared variables and event
clipboard_content = None
event = threading.Event()


def monitor_clipboard(pattern):
    global clipboard_content
    while not event.is_set():
        current_clipboard = pyperclip.paste()
        if re.match(pattern, current_clipboard):
            clipboard_content = current_clipboard
            event.set()
        time.sleep(0.5)  # wait for performance purposes


def get_input(prompt, pattern):
    global clipboard_content
    event.clear()
    clipboard_content = None
    threading.Thread(target=monitor_clipboard, args=(pattern,), daemon=True).start()
    print(prompt)
    while not event.is_set():
        user_input = input()
        if user_input:
            event.set()
            return user_input
        time.sleep(0.1)  # wait for performance purposes
    return clipboard_content


def get_card_number():
    pattern = r'^\d{4} ?\d{4} ?\d{4} ?\d{4}$'  # regex for 16 digit credit card number, optional spaces
    prompt = f"{Fore.MAGENTA}Please enter the credit card number or copy it to the clipboard: "
    card_number = get_input(prompt, pattern)
    print(f"Detected card number: {card_number}")
    return card_number


def get_expiration_date():
    pattern = r'^\d{2}/\d{2}$'  # regex for MM/YY
    prompt = f"{Fore.MAGENTA}Please enter the credit card expiration date (MM/YY) or copy it to the clipboard: "
    expiration_date = get_input(prompt, pattern)
    print(f"Detected expiration date: {expiration_date}")
    return expiration_date


def get_cvc():
    pattern = r'^\d{3}$'  # regex for 3 digit verification code
    prompt = f"{Fore.MAGENTA}Please enter the credit card CVC/CVV or copy it to the clipboard: "
    cvc = get_input(prompt, pattern)
    print(f"Detected CVC/CVV: {cvc}")
    return cvc


if __name__ == "__main__":
    card_number = get_card_number()
    expiration_date = get_expiration_date()
    cvc = get_cvc()

    print(f"Card Number: {card_number}")
    print(f"Expiration Date: {expiration_date}")
    print(f"CVC/CVV: {cvc}")