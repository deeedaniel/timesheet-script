from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import random

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

    wait = WebDriverWait(driver, 10)

    for i in range(1, 4):
        print(f"\n=== Processing recipient {i} ===")
        
        enter_time_button = wait.until(
            EC.element_to_be_clickable((By.ID, f"enter-time-{i}"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", enter_time_button)
        time.sleep(0.5)

        enter_time_button.click()

        # Wait longer for the page to fully load
        time.sleep(7)

        # Find all expansion panels dynamically (they have different IDs for each recipient)
        # Use class name to find all panels on the page
        try:
            panels = driver.find_elements(By.CSS_SELECTOR, "mat-expansion-panel-header")
            print(f"Found {len(panels)} panels on page")
            
            # Open the first 3 panels (Workweek 1, 2, and 3)
            for idx, panel in enumerate(panels[:3]):
                try:
                    driver.execute_script("arguments[0].scrollIntoView(true);", panel)
                    time.sleep(0.5)
                    
                    # Check if panel is not already expanded
                    if "mat-expanded" not in panel.get_attribute("class"):
                        driver.execute_script("arguments[0].click();", panel)
                        time.sleep(1.5)
                        print(f"Opened panel {idx}")
                except Exception as e:
                    print(f"Could not open panel {idx}: {e}")
        except Exception as e:
            print(f"Could not find panels: {e}")

        time.sleep(2)

        # Configure times based on recipient
        # Recipient 1: 9:30am to 11:30am (2 hours)
        # Recipient 2: 11:30am to 1:30pm (2 hours)
        # Recipient 3: Random offset (2:05-4:05, 2:10-4:10, etc.) but still 2 hours

        # TODO: FIX THE RANDOM
        # The "random" is the SAME for all days, it should be different, and it should only be random between 0, 5, 10
        # For example, 2:00 to 4:00, 2:05 to 4:05, 2:10 to 4:10. Those are the only pairs.
        
        if i == 1:
            # Recipient 1: 9:30am to 11:30am
            start_time_str = "0930AM"
            end_time_str = "1130AM"
            print(f"Times for recipient 1: 9:30am to 11:30am")
        elif i == 2:
            # Recipient 2: 11:30am to 1:30pm
            start_time_str = "1130AM"
            end_time_str = "0130PM"
            print(f"Times for recipient 2: 11:30am to 1:30pm")
        else:  # i == 3
            # Recipient 3: Random offset between 0-59 minutes, 2:XX to 4:XX pm
            random_offset = random.randint(0, 59)
            start_time_str = f"02{random_offset:02d}PM"
            end_time_str = f"04{random_offset:02d}PM"
            print(f"Random times for recipient 3: 2:{random_offset:02d}pm to 4:{random_offset:02d}pm")
        
        # Fill in time for Monday-Friday for each workweek
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
                    
                    # Fill start time
                    starttime_input = driver.find_element(By.ID, f"starttime-{workweek * 7 + day}")
                    starttime_input.clear()
                    starttime_input.send_keys(start_time_str)
                    time.sleep(0.2)
                    
                    # Fill end time
                    endtime_input = driver.find_element(By.ID, f"endtime-{workweek * 7 + day}")
                    endtime_input.clear()
                    endtime_input.send_keys(end_time_str)
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

        # import pdb; pdb.set_trace()

        # Wait for save button to be clickable
        save_button = wait.until(
            EC.element_to_be_clickable((By.ID, "save-timesheet-button-0"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", save_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", save_button)
        print("Clicked save button")

        time.sleep(3)

        # Wait for back arrow to be clickable
        back_button = wait.until(
            EC.element_to_be_clickable((By.ID, "backarrow"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", back_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", back_button)
        print(f"Completed recipient {i}, going back to list")

        time.sleep(3)
    
    # Wait for user to finish (press Enter to close)
    input("\nBrowser is open. Press Enter to close...")

    
finally:
    # Close the browser
    driver.quit()