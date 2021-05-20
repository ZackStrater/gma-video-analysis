# Web Scrapper for python
# Imports
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
class WebRunner:
    def __init__(self, driver_path = None, website = None, find = None, pause = 2):
        self.chrome_driver = self.driver(driver_path)
        self.setup = self.website(website)
        self.find = find
        self.data = set()
        self.pause = pause
    def driver(self, path):
        # Set up driver options. "How driver should run"
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        try:
            return webdriver.Chrome(path, options = options)
        except:
            return None
    def website(self, site):
        if site:
            try:
                self.chrome_driver.get(site)
                self.setup = True
                return self.setup
            except:
                return False
        return False
    def element(self, find):
        self.find = find
    # Scroll throught page
    def scroll(self, wait):
        current = self.chrome_driver.execute_script("return document.body.scrollHeight;")  # Current scroll height
        i = 0
        # Scroll through screen
        while True:
            self.chrome_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll down
            time.sleep(wait) # wait for page to load
            nh = self.chrome_driver.execute_script("return document.body.scrollHeight;")  # Current scroll height
            # Check if height is still the same if True the exit
            if nh == current:
                break
            current = nh
            print(f'Scrolling: {nh}')
    def run(self, size = 1, find = None):
        # Set up element to find
        if find: self.element(find)
        # Scroll window
        self.scroll(self.pause)
        # Get content
        item = self.chrome_driver.find_element_by_class_name(self.find)
        # Open file to write
        file = open('scrape_data.txt', 'a')
        try:
            file.write(item.text)
        except:
            print("Could not write into file")
        file.close()
        self.chrome_driver.close()

driver_path = '/home/zackstrater/Downloads/chromedriver'
web = WebRunner(driver_path=driver_path, website='https://www.instagram.com/goodmorningamerica/?hl=en')
web.find()