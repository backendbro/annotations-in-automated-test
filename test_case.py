import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Chrome
from typing import Tuple

@pytest.fixture(scope="module")
def browser():
    # Set up browser instance
    options = Options()
    options.add_argument("--start-maximized")  # Maximize window on start
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    # Teardown browser instance

    driver.quit()

def test_login(browser:Chrome) -> None:
        
    # Open the webpage
    browser.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # username, password and button elements 
    username_input: Tuple[str, str]  = (By.XPATH, "//input[@name='username']")
    password_input: Tuple[str, str]  = (By.XPATH, "//input[@name='password']")
    login_button: Tuple[str, str]  = (By.XPATH, "//button")
    
    username:str = "Admin"
    password:str = "admin123"
    
    # Find the username and password input fields and login button
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(username_input)).send_keys(username)
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(password_input)).send_keys(password)

    # Click login button
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(login_button)).click()

    # Wait for the dashboard page to load
    WebDriverWait(browser, 10).until(EC.title_contains("OrangeHRM"))

    # Verify that we are on the dashboard page after login
    assert "dashboard" in browser.current_url.lower()
    


@pytest.mark.parametrize("password, msg", [("admin123", "maintenance"), ("admin12", "auth")])
def test_maintenance(browser, password, msg) -> None:
    main_ele = (By.XPATH, "//ul[@class='oxd-main-menu']/li[10]")  
    password_ele = (By.NAME, "password")

    btn_submit = (By.XPATH, "//button[@type='submit' and contains(@class, 'oxd-button')]")

    # Find the maintenance tab and password input fields and login button
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(main_ele)).click()
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(password_ele)).send_keys(password)
    
    WebDriverWait(browser, 10).until(EC.visibility_of_element_located(btn_submit)).click()

    # Wait for the dashboard page to load
    WebDriverWait(browser, 10).until(EC.title_contains("OrangeHRM"))

    # Verify that we are on the dashboard page after login
    assert msg in browser.current_url.lower()
        
