# get 'bad request' from Safari, if change Card Type from basic or reversed to some other type
import selenium.common
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from definitii import backup_title_list, backup_entry_list

# for roman telega
login_mode = False
tries = 0


def add_card():
    card_front = backup_title_list[0]
    card_back = backup_entry_list[0]

    PATH = '/usr/bin/safaridriver'
    driver = webdriver.Safari(PATH)
    driver.get('https://ankiweb.net/account/login')

# logging in using entered email and password

    user_info = open('user_info', 'r')
    email_input = user_info.readline()
    pasword_input = user_info.readline().strip('\n')
    email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@placeholder='Email']")))
    email.send_keys(email_input)

    password = driver.find_element(By.XPATH, "//*[@placeholder='Password']")
    password.send_keys(pasword_input)

# clicking the login button
    try:
        login = driver.find_element(By.XPATH, "//*[@class='btn btn-primary btn-lg']")
        login.click()
        add_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Add')))
        add_button.click()
    except selenium.common.ElementNotInteractableException:
        return 'Invalid login! (Type ‹login› to reauthorize)'

# changing card type for 'basic'
    try:
        card_type = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='svelte-apvs86']")))
        card_type.click()
        basic_type = driver.find_element(By.XPATH, "//*[@class='item svelte-apvs86 first']")
        basic_type.click()

# filling the fields
    finally:
        fields = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//*[@class='form-control field']")))
        fields[0].send_keys(card_front)
        fields[1].send_keys(card_back)
        card_ready = driver.find_element(By.XPATH, "//*[@class='btn btn-primary btn-large mt-2']")
        card_ready.click()
        time.sleep(1)
        driver.close()

