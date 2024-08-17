from models.database import session, UserDB, PortfolioItemDB

class User:
    def __init__(self, user_id=None, name=None, capital=None):
        if user_id:
            self.db_user = session.query(UserDB).filter_by(id=user_id).first()
        elif name:
            # Create a new user and let the database assign the ID automatically
            self.db_user = UserDB(name=name, capital=capital)
            session.add(self.db_user)
            session.commit()  # This will assign the ID automatically
            self.db_user = session.query(UserDB).filter_by(id=self.db_user.id).first()
        else:
            raise ValueError("Must provide either `user_id` or `name` to create a user.")

        self.name = self.db_user.name
        self.capital = self.db_user.capital
        self.portfolio = {item.symbol: item.quantity for item in self.db_user.portfolio}

    def buy_stock(self, symbol, quantity, price):
        total_cost = quantity * price
        if total_cost > self.capital:
            raise ValueError("No tienes suficiente capital para esta compra.")
        self.capital -= total_cost
        self.db_user.capital = self.capital

        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity

        portfolio_item = session.query(PortfolioItemDB).filter_by(user_id=self.db_user.id, symbol=symbol).first()
        if portfolio_item:
            portfolio_item.quantity = self.portfolio[symbol]
        else:
            portfolio_item = PortfolioItemDB(user_id=self.db_user.id, symbol=symbol, quantity=self.portfolio[symbol])
            session.add(portfolio_item)

        session.commit()

    def sell_stock(self, symbol, quantity, price):
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError("No tienes suficientes acciones para vender.")
        self.portfolio[symbol] -= quantity
        self.capital += quantity * price
        self.db_user.capital = self.capital

        portfolio_item = session.query(PortfolioItemDB).filter_by(user_id=self.db_user.id, symbol=symbol).first()
        portfolio_item.quantity = self.portfolio[symbol]
        if self.portfolio[symbol] == 0:
            session.delete(portfolio_item)

        session.commit()

    def __str__(self):
        return f"User({self.name}, Capital: {self.capital}, Portfolio: {self.portfolio})"

    @staticmethod
    def get_all_users():
        users_db = session.query(UserDB).all()
        users = [User(user_id=user.id) for user in users_db]
        return users
