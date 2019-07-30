from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import sys
import csv
import time

if len(sys.argv) != 7:
    print('Usage: python redeem_codes_school.py twitter_user_name twitter_password school_name reward_codes_file_path log_file_path element_load_timeout')
    sys.exit(1)

# Configurable parameters
twitter_user_name = sys.argv[1]
twitter_password = sys.argv[2]
# School name and zip code if possible
school_name = sys.argv[3]
reward_codes_file_path = sys.argv[4]
log_file_path = sys.argv[5]
# How long to wait for UI elements to load
element_load_timeout = int(sys.argv[6])

driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')

driver.get("https://us.coca-cola.com/give/schools/")

# Necessary utility function that waits for UI elements to load before accessing them
def wait_for_element_to_load(xpath : str):
    return WebDriverWait(driver,element_load_timeout).until(ec.presence_of_element_located((By.XPATH,xpath)))

# Sign in using twitter account (you can change the sign in method by changing the clicks to elements specified below)
login_icon = wait_for_element_to_load('//*[@id="icon_login"]')
# Wait extra (login button takes long time to load for some reason)
time.sleep(5)
login_icon.click()
login_button = wait_for_element_to_load('//*[@id="nav-profile-dropdown"]/ul[1]/li[1]')
login_button.click()
twitter_button = wait_for_element_to_load('//*[@id="janrain-twitter"]')
twitter_button.click()

# New twitter login window opens, so we have to focus into it to access elements
# Save current coke reward offers window handle
main_window_handle = driver.current_window_handle
twitter_window = list(set(driver.window_handles) - {main_window_handle})[0]
driver.switch_to.window(twitter_window)

user_name_input = wait_for_element_to_load('//*[@id="username_or_email"]')
password_input = wait_for_element_to_load('//*[@id="password"]')

user_name_input.send_keys(twitter_user_name)
password_input.send_keys(twitter_password)
password_input.submit()

# Done signing in
driver.switch_to.window(main_window_handle)

# Wait for main page to load again
time.sleep(10)

school_input_button = wait_for_element_to_load('//*[@id="_ec90261d-8d17-4704-8568-40d8860ee886_pageContent_responsivecolumncont_395902480_column0_donation_4c4b"]/div[1]/div/div[2]/div[2]/div/div[1]/span')

school_input_button.click()

school_input_box = wait_for_element_to_load('//*[@id="_ec90261d-8d17-4704-8568-40d8860ee886_pageContent_responsivecolumncont_395902480_column0_donation_4c4b"]/div[1]/div/div[2]/div[2]/div/input[1]')

school_input_box.send_keys(school_name)
school_input_box.send_keys(Keys.ENTER)

selected_choice = wait_for_element_to_load('//*[@id="ui-select-choices-row-0-0"]/span/div')

selected_choice.click()

with open(reward_codes_file_path) as csv_file:
    with open(log_file_path, mode='a') as log_file:
        number_of_codes_tested = 0

        csv_reader = csv.reader(csv_file)
        log_writer = csv.writer(log_file, lineterminator = '\n')

        # Skip header row
        next(csv_reader)

        # Write log header
        log_writer.writerow(['codes', 'status'])
        
        for row in csv_reader:
            # Reward code should be stored in first column
            code = row[0]
            code_input_box = wait_for_element_to_load('//*[@id="code-entry_179"]')
            code_input_box.clear()
            code_input_box.send_keys(code)
            code_input_box.submit()
            # Brief pause between each entry to allow the page to process previous input
            time.sleep(2)
            try:
                error_text = wait_for_element_to_load('//*[@id="_ec90261d-8d17-4704-8568-40d8860ee886_pageContent_responsivecolumncont_395902480_column0_donation_4c4b"]/p').text
                
                if 'invalid' in error_text:
                    log_writer.writerow([code, 'invalid'])
                elif 'has already been redeemed' in error_text:
                    log_writer.writerow([code, 'already_redeemed'])
                else:
                    # Weird case scenario
                    log_writer.writerow([code, error_text])
            except:
                log_writer.writerow([code, 'success'])

