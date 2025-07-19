from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://practicetestautomation.com/practice-test-login/")
wait = WebDriverWait(driver, 10)

# Step 1: Enter username
user_name = driver.find_element(By.ID, "username")
user_name.send_keys("student")

# Step 2: Enter password
user_password = driver.find_element(By.ID, "password")
user_password.send_keys("Password123")

# Step 3: Click login
button_login = driver.find_element(By.ID, "submit")
button_login.click()

# Step 4: Wait for successful login URL
wait.until(EC.url_to_be("https://practicetestautomation.com/logged-in-successfully/"))

# Step 5: Validate login
expected_login_url = "https://practicetestautomation.com/logged-in-successfully/"
if driver.current_url == expected_login_url:
    print("Login successful")

    # Step 6: Click "Log out"
    logout_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Log out")))
    logout_link.click()

    # Step 7: Wait for redirect to login page
    wait.until(EC.url_to_be("https://practicetestautomation.com/practice-test-login/"))

    # Step 8: Validate logout
    if driver.current_url == "https://practicetestautomation.com/practice-test-login/":
        print("Logout successful, back to login page")
    else:
        print("Logout failed: Not redirected to login page")

else:
    print("Login failed")

time.sleep(3)
driver.quit()
