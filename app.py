from flask import Flask, render_template, jsonify, request, session
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

app = Flask(__name__)
app.secret_key = 'iuahsdu2h98ajdisubah@9qhwduha'

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
    if request.method == 'POST':
        # This is where you can handle the new value of the knob
        # For example, you can store it in a database
        new_value = request.form.get('knob_value')
        print(new_value)  # Just for testing
    return render_template('gasinfo.html')


@app.route('/calculation')
def calculation():
    return render_template('calculation.html')

@app.route('/results')
def results():
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

    for price in prices:
        print(price.text)
        
    for location in locations:
        inner_html = location.get_attribute('innerHTML')
        full_address = inner_html.replace('<br>', ' ')
        print(location.text)
    
    
    sort_by = request.args.get('sort', 'default')  # Get the sort parameter from the URL, default to 'default'
    
    # Using a list of dictionaries to handle duplicate location names and additional data
    distances_costs = [
        {'location': 'Hamilton', 'distance': 90, 'cost': 3},
        {'location': 'Toronto', 'distance': 30, 'cost': 10},
        {'location': 'Mississauga', 'distance': 40, 'cost': 1},
        {'location': 'Kingston', 'distance': 20, 'cost': 8},
        {'location': 'Hamilton', 'distance': 50, 'cost': 6},
        {'location': 'Niagra', 'distance': 60, 'cost': 9},
        {'location': 'Vancouver', 'distance': 100, 'cost': 7},
        {'location': 'Waterloo', 'distance': 80, 'cost': 4},
        {'location': 'Brampton', 'distance': 10, 'cost': 5},
        {'location': 'Hamilton', 'distance': 70, 'cost': 2}
    ]
    
    if sort_by == 'distance':
        sorted_data = sorted(distances_costs, key=lambda x: x['distance'])
    elif sort_by == 'cost':
        sorted_data = sorted(distances_costs, key=lambda x: x['cost'])
    else:
        sorted_data = distances_costs  # Default to unsorted
        
    driver.quit()
    
    return render_template('results.html', distances_costs=sorted_data)
    

if __name__ == '__main__':
    app.run(debug=True)