import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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
    service = Service("/usr/bin/chromedriver")
    d = webdriver.Chrome(service=service, options=options)
    d.implicitly_wait(10)
    yield d
    d.quit()


def find_error_message(driver, wait):
    """
    Try multiple selectors that a Next.js / Tailwind app might use for
    validation errors. Returns the error element if found, else None.
    Also handles HTML5 browser-native validation via JS validity API.
    """
    selectors = [
        "p.text-red-600",
        "p.text-red-500",
        "span.text-red-600",
        "span.text-red-500",
        "[role='alert']",
        ".error-message",
        ".text-red-600",
        ".text-red-500",
        "p[class*='red']",
        "span[class*='red']",
        "div[class*='error']",
    ]
    for sel in selectors:
        try:
            el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, sel)))
            if el and el.text.strip():
                return el
        except TimeoutException:
            pass
    return None


def has_html5_validation_error(driver, field_id):
    """Check if a field has a browser-native HTML5 validation error."""
    return driver.execute_script(
        f"var el = document.getElementById('{field_id}'); "
        "return el ? !el.validity.valid : false;"
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_01_homepage_loads(driver):
    driver.get(BASE_URL)
    assert driver.title != ""
    assert "error" not in driver.title.lower()


def test_02_homepage_has_content(driver):
    driver.get(BASE_URL)
    assert len(driver.page_source) > 200


def test_03_login_page_loads(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    assert field.is_displayed()


def test_04_login_email_field_type(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    assert field.get_attribute("type") == "email"


def test_05_login_password_field_type(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    assert field.get_attribute("type") == "password"


def test_06_login_remember_me_checkbox(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    cb = wait.until(EC.presence_of_element_located((By.ID, "remember-me")))
    assert cb.get_attribute("type") == "checkbox"


def test_07_login_submit_button_exists(driver):
    driver.get(f"{BASE_URL}/login")
    wait = WebDriverWait(driver, 15)
    btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    assert btn.is_displayed()


def test_08_register_page_loads(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    assert field.is_displayed()


def test_09_register_name_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "name")))
    assert field.get_attribute("type") == "text"


def test_10_register_lastname_field_exists(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "lastname")))
    assert field.is_displayed()


def test_11_register_email_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    assert field.get_attribute("type") == "email"


def test_12_register_password_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "password")))
    assert field.get_attribute("type") == "password"


def test_13_register_confirmpassword_field_type(driver):
    driver.get(f"{BASE_URL}/register")
    wait = WebDriverWait(driver, 15)
    field = wait.until(EC.presence_of_element_located((By.ID, "confirmpassword")))
    assert field.get_attribute("type") == "password"


def test_14_shop_page_loads(driver):
    driver.get(f"{BASE_URL}/shop")
    assert driver.title != ""
    assert "error" not in driver.title.lower()


def test_15_nonexistent_route_shows_404(driver):
    driver.get(f"{BASE_URL}/this-route-does-not-exist-xyz-99999")
    page_source = driver.page_source.lower()
    assert "404" in page_source or "not found" in page_source
