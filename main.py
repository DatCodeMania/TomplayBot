from colorama import init
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from input_handler import InputHandler
from logging_formatter import setup_logger
from driver import get_driver

init(autoreset=True)


class TomplayBot:
    MONITOR_CLIPBOARD = True
    DEFAULT_WAIT_TIME = 30  # in seconds
    DEFAULT_RETRY_ATTEMPTS = 3

    def __init__(self):
        self.logger = setup_logger("TomplayBot")
        self.input_handler = InputHandler(should_monitor_clipboard=self.MONITOR_CLIPBOARD)
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, self.DEFAULT_WAIT_TIME)
        self.retry_attempts = self.DEFAULT_RETRY_ATTEMPTS

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

    def run(self):
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
