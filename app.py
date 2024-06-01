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
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)