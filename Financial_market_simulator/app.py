from flask import Flask, render_template, request, redirect, url_for, session
from models.user import User
from services.market_service import MarketService
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para la gestión de sesiones

# Función para inicializar el mercado con precios iniciales
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
    for symbol, price in initial_prices.items():
        market_service.set_initial_price(symbol, price)
        
# Lista de colores predefinidos
color_list = [
    '#3498db', # Azul
    '#e74c3c', # Rojo
    '#2ecc71', # Verde
    '#f1c40f', # Amarillo
    '#9b59b6', # Morado
    '#e67e22', # Naranja
    '#1abc9c', # Turquesa
    '#34495e'  # Azul oscuro
]

# Función para asignar colores
def get_color(index):
    if index < len(color_list):
        return color_list[index]
    else:
        # Generar un color aleatorio si se superan los predefinidos
        return f"#{random.randint(0, 0xFFFFFF):06x}"
    

# Inicializar el mercado
market = MarketService()
initialize_market(market)

# Cargar usuarios desde la base de datos
users = User.get_all_users()

@app.route('/')
def index():
    users = User.get_all_users()
    for i, user in enumerate(users):
        user.color = get_color(i)
    return render_template('index.html', users=users)


@app.route('/select_user/<int:user_id>')
def select_user(user_id):
    user = next((user for user in users if user.db_user.id == user_id), None)
    if user:
        session['active_user'] = user_id
        return redirect(url_for('user_options'))
    return redirect(url_for('index'))

@app.route('/user_options')
def user_options():
    if 'active_user' not in session:
        return redirect(url_for('index'))

    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    return render_template('user_options.html', user=user)

@app.route('/view_prices')
def view_prices():
    if 'active_user' not in session:
        return redirect(url_for('index'))
    return render_template('view_prices.html', prices=market.prices)

@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    if 'active_user' not in session:
        return redirect(url_for('index'))

    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    price = market.get_price(symbol)
    user.buy_stock(symbol, quantity, price)
    
    return redirect(url_for('user_options'))

@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    if 'active_user' not in session:
        return redirect(url_for('index'))

    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    symbol = request.form['symbol']
    quantity = int(request.form['quantity'])
    price = market.get_price(symbol)
    user.sell_stock(symbol, quantity, price)
    
    return redirect(url_for('user_options'))

@app.route('/view_portfolio')
def view_portfolio():
    if 'active_user' not in session:
        return redirect(url_for('index'))

    user_id = session['active_user']
    user = next((user for user in users if user.db_user.id == user_id), None)

    return render_template('view_portfolio.html', user=user)

@app.route('/simulate_market')
def simulate_market():
    market.simulate_market()
    return redirect(url_for('user_options'))

@app.route('/create_user', methods=['POST'])
def create_user():
    name = request.form['name']
    capital = float(request.form['capital'])
    new_user = User(name=name, capital=capital)
    users.append(new_user)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True, port = 5001)
