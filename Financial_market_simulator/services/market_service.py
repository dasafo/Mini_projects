import random
from models.database import session, StockPriceDB

class MarketService:
    def __init__(self):
        self.prices = {stock.symbol: stock.price for stock in session.query(StockPriceDB).all()}
        self.market_trend = random.choice(['bullish', 'bearish', 'neutral'])  # Tendencia del mercado
        self.correlations = {
            'AAPL': ['MSFT', 'GOOGL'],  # Correlaciones positivas
            'AMZN': ['NFLX'],
            'TSLA': ['NVDA'],
        }
        self.sentiment_events = [
            {"description": "Lanzamiento de un nuevo producto exitoso", "impact": 1.05, "type": "positive"},
            {"description": "Problemas regulatorios", "impact": 0.95, "type": "negative"},
            {"description": "Crisis económica en sector", "impact": 0.90, "type": "negative"},
            {"description": "Aumento en la demanda de productos", "impact": 1.10, "type": "positive"},
        ]

    def set_initial_price(self, symbol, price):
        stock = session.query(StockPriceDB).filter_by(symbol=symbol).first()
        if not stock:
            stock = StockPriceDB(symbol=symbol, price=price)
            session.add(stock)
        else:
            stock.price = price
        session.commit()
        self.prices[symbol] = price

    def get_price(self, symbol):
        if symbol not in self.prices:
            raise ValueError("El símbolo no existe en el mercado.")
        return self.prices[symbol]

    def simulate_market(self):
        trend_factor = 1.0
        if self.market_trend == 'bullish':
            trend_factor = random.uniform(1.01, 1.05)  # Mercado alcista
        elif self.market_trend == 'bearish':
            trend_factor = random.uniform(0.95, 0.99)  # Mercado bajista

        for symbol in self.prices:
            # Fluctuación de precios influenciada por la tendencia del mercado
            daily_fluctuation = random.uniform(0.98, 1.02)
            new_price = self.prices[symbol] * daily_fluctuation * trend_factor

            # Aplicar correlaciones positivas
            if symbol in self.correlations:
                for correlated_symbol in self.correlations[symbol]:
                    correlated_fluctuation = random.uniform(0.99, 1.01)  # Variación menor en correlación
                    self.prices[correlated_symbol] *= correlated_fluctuation

            self.prices[symbol] = new_price

            # Simular un evento de sentimiento con una pequeña probabilidad
            if random.random() < 0.05:  # 5% de probabilidad de un evento
                event = random.choice(self.sentiment_events)
                self.prices[symbol] *= event["impact"]
                print(f"Evento '{event['description']}' impacta {symbol}: Nuevo precio {self.prices[symbol]:.2f}")

            # Actualizar precio en la base de datos
            stock = session.query(StockPriceDB).filter_by(symbol=symbol).first()
            stock.price = self.prices[symbol]
        session.commit()
