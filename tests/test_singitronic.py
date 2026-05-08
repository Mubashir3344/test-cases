"""
Selenium automated test suite for Singitronic web application.
Target: http://13.51.242.231  (configurable via APP_URL env var)
Requires: headless Chrome with ChromeDriver at /usr/local/bin/chromedriver
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = os.environ.get("APP_URL", "http://13.51.242.231").rstrip("/")


@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    service = Service("/usr/local/bin/chromedriver")
    d = webdriver.Chrome(service=service, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()


def test_01_homepage_loads(driver):
    driver.get(BASE_URL)
    assert driver.title != "", "Page title should not be empty"
    assert "error" not in driver.title.lower(), "Home page should not show an error title"


def test_02_homepage_has_content(driver):
    driver.get(BASE_URL)
    assert len(driver.page_source) > 200, "Page source should have meaningful content"


def test_03_login_page_loads(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    assert email_field.is_displayed(), "Email field must be visible on login page"


def test_04_login_email_field_type(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    assert field.get_attribute("type") == "email", "Email field must have type='email'"


def test_05_login_password_field_type(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    assert field.get_attribute("type") == "password", "Password field must have type='password'"


def test_06_login_remember_me_checkbox(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    cb = wait.until(EC.presence_of_element_located((By.ID, "remember-me")))
    assert cb.get_attribute("type") == "checkbox", "Remember-me must be a checkbox input"


def test_07_login_submit_button_exists(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    assert btn.is_displayed(), "Submit button must be visible on login page"


def test_08_login_invalid_email_shows_error(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    pwd = driver.find_element(By.ID, "password")
    email.clear()
    email.send_keys("not-an-email")
    pwd.clear()
    pwd.send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-red-600")))
    assert error.text.strip() != "", "An error message must appear for an invalid e-mail format"


def test_09_login_short_password_shows_error(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    pwd = driver.find_element(By.ID, "password")
    email.clear()
    email.send_keys("user@example.com")
    pwd.clear()
    pwd.send_keys("short")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-red-600")))
    assert error.text.strip() != "", "An error message must appear when password is too short"


def test_10_login_wrong_credentials_shows_error(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
    pwd = driver.find_element(By.ID, "password")
    email.clear()
    email.send_keys("nonexistent_xyz_99@example.com")
    pwd.clear()
    pwd.send_keys("WrongPassword999")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(3)
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-red-600")))
    assert error.text.strip() != "", "An error message must appear for wrong credentials"


def test_11_register_page_loads(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    assert name_field.is_displayed(), "Name field must be visible on register page"


def test_12_register_name_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    assert field.get_attribute("type") == "text", "Name field must have type='text'"


def test_13_register_lastname_field_exists(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "lastname")))
    assert field.is_displayed(), "Lastname field must be visible on register page"


def test_14_register_email_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    assert field.get_attribute("type") == "email", "Register email field must have type='email'"


def test_15_register_password_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    assert field.get_attribute("type") == "password", "Password field must have type='password'"


def test_16_register_confirmpassword_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "confirmpassword")))
    assert field.get_attribute("type") == "password", "Confirm-password must have type='password'"


def test_17_register_password_mismatch_shows_error(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.ID, "name"))).send_keys("Test")
    driver.find_element(By.ID, "lastname").send_keys("User")
    driver.find_element(By.ID, "email").send_keys("testuser_mismatch@example.com")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "confirmpassword").send_keys("differentPassword999")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-red-600")))
    assert error.text.strip() != "", "An error must appear when passwords do not match"


def test_18_register_invalid_email_shows_error(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.ID, "name"))).send_keys("Test")
    driver.find_element(By.ID, "lastname").send_keys("User")
    driver.find_element(By.ID, "email").send_keys("not-a-valid-email")
    driver.find_element(By.ID, "password").send_keys("password123")
    driver.find_element(By.ID, "confirmpassword").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-red-600")))
    assert error.text.strip() != "", "An error must appear for an invalid e-mail during registration"


def test_19_shop_page_loads(driver):
    driver.get(f"{BASE_URL}/shop")
    assert driver.title != "", "Shop page must have a non-empty title"
    assert "error" not in driver.title.lower(), "Shop page must not show an error title"


def test_20_nonexistent_route_shows_404(driver):
    driver.get(f"{BASE_URL}/this-route-does-not-exist-xyz-99999")
    page_source = driver.page_source.lower()
    assert "404" in page_source or "not found" in page_source, \
        "A 404 or Not-Found indicator must appear for non-existent routes"
