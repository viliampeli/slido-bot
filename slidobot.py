from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys
import getopt

class SlidoBot:
    def __init__(self, hash=None, xpath=None, driver_path=None, delay=2):
        if hash is None or xpath is None or driver_path is None:
            raise ValueError("Invalid argument: hash, xpath, and driver_path are required")
        self.hash = hash
        self.xpath = xpath
        self.driver_path = driver_path
        self.delay = delay  # Delay in seconds between actions

    def vote(self):
        # Set up Chrome options for headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--disable-gpu")  # Disable GPU rendering
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        service = Service(executable_path=self.driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get("https://app.sli.do/event/" + self.hash + "/live/questions")
            button_elem = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, self.xpath))
            )
            driver.execute_script("arguments[0].click();", button_elem)

            time.sleep(self.delay)

        except Exception as e:
            print(f"Error during voting: {str(e)}")
        finally:
            driver.quit()


def main():
    HASH = None
    XPATH = None
    DRIVER_PATH = None
    VOTES = 1
    DELAY = 2

    try:
        options, args = getopt.getopt(
            sys.argv[1:], "h:x:d:v:t:",
            ["hash=", "xpath=", "driver=", "votes=", "delay="]
        )
        for name, value in options:
            if name in ('-h', '--hash'):
                HASH = value
            if name in ('-x', '--xpath'):
                XPATH = value
            if name in ('-d', '--driver'):
                DRIVER_PATH = value
            if name in ('-v', '--votes'):
                VOTES = int(value)
            if name in ('-t', '--delay'):
                DELAY = int(value)

        if not HASH or not XPATH or not DRIVER_PATH:
            raise ValueError("Hash, XPath, and Driver Path are required arguments")

    except getopt.GetoptError as err:
        print(str(err))
        print("Invalid args!")
        sys.exit(1)
    except ValueError as ve:
        print(str(ve))
        sys.exit(1)

    for i in range(1, VOTES + 1):
        BOT = SlidoBot(HASH, XPATH, DRIVER_PATH, delay=DELAY)
        BOT.vote()
        print("Votes: " + str(i))

if __name__ == "__main__":
    print("Have fun.")
    main()
