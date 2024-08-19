import random
from models.database import session, StockPriceDB

class MarketService:
    def __init__(self):
        # Initialize a dictionary of current stock prices from the database
        self.prices = {stock.symbol: stock.price for stock in session.query(StockPriceDB).all()}
        # Randomly choose the market trend (bullish, bearish, or neutral)
        self.market_trend = random.choice(['bullish', 'bearish', 'neutral'])
        # Define correlations between stocks that typically move together
        self.correlations = {
            'AAPL': ['MSFT', 'GOOGL'],  # Positive correlations
            'AMZN': ['NFLX'],
            'TSLA': ['NVDA'],
        }
        # Define sentiment events that can positively or negatively impact stock prices
        self.sentiment_events = [
            {"description": "Launch of a successful new product", "impact": 1.05, "type": "positive"},
            {"description": "Regulatory problems", "impact": 0.95, "type": "negative"},
            {"description": "Economic crisis in sector", "impact": 0.90, "type": "negative"},
            {"description": "Increased product demand", "impact": 1.10, "type": "positive"},
        ]

    def set_initial_price(self, symbol, price):
        # Fetch a stock from the database by its symbol
        stock = session.query(StockPriceDB).filter_by(symbol=symbol).first()
        if not stock:
            # If the stock doesn't exist, create a new entry in the database
            stock = StockPriceDB(symbol=symbol, price=price)
            session.add(stock)
        else:
            # If it exists, update the price
            stock.price = price
        session.commit()  # Save changes to the database
        self.prices[symbol] = price  # Update the local prices dictionary

    def get_price(self, symbol):
        # Check if the symbol exists in the prices dictionary
        if symbol not in self.prices:
            raise ValueError("Symbol doesn't exist in Market.")
        return self.prices[symbol]  # Return the current price of the stock

    def simulate_market(self):
        trend_factor = 1.0
        # Adjust the trend factor based on the current market trend
        if self.market_trend == 'bullish':
            trend_factor = random.uniform(1.01, 1.05)  # Bullish market effect
        elif self.market_trend == 'bearish':
            trend_factor = random.uniform(0.95, 0.99)  # Bearish market effect

        for symbol in self.prices:
            # Simulate daily price fluctuation influenced by the market trend
            daily_fluctuation = random.uniform(0.98, 1.02)
            new_price = self.prices[symbol] * daily_fluctuation * trend_factor

            # Apply positive correlations if the symbol has correlated stocks
            if symbol in self.correlations:
                for correlated_symbol in self.correlations[symbol]:
                    correlated_fluctuation = random.uniform(0.99, 1.01)  # Smaller fluctuation for correlated stocks
                    self.prices[correlated_symbol] *= correlated_fluctuation

            self.prices[symbol] = new_price  # Update the stock's price

            # Simulate a sentiment event with a 5% probability
            if random.random() < 0.05:
                event = random.choice(self.sentiment_events)
                self.prices[symbol] *= event["impact"]  # Apply the event's impact on the stock price
                print(f"Event '{event['description']}' impact {symbol}: New price {self.prices[symbol]:.2f}")

            # Update the stock price in the database
            stock = session.query(StockPriceDB).filter_by(symbol=symbol).first()
            stock.price = self.prices[symbol]
        session.commit()  # Save all price updates to the database
