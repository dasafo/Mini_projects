from flask import Flask, render_template, request, redirect, url_for, session
from models.user import User
from services.market_service import MarketService
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

# Function to initialize the market with initial stock prices
def initialize_market(market_service):
    initial_prices = {
        "AAPL": 150,
        "GOOGL": 2800,
        "AMZN": 3500,
        "TSLA": 700,
        "MSFT": 300,
        "FB": 340,
        "NFLX": 550,
        "NVDA": 800,
    }
    # Set initial prices for each stock in the market
    for symbol, price in initial_prices.items():
        market_service.set_initial_price(symbol, price)

# Predefined list of colors
color_list = [
    '#3498db', # Blue
    '#e74c3c', # Red
    '#2ecc71', # Green
    '#f1c40f', # Yellow
    '#9b59b6', # Purple
    '#e67e22', # Orange
    '#1abc9c', # Turquoise
    '#34495e'  # Dark Blue
]

# Function to assign colors
def get_color(index):
    if index < len(color_list):
        return color_list[index]
    else:
        # Generate a random color if the predefined list is exceeded
        return f"#{random.randint(0, 0xFFFFFF):06x}"
    
# Initialize the market
market = MarketService()
initialize_market(market)

# Load users from the database
users = User.get_all_users()

@app.route('/')
def index():
    # Reload users each time the index is accessed
    users = User.get_all_users()
    # Assign a color to each user
    for i, user in enumerate(users):
        user.color = get_color(i)
    # Render the index page with the list of users
    return render_template('index.html', users=users)

@app.route('/select_user/<int:user_id>')
def select_user(user_id):
    # Find the selected user by their ID
    user = next((user for user in users if user.db_user.id == user_id), None)
    if user:
        # Set the selected user as the active user in the session
        session['active_user'] = user_id
        return redirect(url_for('user_options'))
    # If the user isn't found, redirect to the index page
    return redirect(url_for('index'))

@app.route('/user_options')
def user_options():
    # Check if an active user is selected in the session
    if 'active_user' not in session:
        return redirect(url_for('index'))

    # Retrieve the active user from the session
    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    # Render the user options page for the active user
    return render_template('user_options.html', user=user)

@app.route('/view_prices')
def view_prices():
    # Check if an active user is selected in the session
    if 'active_user' not in session:
        return redirect(url_for('index'))
    # Render the view prices page with the current market prices
    return render_template('view_prices.html', prices=market.prices)

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    # Check if an active user is selected in the session
    if 'active_user' not in session:
        return redirect(url_for('index'))

    # Retrieve the active user from the session
    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    # Get the stock symbol and quantity from the form submission
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    # Get the current price of the stock from the market service
    price = market.get_price(symbol)
    # Execute the stock purchase for the user
    user.buy_stock(symbol, quantity, price)
    
    return redirect(url_for('user_options'))

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    # Check if an active user is selected in the session
    if 'active_user' not in session:
        return redirect(url_for('index'))

    # Retrieve the active user from the session
    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    # Get the stock symbol and quantity from the form submission
    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    # Get the current price of the stock from the market service
    price = market.get_price(symbol)
    # Execute the stock sale for the user
    user.sell_stock(symbol, quantity, price)
    
    return redirect(url_for('user_options'))

@app.route('/view_portfolio')
def view_portfolio():
    # Check if an active user is selected in the session
    if 'active_user' not in session:
        return redirect(url_for('index'))

    # Retrieve the active user from the session
    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    # Render the view portfolio page for the active user
    return render_template('view_portfolio.html', user=user)

@app.route('/simulate_market')
def simulate_market():
    # Simulate market fluctuations
    market.simulate_market()
    # Redirect to the user options page after the simulation
    return redirect(url_for('user_options'))

@app.route('/create_user', methods=['POST'])
def create_user():
    # Get the new user's name and initial capital from the form submission
    name = request.form['name']
    capital = float(request.form['capital'])
    # Create a new user and add them to the users list
    new_user = User(name=name, capital=capital)
    users.append(new_user)
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Run the Flask application in debug mode on port 5001
    app.run(debug=True, port=5001)
