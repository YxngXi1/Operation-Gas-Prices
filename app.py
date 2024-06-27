from flask import Flask, render_template, jsonify, request, session
import requests
from flask_session import Session
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

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key= 'b4f+P(XRM3OESCkht?4{'

@app.route('/')
def index():
    prices = [2.50, 2.55, 2.60]  # Example data
    average_price = sum(prices) / len(prices)
    return render_template('index.html', prices=prices, average_price=average_price)

@app.route('/yourinfo')
def yourinfo():
    return render_template('yourinfo.html')
    
@app.route('/save_address', methods=['POST'])
def save_address():
    # Assuming the client sends data as JSON
    data = request.get_json()
    if not data or 'address' not in data:
        return jsonify({'error': 'Address is missing'}), 400
    
    address = data['address']
    session['address'] = address  # Save the address to the session
    print(address)
    return jsonify({'message': 'Address saved successfully'})

@app.route('/gasinfo', methods=['GET', 'POST'])
def gasinfo():
    return render_template('gasinfo.html')


@app.route('/calculation')
def calculation():
    return render_template('calculation.html')

@app.route('/scrape')
def scrape():
    print('time to scrape')
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

    user_address = session.get('address', 'Default Address')
    url = f"https://www.gasbuddy.com/home?search={user_address}&fuel=1&method=all&maxAge=0"

    driver.get(url)

    # Wait for the element to be loaded
    wait = WebDriverWait(driver, 10)
    prices = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'StationDisplayPrice-module__price___3rARL')))
    locations = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'StationDisplay-module__address___2_c7v')))
        
    distances_prices = []

    # Scraping loop
    for price, location in zip(prices, locations):
        inner_html = location.get_attribute('innerHTML')
        full_address = inner_html.replace('<br>', ', ')
        price_text = price.text.strip('$')  # Assuming the price is prefixed with a dollar sign

        # Create a dictionary for the current location and price
        current_data = {
            'location': full_address,
            'price': price_text,
        }

        # Check if the location already exists in the distances_costs list
        location_exists = False
        for entry in distances_prices:
            if entry['location'] == full_address:
                # Update this entry with new cost information or handle duplicates as needed
                entry['cost'] = price_text
                location_exists = True
                break  # Assuming only one entry per location; remove if handling duplicates

        # If the location does not exist, add the new entry
        if not location_exists:
            distances_prices.append(current_data)

    # At this point, distances_costs contains all your scraped data along with any existing data

    # Print updated distances_costs for verification
    print(distances_prices)
        
    session['distances_prices'] = distances_prices
    
    driver.quit()
    
    return jsonify({'message': 'done scraping'})

@app.route('/results')
def results():
    distances_prices = session.get('distances_prices', [])  # Default to an empty list if not found
    
    sort_by = request.args.get('sort', 'default')  # Get the sort parameter from the URL, default to 'default'
    
    if sort_by == 'price_asc':
        sorted_data = sorted(distances_prices, key=lambda x: x['price'])  # Ensure price is treated as a float for sorting
    elif sort_by == 'price_dsc':
        sorted_data = sorted(distances_prices, key=lambda x: x['price'], reverse=True)  # Ensure price is treated as a float for sorting
    else:
        sorted_data = distances_prices

    return render_template('results.html', locations_prices=sorted_data)
    

if __name__ == '__main__':
    app.run(debug=True)