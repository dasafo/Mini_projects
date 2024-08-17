import random
from models.database import session, StockPriceDB

class MarketService:
    def __init__(self):
        # Initialize the MarketService and load all stock prices from the database into a dictionary
        # Key=symbol of the company, Value= current price
        self.prices = {stock.symbol: stock.price for stock in session.query(StockPriceDB).all()} 
        
    def set_initial_price(self, symbol, price):
        # Sets the initial price for a stock symbol, or updates it if the stock already exists in the database
        stock = session.query(StockPriceDB).filter_by(symbol=symbol).first()
        if not stock:
            # If the stock does not exist, create a new StockPriceDB record and add it to the session
            stock = StockPriceDB(symbol=symbol, price=price)
            session.add(stock)
        else:
            # If the stock exists, update the price
            stock.price = price
        # Commit the changes to the database
        session.commit()
        # Update the prices dictionary with the new price
        self.prices[symbol] = price
        
    def get_price(self, symbol):
        # Retrieve the price of a given stock symbol from the prices dictionary
        if symbol not in self.prices:
            # If the symbol does not exist in the dictionary, raise an error
            raise ValueError("This Symbol doesn't exist in the Market.")
        return self.prices[symbol]
    
    def simulate_market(self):
        # Simulates market changes by slightly adjusting the price of each stock
        for symbol in self.prices:
            # Adjust the price randomly within a range of -5% to +5%
            self.prices[symbol] *= random.uniform(0.95, 1.05)
            # Update the stock price in the database to reflect the new simulated price
            stock = session.query(StockPriceDB).filter_by(symbol=symbol).first()
            stock.price = self.prices[symbol]
        # Commit all changes to the database
        session.commit()
