import logging
import os
import secrets
import string
import uuid

import dotenv
from colorama import init
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from driver import get_driver
from input_handler import InputHandler
from logging_formatter import setup_logger

init(autoreset=True)
dotenv.load_dotenv()


class TomplayBot:
    MONITOR_CLIPBOARD = True
    DEFAULT_WAIT_TIME = 30  # in seconds
    DEFAULT_RETRY_ATTEMPTS = 3

    def __init__(self):
        self.logger = setup_logger(name="TomplayBot", level=logging.INFO)
        self.input_handler = InputHandler(should_monitor_clipboard=self.MONITOR_CLIPBOARD)
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)
        self.retry_attempts = self.DEFAULT_RETRY_ATTEMPTS
        self.email_domain = os.getenv("EMAIL_DOMAIN")

    def wait_for_visibility(self, locator):
        for _ in range(self.retry_attempts):
            try:
                return self.wait.until(EC.presence_of_element_located(locator))
            except Exception as e:
                self.logger.warning(f"Exception finding visibility of {locator}, refreshing page.")
                self.logger.debug(f"Error: {e!r}")
                self.driver.refresh()
                continue
        raise RuntimeError("Attempts exhausted to find visibility")

    def wait_for_clickability(self, locator):
        for _ in range(self.retry_attempts):
            try:
                return self.wait.until(EC.element_to_be_clickable(locator))
            except Exception as e:
                self.logger.warning(f"Exception finding clickability of {locator}, refreshing page.")
                self.logger.debug(f"Error: {e!r}")
                self.driver.refresh()
                continue
        raise RuntimeError("Attempts exhausted to find clickability")

    def generate_random_email(self):
        unique_id = uuid.uuid4().hex[:8]
        return f"tomplay_{unique_id}@{self.email_domain}"

    def generate_password(self):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))

    def interact_with_site(self):
        email = self.generate_random_email()
        password = self.generate_password()
        self.driver.get("https://tomplay.com/premium-trial")
        self.wait_for_clickability((By.ID, "register_email")).send_keys(email)
        self.wait_for_clickability((By.ID, "register_password")).send_keys(password)
        self.wait_for_clickability((By.CSS_SELECTOR, ".select2-selection.select2-selection--single")).click()
        self.wait_for_clickability((By.XPATH, "//li[text()='Saxophone']")).click()
        self.wait_for_clickability((By.CSS_SELECTOR, "#select2-level-container")).click()
        self.wait_for_clickability((By.XPATH, "//li[text()='Intermediate']")).click()
        # TODO: Fix below two statements, currently not functional.
        self.wait_for_clickability((By.XPATH, "//div[@class='custom-checkbox brand-checkbox terms-and-privacy']/input[@name='terms_and_conditions']")).click()
        self.wait_for_clickability((By.ID, "register-submit-btn")).click()

    def run(self):
        self.interact_with_site()
        self.logger.debug("Starting TomplayBot")
        card_number = self.input_handler.get_card_number()
        self.logger.debug(f"Card number obtained: {card_number}")

        expiration_date = self.input_handler.get_expiration_date()
        self.logger.debug(f"Expiration date obtained: {expiration_date}")

        cvc = self.input_handler.get_cvc()
        self.logger.debug(f"CVC obtained: {cvc}")


if __name__ == "__main__":
    bot = TomplayBot()
    bot.run()
