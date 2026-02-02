from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Chrome options to avoid bot detection
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Set up the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Go to a website (example: Google)
    driver.get("https://www.google.com")
    
    # Find the search box by its name attribute
    search_box = driver.find_element(By.NAME, "q")
    
    # Type something into it
    search_box.send_keys("Hello, world!")
    
    # Submit the form
    search_box.submit()
    
    # Wait for user to finish (press Enter to close)
    input("\nBrowser is open. Press Enter to close...")
    
finally:
    # Close the browser
    driver.quit()