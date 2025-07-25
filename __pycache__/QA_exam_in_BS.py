from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pytest

website_url = "https://test.nop-station.store"

@pytest.fixture
def setup():
    """Setup"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(website_url)
    yield driver
    driver.quit()

def skip(func):
    def inner(*args, **kwargs):
        pytest.skip("Skipping this test as per request.")
    return inner

def test_user_login(setup):
    """Login Test"""
    driver = setup
    wait = WebDriverWait(driver, 10)
    user_name = "nusrat__" 
    password = "abc123"
    login_link = driver.find_element(By.XPATH, "//a[@class='ico-login']")
    login_link.click()
    time.sleep(2)
    driver.find_element(By.ID, "Username").send_keys(user_name)
    driver.find_element(By.ID, "Password").send_keys(password)
    driver.find_element(By.CLASS_NAME, "login-button").click()
    time.sleep(3)
    welcome_text_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='topic-block-title']/h2"))
    )
    assert "Welcome to our store" in welcome_text_element.text

@skip
def test_search_for_awesome_products(setup):
    """Search for Awesome Products"""
    driver = setup
    wait = WebDriverWait(driver, 10)  
    searched_key = "Awesome"
    
    search_box = driver.find_element(By.CSS_SELECTOR, ".search-box-text.ui-autocomplete-input")
    search_box.send_keys(searched_key)

    search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-1.search-box-button")))
    search_btn.click()

    searched_products = driver.find_elements(By.CSS_SELECTOR, ".product-title")  
    for product in searched_products:
        assert searched_key.lower() in product.text.lower(), f"Product '{product.text}' does not contain '{searched_key}'"

    time.sleep(5)

@skip
def test_add_awesome_products_to_cart(setup):
    """Add Products to Carts"""
    driver = setup
    wait = WebDriverWait(driver, 10)

    search_box = driver.find_element(By.CSS_SELECTOR, ".search-box-text.ui-autocomplete-input")
    search_box.clear()
    search_box.send_keys("Awesome")
    search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-1.search-box-button")))
    search_btn.click()
    time.sleep(2) 

    products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    assert len(products) >= 2, "Less than 2 'Awesome' products found"

    total_cost = 0.0
    added_products = []

    for product in products[:2]:
        product_name = product.find_element(By.CSS_SELECTOR, ".product-title").text
        product_price_text = product.find_element(By.CSS_SELECTOR, ".price").text
        product_price = float(product_price_text.replace('$', '').replace(',', '').strip())

        add_to_cart_btn = product.find_element(By.CSS_SELECTOR, ".product-box-add-to-cart-button")
        add_to_cart_btn.click()
        time.sleep(2)

        total_cost += product_price
        added_products.append((product_name, product_price))
      
    assert total_cost >= 200.00, f"Total cost is ${total_cost:.2f}, which is less than $200.00."
    cart_link = driver.find_element(By.XPATH, "//a[@class='ico-cart']")
    cart_link.click()
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Shopping cart"))

def test_checkout_process(setup):
    """Check Out Process from the login to billing process"""
    driver = setup
    wait = WebDriverWait(driver, 10)

    # Log in
    user_name = "nusrat__" 
    password = "abc123"
    login_link = driver.find_element(By.XPATH, "//a[@class='ico-login']")
    login_link.click()
    time.sleep(2)  

    search_box = driver.find_element(By.CSS_SELECTOR, ".search-box-text.ui-autocomplete-input")
    search_box.clear()
    search_box.send_keys("Awesome")
    search_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-1.search-box-button")))
    search_btn.click()
    time.sleep(2) 
    products = driver.find_elements(By.CSS_SELECTOR, ".product-item")
    assert len(products) >= 2, "Less than 2 'Awesome' products found"

    total_cost = 0.0
    added_products = []

    for product in products[:2]:
        product_name = product.find_element(By.CSS_SELECTOR, ".product-title").text
        product_price_text = product.find_element(By.CSS_SELECTOR, ".price").text
        product_price = float(product_price_text.replace('$', '').replace(',', '').strip())

        add_to_cart_btn = product.find_element(By.CSS_SELECTOR, ".product-box-add-to-cart-button")
        add_to_cart_btn.click()
        time.sleep(2)  

        total_cost += product_price
        added_products.append((product_name, product_price))

    assert total_cost >= 200.00, f"Total cost is ${total_cost:.2f}, which is less than $200.00."

    driver.back()
    cart_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.ico-cart"))
    )
    cart_link.click()
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "h1"), "Shopping cart")) 
    tos_checkbox = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "termsofservice"))
    )
    tos_checkbox.click()

    checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "checkout")))
    checkout_button.click()


    wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Checkout']")))

    billing_heading = wait.until(
    EC.visibility_of_element_located((By.XPATH, "//h2[@class='step-title' and text()='Billing address']"))
)
    assert "Billing address" in billing_heading.text
    driver.find_element(By.ID, "BillingNewAddress_FirstName").send_keys("Nusrat Jahan")
    driver.find_element(By.ID, "BillingNewAddress_LastName").send_keys("Nory")
    driver.find_element(By.ID, "BillingNewAddress_Email").send_keys("nusrat123@test.com")
    country_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "BillingNewAddress_CountryId")))
    country_dropdown.click()
    driver.find_element(By.XPATH, "//select[@id='BillingNewAddress_CountryId']/option[text()='Bangladesh']").click() 
    driver.find_element(By.ID, "BillingNewAddress_City").send_keys("Dhaka")
    driver.find_element(By.ID, "BillingNewAddress_Address1").send_keys("123 Main St")
    driver.find_element(By.ID, "BillingNewAddress_ZipPostalCode").send_keys("10001")
    driver.find_element(By.ID, "BillingNewAddress_PhoneNumber").send_keys("1234567890")
    continue_button = driver.find_element(By.XPATH, "//button[@onclick='Billing.save()']")
    continue_button.click()

    wait.until(EC.element_to_be_clickable((By.ID, "ShipToSameAddress"))).click()  
    continue_button = driver.find_element(By.XPATH, "//button[@onclick='Shipping.save()']")
    continue_button.click()

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='shippingoption_1']"))).click()
    continue_button = driver.find_element(By.XPATH, "//button[@onclick='ShippingMethod.save()']")
    continue_button.click()

    wait.until(EC.visibility_of_element_located((By.ID, "CreditCardType"))).send_keys("Visa")  
    driver.find_element(By.ID, "CardholderName").send_keys("Nusrat")
    driver.find_element(By.ID, "CardNumber").send_keys("4111111111111111") 
    driver.find_element(By.ID, "ExpireMonth").send_keys("09") 
    driver.find_element(By.ID, "ExpireYear").send_keys("2030") 
    driver.find_element(By.ID, "CardCode").send_keys("129") 

    continue_button = driver.find_element(By.XPATH, "//button[@onclick='PaymentMethod.save()']")
    continue_button.click()
    print("Checkout process completed successfully.")
