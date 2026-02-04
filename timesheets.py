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

    username_field = driver.find_element(By.ID, "input-user-name")
    password_field = driver.find_element(By.ID, "input-password")

    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "login")

    # Scroll to the button to make sure it's visible
    driver.execute_script("arguments[0].scrollIntoView(true);", login_button)
    time.sleep(2)  # Brief pause after scrolling
    login_button.click()

    time.sleep(2)

    # Click the info button to close the info modal
    driver.find_element(By.ID, "info-button-ok").click()

    time.sleep(2)

    driver.find_element(By.ID, "timecardEntry").click()

    # Python Debugger
    # import pdb; pdb.set_trace()

    time.sleep(2)

    # Click enter time for first care recipient
    driver.find_element(By.ID, "enter-time-1").click()

    time.sleep(5)

    # Open all expansion panels (Workweek 1, 2, and 3)
    for panel_id in range(3):
        try:
            panel = driver.find_element(By.ID, f"mat-expansion-panel-header-{panel_id}")
            driver.execute_script("arguments[0].scrollIntoView(true);", panel)
            # Check if panel is not already expanded
            if "mat-expanded" not in panel.get_attribute("class"):
                panel.click()
                time.sleep(1)
        except Exception as e:
            print(f"Could not open panel {panel_id}: {e}")

    time.sleep(2)

    # Fill in time for Monday-Friday (9:30am to 11:30am) for each workweek
    # Workweeks have different day configurations:
    # Workweek 1: days 0-6 (Sunday-Saturday)
    # Workweek 2: days 0-6 (Sunday-Saturday)
    # Workweek 3: Only Sunday (day 0), rest are out of pay period
    
    workweek_configs = [
        (0, [1, 2, 3, 4, 5]),  # Workweek 1: Monday-Friday (indices 1-5)
        (1, [1, 2, 3, 4, 5]),  # Workweek 2: Monday-Friday (indices 1-5)
    ]
    
    for workweek, days in workweek_configs:
        for day in days:
            try:
                # Calculate the absolute input index
                # Each day has: hours, minutes, starttime, endtime inputs
                # Base index is workweek * 7 days * 4 inputs per day
                base_index = workweek * 7 * 4 + day * 4
                
                # Fill hours (02)
                hours_input = driver.find_element(By.ID, f"hours-{workweek * 7 + day}")
                hours_input.clear()
                hours_input.send_keys("02")
                
                # Fill minutes (00)
                minutes_input = driver.find_element(By.ID, f"minutes-{workweek * 7 + day}")
                minutes_input.clear()
                minutes_input.send_keys("00")
                
                # Fill start time (09:30 AM)
                starttime_input = driver.find_element(By.ID, f"starttime-{workweek * 7 + day}")
                starttime_input.clear()
                starttime_input.send_keys("0930AM")
                time.sleep(0.2)
                
                # Fill end time (11:30 AM)
                endtime_input = driver.find_element(By.ID, f"endtime-{workweek * 7 + day}")
                endtime_input.clear()
                endtime_input.send_keys("1130AM")
                time.sleep(0.2)
                
                # Select start location (Home)
                start_location = driver.find_element(By.ID, f"start-locationSelect-{workweek * 7 + day}")
                start_location.send_keys("Home")
                
                # Select end location (Home)
                end_location = driver.find_element(By.ID, f"end-locationSelect-{workweek * 7 + day}")
                end_location.send_keys("Home")
                
                time.sleep(0.5)
                print(f"Filled Workweek {workweek + 1}, Day {day} (Monday-Friday)")
                
            except Exception as e:
                print(f"Could not fill Workweek {workweek + 1}, Day {day}: {e}")
    
    print("\nAll time entries filled successfully!")
    
    # Wait for user to finish (press Enter to close)
    input("\nBrowser is open. Press Enter to close...")

    
finally:
    # Close the browser
    driver.quit()