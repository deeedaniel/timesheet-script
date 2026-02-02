from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Set up Chrome options to avoid bot detection
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Get credentials from environment variables
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

# Set up the browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Go to the login page
    driver.get("https://www.etimesheets.ihss.ca.gov/login")
    
    # Wait for page to load
    time.sleep(2)
    
    # TODO: Find and fill in the login form
    # Example (you'll need to inspect the page to get the correct element IDs):
    # username_field = driver.find_element(By.ID, "username")
    # password_field = driver.find_element(By.ID, "password")
    # username_field.send_keys(username)
    # password_field.send_keys(password)
    # login_button = driver.find_element(By.ID, "login-button")
    # login_button.click()
    
    # Wait for user to finish (press Enter to close)
    input("\nBrowser is open. Press Enter to close...")
    
finally:
    # Close the browser
    driver.quit()