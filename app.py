from flask import Flask, render_template
from flask import request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    prices = [2.50, 2.55, 2.60]  # Example data
    average_price = sum(prices) / len(prices)
    return render_template('index.html', prices=prices, average_price=average_price)

@app.route('/yourinfo')
def yourinfo():
    
    return render_template('yourinfo.html')

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
        
    user_input = 'L5M 5Y5'
    
    # Send a request to the target site with the user's input
    # This example assumes you're sending the input as a query parameter
    response = requests.get(f"https://www.gasbuddy.com/home?search={user_input}&fuel=1&method=all&maxAge=0")
    
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Scrape the data you need from the site
    # This is a placeholder; you'll need to adjust it based on the site's structure
    scraped_data = soup.find_all('span', class_='text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL')
    print(scraped_data)
    
    return render_template('results.html', distances_costs=sorted_data)
    

if __name__ == '__main__':
    app.run(debug=True)