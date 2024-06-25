import re
import threading
import time
import pyperclip
from colorama import Fore


class InputHandler:
    def __init__(self, should_monitor_clipboard):
        self.should_monitor_clipboard = should_monitor_clipboard
        self.clipboard_content = None
        self.event = threading.Event()

    def monitor_clipboard(self, pattern):
        global clipboard_content
        while not self.event.is_set():
            current_clipboard = pyperclip.paste()
            if re.match(pattern, current_clipboard):
                clipboard_content = current_clipboard
                self.event.set()
            time.sleep(0.5)  # wait for performance purposes

    def get_input(self, prompt, pattern):
        global clipboard_content
        self.event.clear()
        clipboard_content = None
        thread = threading.Thread(target=self.monitor_clipboard, args=(pattern,), daemon=True)
        thread.start()
        print(prompt, end='', flush=True)

        while not self.event.is_set():
            current_clipboard = pyperclip.paste()
            if re.match(pattern, current_clipboard):
                clipboard_content = current_clipboard
                self.event.set()
                break

            time.sleep(0.5)  # wait for performance purposes

        thread.join()
        return clipboard_content

    def get_card_number(self):
        pattern = r'^\d{4} ?\d{4} ?\d{4} ?\d{4}$'  # regex for 16 digit credit card number, optional spaces
        if self.should_monitor_clipboard:
            prompt = f"{Fore.BLUE}[💳] Please copy the credit card number to the clipboard:"
            card_number = self.get_input(prompt, pattern)
            print(f"\n{Fore.GREEN}Detected card number: {card_number}")
            return card_number
        else:
            card_number = ""
            while not re.match(pattern, card_number):
                if card_number != "":
                    print(f"{Fore.RED}[⛔] Invalid credit card number!")
                card_number = input(f"{Fore.BLUE}[💳] Please enter the credit card number: {Fore.WHITE}")
            print(f"{Fore.GREEN}[✅] Card number accepted.")
            return card_number

    def get_expiration_date(self):
        pattern = r'^\d{2}/\d{2}$'  # regex for MM/YY
        if self.should_monitor_clipboard:
            prompt = f"{Fore.BLUE}[📅] Please copy the credit card expiration date (MM/YY) to the clipboard:"
            expiration_date = self.get_input(prompt, pattern)
            print(f"\n{Fore.GREEN}Detected expiration date: {expiration_date}")
            return expiration_date
        else:
            expiration_date = ""
            while not re.match(pattern, expiration_date):
                if expiration_date != "":
                    print(f"{Fore.RED}[⛔] Invalid credit card expiration date!(MM/YY)")
                expiration_date = input(f"{Fore.BLUE}[💳] Please enter the credit card expiration date (MM/YY): {Fore.WHITE}")
            print(f"{Fore.GREEN}[✅] Expiration date accepted.")
            return expiration_date

    def get_cvc(self):
        pattern = r'^\d{3}$'  # regex for 3 digit verification code
        if self.should_monitor_clipboard:
            prompt = f"{Fore.BLUE}[🔒] Please copy the credit card CVC/CVV to the clipboard:"
            cvc = self.get_input(prompt, pattern)
            print(f"\n{Fore.GREEN}Detected CVC/CVV: {cvc}")
            return cvc
        else:
            cvc = ""
            while not re.match(pattern, cvc):
                if cvc != "":
                    print(f"{Fore.RED}[⛔] Invalid credit card CVC/CVV!")
                cvc = input(f"{Fore.BLUE}[🔒] Please enter the credit card CVC/CVV: {Fore.WHITE}")
            print(f"{Fore.GREEN}[✅] CVC/CVV accepted.")
            return cvc
