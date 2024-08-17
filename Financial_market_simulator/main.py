from models.user import User
from services.market_service import MarketService

# User create
user = User(1, "Matias", 10000)

# Create a marketplace service and set up initial market prices
market = MarketService()
market.set_initial_price('AAPL', 150)
market.set_initial_price('GOOGL', 2800)

print(f"Initial price AAPL: {market.get_price('AAPL')}")
print(f"Initial price GOOGL: {market.get_price('GOOGL')}")

# Simulate stock purchase
user.buy_stock('AAPL', 10, market.get_price('AAPL'))
user.buy_stock('GOOGL', 2, market.get_price('GOOGL'))

print(user)

# Simulate the market (price fluctuation)
market.simulate_market()

# Show prices after simulation
print(f"Price after AAPL simulation: {market.get_price('AAPL')}.")
print(f"Price after GOOGL simulation: {market.get_price('GOOGL')}.")

# Simulate the sale of shares
user.sell_stock('AAPL', 5, market.get_price("AAPL"))
print(user)
