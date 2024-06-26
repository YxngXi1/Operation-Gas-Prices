from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Function to initialize the driver based on the browser choice
def init_driver(browser_choice):
    if browser_choice.lower() == 'firefox':
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    elif browser_choice.lower() == 'edge':
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
    else:
        # Default to Chrome if no valid option is provided
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Example usage
browser_choice = 'chrome'  # This could be dynamically set by the user
driver = init_driver(browser_choice)

user_input = 'L5M 5Y5'
url = f"https://www.gasbuddy.com/home?search={user_input}&fuel=1&method=all&maxAge=0"

driver.get(url)

# Wait for the element to be loaded
wait = WebDriverWait(driver, 10)
elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'StationDisplayPrice-module__price___3rARL')))

for element in elements:
    print(element.text)

driver.quit()