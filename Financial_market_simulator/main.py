from models.user import User
from services.market_service import MarketService

# Función para inicializar el mercado con precios iniciales de varias acciones
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

# Menú de la interfaz CLI
def show_menu():
    print("\n--- Simulador de Mercado Financiero ---")
    print("1. Crear nuevo usuario")
    print("2. Seleccionar usuario")
    print("3. Ver precios de acciones")
    print("4. Comprar acciones")
    print("5. Vender acciones")
    print("6. Ver cartera")
    print("7. Simular mercado")
    print("8. Salir")

# Manejar la elección del usuario en la CLI
def handle_user_choice(choice, users, active_user, market):
    if choice == 1:
        # Create a new user
        name = input("Enter the new user's name: ")
        capital = float(input("Enter the initial capital for the user: "))
        new_user = User(name=name, capital=capital)
        users.append(new_user)
        print(f"User {name} created successfully.")
    elif choice == 2:
        # Select an existing user
        if not users:
            print("No users available. Please create a new user first.")
        else:
            print("\nAvailable users:")
            for idx, user in enumerate(users):
                print(f"{idx + 1}. {user.name}")
            try:
                selected_idx = int(input("Select a user by number: ")) - 1
                if 0 <= selected_idx < len(users):
                    active_user = users[selected_idx]
                    print(f"User {active_user.name} selected.")
                else:
                    print("Invalid selection. Please choose a valid user number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    elif choice == 3:
        # View current stock prices
        print("\nCurrent market prices:")
        for symbol in market.prices:
            print(f"{symbol}: {market.get_price(symbol):.2f}")
    elif choice == 4:
        # Buy stocks for the selected user
        if not active_user:
            print("You must select a user first.")
        else:
            symbol = input("Enter the stock symbol to buy: ")
            quantity = int(input("Enter the quantity to buy: "))
            price = market.get_price(symbol)
            active_user.buy_stock(symbol, quantity, price)
            print(f"{active_user.name} bought {quantity} shares of {symbol} at {price:.2f} each.")
    elif choice == 5:
        # Sell stocks for the selected user
        if not active_user:
            print("You must select a user first.")
        else:
            symbol = input("Enter the stock symbol to sell: ")
            quantity = int(input("Enter the quantity to sell: "))
            price = market.get_price(symbol)
            active_user.sell_stock(symbol, quantity, price)
            print(f"{active_user.name} sold {quantity} shares of {symbol} at {price:.2f} each.")
    elif choice == 6:
        # View the selected user's portfolio
        if not active_user:
            print("You must select a user first.")
        else:
            print(f"\n{active_user.name}'s Portfolio:")
            print(active_user)
    elif choice == 7:
        # Simulate the market to adjust stock prices
        market.simulate_market()
        print("The market has been simulated.")
    elif choice == 8:
        # Exit the application
        return False, active_user
    return True, active_user


# Punto de entrada de la aplicación
def main():
    # Inicializar mercado
    market = MarketService()
    initialize_market(market)

    # Cargar usuarios desde la base de datos
    users = User.get_all_users()
    active_user = None

    # Interfaz de usuario CLI
    running = True
    while running:
        show_menu()
        choice = int(input("Elige una opción: "))
        running, active_user = handle_user_choice(choice, users, active_user, market)

if __name__ == "__main__":
    main()
