from models.database import session, UserDB, PortfolioItemDB

class User:
    def __init__(self, user_id=None, name=None, capital=None):
        if user_id:
            # If a user ID is provided, fetch the user from the database
            self.db_user = session.query(UserDB).filter_by(id=user_id).first()
        elif name:
            # If a name is provided, create a new user with the given name and capital
            # The ID will be assigned automatically by the database
            self.db_user = UserDB(name=name, capital=capital)
            session.add(self.db_user)
            session.commit()  # This will assign the ID automatically
            # Re-fetch the user to ensure we have the complete user data, including the ID
            self.db_user = session.query(UserDB).filter_by(id=self.db_user.id).first()
        else:
            # Raise an error if neither user_id nor name is provided
            raise ValueError("Must provide either `user_id` or `name` to create a user.")

        # Initialize the user's attributes with data from the database
        self.name = self.db_user.name
        self.capital = self.db_user.capital
        # Create a portfolio dictionary from the user's portfolio items in the database
        self.portfolio = {item.symbol: item.quantity for item in self.db_user.portfolio}

    def buy_stock(self, symbol, quantity, price):
        # Calculate the total cost of the purchase
        total_cost = quantity * price
        # Check if the user has enough capital to make the purchase
        if total_cost > self.capital:
            raise ValueError("You don't have enough money!.")
        # Deduct the total cost from the user's capital
        self.capital -= total_cost
        self.db_user.capital = self.capital

        # Update the user's portfolio with the purchased stock
        if symbol in self.portfolio:
            self.portfolio[symbol] += quantity
        else:
            self.portfolio[symbol] = quantity

        # Check if the portfolio item exists in the database
        portfolio_item = session.query(PortfolioItemDB).filter_by(user_id=self.db_user.id, symbol=symbol).first()
        if portfolio_item:
            # If the item exists, update the quantity
            portfolio_item.quantity = self.portfolio[symbol]
        else:
            # If the item doesn't exist, create a new portfolio item
            portfolio_item = PortfolioItemDB(user_id=self.db_user.id, symbol=symbol, quantity=self.portfolio[symbol])
            session.add(portfolio_item)

        # Commit the changes to the database
        session.commit()

    def sell_stock(self, symbol, quantity, price):
        # Check if the user has enough shares to sell
        if symbol not in self.portfolio or self.portfolio[symbol] < quantity:
            raise ValueError("You don't have enough shares to sell!")
        # Deduct the sold quantity from the portfolio
        self.portfolio[symbol] -= quantity
        # Add the proceeds from the sale to the user's capital
        self.capital += quantity * price
        self.db_user.capital = self.capital

        # Fetch the portfolio item from the database
        portfolio_item = session.query(PortfolioItemDB).filter_by(user_id=self.db_user.id, symbol=symbol).first()
        # Update the quantity in the database
        portfolio_item.quantity = self.portfolio[symbol]
        # If the quantity is zero, remove the portfolio item from the database
        if self.portfolio[symbol] == 0:
            session.delete(portfolio_item)

        # Commit the changes to the database
        session.commit()

    def __str__(self):
        # Return a string representation of the user
        return f"User({self.name}, Capital: {self.capital}, Portfolio: {self.portfolio})"

    @staticmethod
    def get_all_users():
        # Fetch all users from the database
        users_db = session.query(UserDB).all()
        # Create a list of User objects for each user in the database
        users = [User(user_id=user.id) for user in users_db]
        return users
