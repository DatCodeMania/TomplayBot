import random
import uuid

from selenium import webdriver


# It would've probably been a good idea to make this more robust, however, for this project it should do
def get_random_user_agent():
    user_agents_pool = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
    ]
    return random.choice(user_agents_pool)


def get_driver():
    # Research these comments if you feel like it, they are mainly performance optimizations and also evasion methods.
    arguments = [
            "--window-size=1920,1080",
            f"user-agent={get_random_user_agent()}",
            "--disable-dev-shm-usage",
            "--no-sandbox",

            "--disable-client-side-phishing-detection",
            '--disable-default-apps',
            '--disable-features=Translate',
            '--no-default-browser-check',

            "--disable-renderer-backgrounding",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",

            '--disable-breakpad',
            "--disable-crash-reporter",
            "--disable-oopr-debug-crash-dump",
            "--no-crash-upload",
            "--disable-low-res-tiling",
            '--disable-component-update',
            '--disable-domain-reliability',
            '--disable-ipc-flooding-protection',
            '--disable-features=AutofillServerCommunication',
            '--disable-features=CertificateTransparencyComponentUpdater',
            '--disable-sync',
            '--no-pings',
            '--disable-features=OptimizationHints',

            "--disable-blink-features",
            "--disable-blink-features=AutomationControlled",

            f"--user-data-dir=./chrome_sessions/{uuid.uuid4()}",
        ]

    chrome_options = webdriver.ChromeOptions()

    for arg in arguments:
        chrome_options.add_argument(arg)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_extension("./uBlock0.chromium.crx")

    driver = webdriver.Chrome(options=chrome_options)
    return driver
