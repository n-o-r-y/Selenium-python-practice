import pytest
import time

from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

url = "https://automationexercise.com"

def skip(func):
    def inner(*args, **kwargs):
        pytest.skip("Skipping this test as per request.")
    return inner

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    yield driver
    driver.quit()


def test_click_products_btn(driver):
    wait = WebDriverWait(driver, 2)
    product_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Products')]")
    product_btn.click()
    EC.url_to_be(f"{url}/products")
    assert driver.current_url == f"{url}/products", "Failed to navigate to Products page"

@skip
def test_search_for_product(driver):
    wait = WebDriverWait(driver, 2)
    product_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Products')]")
    product_btn.click()
    EC.url_to_be(f"{url}/products")

    search_box = wait.until(EC.visibility_of_element_located((By.ID, "search_product")))
    search_box.send_keys("Blue Top")

    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_search")))
    search_btn.click()

    searched_product = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Blue Top']")))
    assert searched_product.is_displayed(), "Searched product 'Blue Top' is not displayed"

@skip
def test_search_for_products(driver):
    wait = WebDriverWait(driver, 2)
    product_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Products')]")
    product_btn.click()
    EC.url_to_be(f"{url}/products")

    search_keyword = "Blue".lower()

    search_box = wait.until(EC.visibility_of_element_located((By.ID, "search_product")))
    search_box.send_keys(search_keyword)

    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_search")))
    search_btn.click()

    searched_products = driver.find_elements(By.CSS_SELECTOR, ".productinfo>p")

    for product in searched_products:
        assert search_keyword in product.text.lower(), f"Product '{product.text}' does not contain '{search_keyword}'"

def test_search_for_non_existent_product(driver):
    """
    If the product does not exist, the message "No products found" should be displayed.
    """

    wait = WebDriverWait(driver, 2)
    product_btn = driver.find_element(By.XPATH, "//a[contains(text(), 'Products')]")
    product_btn.click()
    EC.url_to_be(f"{url}/products")

    search_keyword = "NonExistentProduct"
    search_box = driver.find_element(By.ID, "search_product")
    search_box.send_keys(search_keyword)

    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_search")))
    search_btn.click()

    searched_products = driver.find_elements(By.CSS_SELECTOR, ".productinfo>p")

    assert not len(searched_products), f"Products found for non-existent search '{search_keyword}'"

@skip
def test_home_page_visibility(driver):
    wait = WebDriverWait(driver, 10)
    logo = wait.until(EC.visibility_of_element_located((By.XPATH, "//img[@alt='Website for automation practice']")))
    assert logo.is_displayed(), "Home page logo is not visible"

@skip
def test_navigate_to_signup_page(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Signup / Login").click()
    signup_heading = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='New User Signup!']")))
    assert signup_heading.is_displayed(), "Signup heading is not visible"

@skip
def test_enter_name_and_email(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Signup / Login").click()
    signup_heading = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='New User Signup!']")))
    assert signup_heading.is_displayed(), "Signup heading is not visible"

    input_name = wait.until(EC.visibility_of_element_located((By.NAME, "name")))
    input_name.send_keys("Test Userno")

    unique_email = f"testuser_{int(time.time())}@example.com"
    input_email = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='signup-email']")))
    input_email.send_keys(unique_email)

    signup_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text() = 'Signup']")))
    signup_btn.click()

    # Wait for the next page or confirmation element
    confirmation = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Enter Account Information')]")))
    assert confirmation.is_displayed(), "Account information page not loaded"

@skip
def test_enter_account_details(driver):
    wait = WebDriverWait(driver, 10)
    driver.find_element(By.LINK_TEXT, "Signup / Login").click()
    input_name = wait.until(EC.visibility_of_element_located((By.NAME, "name")))
    input_name.send_keys("Test Userno")

    import time
    unique_email = f"testuser_{int(time.time())}@example.com"
    input_email = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='signup-email']")))
    input_email.send_keys(unique_email)

    signup_btn = driver.find_element(By.XPATH, "//button[text() = 'Signup']")
    signup_btn.click()

    wait = WebDriverWait(driver, 2)
    gender_radio = driver.find_element(By.ID, "id_gender2")
    gender_radio.click()

    input_password = driver.find_element(By.ID, "password")
    input_password.send_keys("TestPassword123")

    signup_btn = driver.find_element(By.XPATH, "//button[text() = 'Signup']")
    signup_btn.click()

    Select(driver.find_element(By.ID, "days")).select_by_visible_text("1")
    Select(driver.find_element(By.ID, "months")).select_by_visible_text("January")
    Select(driver.find_element(By.ID, "years")).select_by_visible_text("1990")
    
    driver.find_element(By.ID, "newsletter").click()
    driver.find_element(By.ID, "optin").click()

    # Step 12: Fill address and contact details
    driver.find_element(By.ID, "first_name").send_keys("Test")
    driver.find_element(By.ID, "last_name").send_keys("User")
    driver.find_element(By.ID, "company").send_keys("TestCorp")
    driver.find_element(By.ID, "address1").send_keys("123 Test Street")
    driver.find_element(By.ID, "address2").send_keys("Apt 456")

    # Select Country from dropdown
    Select(driver.find_element(By.ID, "country")).select_by_visible_text("Canada")

    driver.find_element(By.ID, "state").send_keys("Ontario")
    driver.find_element(By.ID, "city").send_keys("Toronto")
    driver.find_element(By.ID, "zipcode").send_keys("M5J2N8")
    driver.find_element(By.ID, "mobile_number").send_keys("+1 234 567 8901")

    driver.find_element(By.XPATH, "//button[text() = 'Create Account']").click()
        # Step 14: Verify 'ACCOUNT CREATED!' is visible
    try:
        success_msg = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//b[text()='Account Created!']"))
        )
        assert success_msg.is_displayed(), "'ACCOUNT CREATED!' message not visible"
        print("✅ 'ACCOUNT CREATED!' message is visible.")
    except Exception as e:
        assert False, f"❌ Failed to verify 'ACCOUNT CREATED!' message: {e}"
