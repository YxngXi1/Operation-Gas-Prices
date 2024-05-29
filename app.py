from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    prices = [2.50, 2.55, 2.60]  # Example data
    average_price = sum(prices) / len(prices)
    return render_template('index.html', prices=prices, average_price=average_price)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
