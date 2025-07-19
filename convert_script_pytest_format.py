import pytest
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

login_url = "https://practicetestautomation.com/practice-test-login/"
login_success_url = "https://practicetestautomation.com/logged-in-successfully/"

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_login_success(driver):
    driver.get(login_url)
    wait = WebDriverWait(driver, 10)

    user_name = driver.find_element(By.ID, "username")
    user_name.send_keys("student")
    user_password = driver.find_element(By.ID, "password")
    user_password.send_keys("Password123")
    button_login = driver.find_element(By.ID, "submit")
    button_login.click()

    wait.until(EC.url_to_be(login_success_url))
    current_url = driver.current_url

    if(current_url == login_success_url):
        print("Login successful")

        logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log out")))
        logout_link.click()
        wait.until(EC.url_to_be(login_url))
        print("Logged out successfully")
    else:
        print("Login failed: Not redirected to success page")

    time.sleep(5)

def test_login_invalid_password(driver):
    driver.get(login_url)
    wait = WebDriverWait(driver, 10)

    user_name = driver.find_element(By.ID, "username")
    user_name.send_keys("student")
    user_password = driver.find_element(By.ID, "password")
    user_password.send_keys("InvalidPassword")
    button_login = driver.find_element(By.ID, "submit")
    button_login.click()

    wait.until(EC.url_to_be(login_url))
    current_url = driver.current_url

    if(current_url == login_url):
        print("Login failed: Invalid password")
    else:
        print("Login successful")

    time.sleep(5)
