from flask import Flask, render_template
from flask import request

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
    
    distances_locations = [(90, 'Hamilton'), (30, 'Toronto'), (40, 'Mississauga'), (20, 'Kingston'), (50, 'London'), (60, 'Niagra'), (100, 'Vancouver'), (80, 'Waterloo'), (10, 'Brampton'), (70, 'Markham')]
    
    if sort_by == 'location':
        sorted_data = sorted(distances_locations, key=lambda x: x[1])
    elif sort_by == 'distance':
        sorted_data = sorted(distances_locations, key=lambda x: x[0])
    else:
        sorted_data = distances_locations
    
    return render_template('results.html', distances_locations=sorted_data)
    

if __name__ == '__main__':
    app.run(debug=True)