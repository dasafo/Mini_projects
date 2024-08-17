class User:
    def __init__(self, user_id, name, capital):
        self.user_id = user_id
        self.name = name
        self.capital = capital
        self.portfolio = {} # Key=shares symbol, Value=shares amount
        
    def buy_stock(self, symbol, quantity, price):
        total_cost = quantity * price
        if total_cost > self.capital:
            raise ValueError("You don't have enough money for this stock purchase.")
        
        self.capital -= total_cost
        
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity
            
    def sell_stock(self, symbol, quantity, price):
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError("You don't have enough stocks to sell.")
        self.portfolio[symbol] -= quantity
        self.capital -= quantity * price
    
    def __str__(self):
        return f"User({self.name}, Capital: {self.capital}, Portfolio: {self.portfolio})"
            
        