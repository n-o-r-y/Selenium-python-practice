from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driverLink = "https://practicetestautomation.com/practice-test-login/"
driver.get(driverLink)
maximize_window = driver.maximize_window()

user_name = driver.find_element(By.ID, "username")
user_name.send_keys("student")
user_password = driver.find_element(By.ID, "password")  
user_password.send_keys("Password")
logIn_btn = driver.find_element(By.ID, "submit")
logIn_btn.click()

wait = WebDriverWait(driver, 10)
error_msg = wait.until(EC.visibility_of_element_located((By.ID, "error")))

expected_msg = "Your password is invalid!"
if(error_msg.text == expected_msg):
    print("Test passed: Correct error message displayed for invalid password.")
else:
    print("Test failed: Incorrect error message displayed.")    

time.sleep(5)