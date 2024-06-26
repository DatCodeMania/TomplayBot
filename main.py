import logging
import os
import random
import secrets
import string
import time
import uuid

import dotenv
from colorama import init
from selenium.webdriver.common.action_chains import ActionChains
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

    LOGGING_LEVEL = logging.DEBUG

    # Read OPTIONS.md
    INSTRUMENT = "Saxophone"
    LEVEL = "Intermediate"

    def __init__(self):
        self.logger = setup_logger(name="TomplayBot", level=self.LOGGING_LEVEL)
        self.input_handler = InputHandler(should_monitor_clipboard=self.MONITOR_CLIPBOARD)
        self.driver = get_driver()

        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)
        self.retry_attempts = self.DEFAULT_RETRY_ATTEMPTS

        self.email_domain = os.getenv("EMAIL_DOMAIN")

        self.instrument = self.INSTRUMENT
        self.level = self.LEVEL

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

    def switch_to_frame(self, title):
        frame = self.wait_for_visibility((By.CSS_SELECTOR, f"iframe[title='{title}']"))
        self.driver.switch_to.frame(frame)

    def random_delay(self, min_delay=1, max_delay=3):
        wait_time = random.uniform(min_delay, max_delay)
        self.logger.debug(f"Waiting for {wait_time} seconds to appear human.")
        time.sleep(wait_time)

    def humanized_type(self, element, text):
        self.logger.debug(f"Typing '{text}' in a human fashion...")
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))

    def interact_with_site(self):
        email = self.generate_random_email()
        password = self.generate_password()
        self.logger.debug("Loading site.")
        self.logger.debug(f"Email: {email}")
        self.logger.debug(f"Password: {password}")
        self.driver.get("https://tomplay.com/premium-trial")

        self.random_delay()

        self.logger.debug("Locating email entry element...")
        email_element = self.wait_for_clickability((By.ID, "register_email"))
        self.humanized_type(email_element, email)

        self.random_delay()

        self.logger.debug("Locating password entry element...")
        password_element = self.wait_for_clickability((By.ID, "register_password"))
        self.humanized_type(password_element, password)

        self.random_delay()

        # Select instrument
        self.logger.debug("Locating instrument selection element...")
        self.wait_for_clickability((By.CSS_SELECTOR, ".select2-selection.select2-selection--single")).click()
        self.random_delay()
        self.logger.debug("Selecting instrument from dropdown...")
        self.wait_for_clickability((By.XPATH, f"//li[text()='{self.instrument}']")).click()

        self.random_delay()

        # Select level
        self.logger.debug("Locating level selection element...")
        self.wait_for_clickability((By.CSS_SELECTOR, "#select2-level-container")).click()
        self.random_delay()
        self.logger.debug("Selecting level from dropdown...")
        self.wait_for_clickability((By.XPATH, f"//li[text()='{self.level}']")).click()

        self.random_delay()

        # Click the terms & co checkbox
        self.logger.debug("Locating checkbox parent div...")
        terms_checkbox_div = self.wait_for_clickability((By.XPATH, "//div[@class='custom-checkbox brand-checkbox terms-and-privacy ']"))
        ActionChains(self.driver).move_to_element(terms_checkbox_div).click().perform()

        self.random_delay()

        # Click create account button
        submit_button = self.wait_for_clickability((By.ID, "register-submit-btn"))
        ActionChains(self.driver).move_to_element(submit_button).click().perform()

        self.random_delay()

        # Input CC number
        self.logger.debug("Locating CC number input element...")
        self.switch_to_frame("Secure card number input frame")
        card_number_element = self.wait_for_clickability((By.NAME, "cardnumber"))
        self.humanized_type(card_number_element, self.card_number)
        self.driver.switch_to.default_content()

        self.random_delay()

        # Input CC expiration date
        self.logger.debug("Locating CC expiration date input element...")
        self.switch_to_frame("Secure expiration date input frame")
        expiry_element = self.wait_for_clickability((By.CSS_SELECTOR, "input[name='exp-date']"))
        self.humanized_type(expiry_element, self.expiration_date)
        self.driver.switch_to.default_content()

        self.random_delay()

        # Input CC CVC
        self.logger.debug("Locating CC CVC input element...")
        self.switch_to_frame("Secure CVC input frame")
        cvc_element = self.wait_for_clickability((By.NAME, "cvc"))
        self.humanized_type(cvc_element, self.cvc)
        self.driver.switch_to.default_content()

        self.random_delay()

        # Click start trial button
        self.logger.debug("Locating 'start trial' button...")
        start_trial_button = self.wait_for_clickability((By.CSS_SELECTOR, "a.btn.btn--brand.cartMakePayment"))
        ActionChains(self.driver).move_to_element(start_trial_button).click().perform()

    def run(self):
        self.logger.debug("Starting TomplayBot")
        self.card_number = self.input_handler.get_card_number()
        self.logger.debug(f"Card number obtained: {self.card_number}")

        self.expiration_date = self.input_handler.get_expiration_date()
        self.logger.debug(f"Expiration date obtained: {self.expiration_date}")

        self.cvc = self.input_handler.get_cvc()
        self.logger.debug(f"CVC obtained: {self.cvc}")

        self.logger.debug("Beginning site interactions.")
        self.interact_with_site()


if __name__ == "__main__":
    bot = TomplayBot()
    bot.run()
