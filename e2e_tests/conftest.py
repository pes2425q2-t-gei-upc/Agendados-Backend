import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="class")
def chrome_driver(request):
    # Set up Chrome options for headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Use Chrome directly from the Docker container
    options.binary_location = "/usr/bin/google-chrome"

    # Create driver without using webdriver_manager
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    # Make driver available to the test
    request.cls.driver = driver

    # Return driver for the test method
    yield driver

    # Cleanup after test finishes
    driver.quit()