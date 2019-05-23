from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import pandas as pd
import sys

if len(sys.argv) != 6:
    print('Usage: python redeem_codes.py twitter_user_name twitter_password desired_awards reward_codes_file_path element_load_timeout')
    sys.exit(1)

# Configurable parameters
twitter_user_name = sys.argv[1]
twitter_password = sys.argv[2]
# Which awards you would like to distribute your codes to (see the below rewards table for all available rewards)
desired_rewards = sys.argv[3].split(',')
reward_codes_file_path = sys.argv[4]
# How long to wait for UI elements to load
element_load_timeout = int(sys.argv[5])

driver = webdriver.Chrome('chromedriver_win32/chromedriver.exe')

driver.get("https://us.coca-cola.com/offers/")

# Necessary utility function that waits for UI elements to load before accessing them
def wait_for_element_to_load(xpath : str):
    return WebDriverWait(driver,element_load_timeout).until(ec.presence_of_element_located((By.XPATH,xpath)))

# Sign in using twitter account (you can change the sign in method by changing the clicks to elements specified below)
login_icon = wait_for_element_to_load('//*[@id="icon_login"]')
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

# Holds reward name and its respective element xpath
rewards_table = [
    ('OliveGarden', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_1344331841_column0_codeentry_e960"]'),
    ('Dominos', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_column0_codeentry_cd4d"]'),
    ('AMCTheaters', '//*[@id="enter_code_id_content_coke2016_en_amc_multi_layer_offer_jcr_content_common_content_iparsys_responsivecolumncont_column0_codeentry_ec58"]'),
    ('Magazines', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_1949744869_column0_codeentry_a45c"]'),
    ('iTunes', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_1616209238_column0_codeentry_1135"]'),
    ('Nordstrom', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_1356747955_column0_codeentry_e30c"]'),
    ('Chilis', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_codeentry_d92e"]'),
    ('Shutterfly', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_1164568584_column0_codeentry_9cf"]'),
    ('Drink', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_285521029_column0_codeentry_ec58"]'),
    ('Groceries', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_140468331_column0_codeentry_6b0d"]'),
    ('Coffee', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_353597540_column0_codeentry_49d0"]'),
    ('VendingMachine', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_921245997_column0_codeentry_152a"]'),
    ('UHDTV', '//*[@id="enter_code_id_content_coke2016_en_offers_jcr_content_pageContent_responsivecolumncont_1067140601_column0_codeentry_a9fd"]')
]

data = pd.read_csv(reward_codes_file_path)

number_of_codes_tested = 0
for code in data['codes']:
    reward_index = number_of_codes_tested % len(desired_rewards)
    desired_reward_name = desired_rewards[reward_index]
    desired_reward_xpath = [item[1] for item in rewards_table if item[0] == desired_reward_name][0]
    desired_reward_input = wait_for_element_to_load(desired_reward_xpath)
    ActionChains(driver).move_to_element(desired_reward_input).perform()
    desired_reward_input.clear()
    desired_reward_input.send_keys(code)
    desired_reward_input.submit()
    number_of_codes_tested += 1
