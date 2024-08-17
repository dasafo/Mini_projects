from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Define a base class for our ORM models
Base = declarative_base()

# Define the UserDB class which maps to the 'users' table
class UserDB(Base):
    __tablename__ = 'users'  # Specify the table name
    id = Column(Integer, primary_key=True)  # Define an integer primary key column
    name = Column(String)  # Define a string column for the user's name
    capital = Column(Float)  # Define a float column for the user's capital
    portfolio = relationship("PortfolioItemDB", back_populates="user")  # Define a relationship to the PortfolioItemDB class

# Define the PortfolioItemDB class which maps to the 'portfolio_items' table
class PortfolioItemDB(Base):
    __tablename__ = 'portfolio_items'  # Specify the table name
    id = Column(Integer, primary_key=True)  # Define an integer primary key column
    user_id = Column(Integer, ForeignKey('users.id'))  # Define a foreign key column referencing the 'users' table
    symbol = Column(String)  # Define a string column for the stock symbol
    quantity = Column(Integer)  # Define an integer column for the quantity of stocks
    user = relationship("UserDB", back_populates="portfolio")  # Define a relationship back to the UserDB class

# Define the StockPriceDB class which maps to the 'stock_prices' table
class StockPriceDB(Base):
    __tablename__ = 'stock_prices'  # Specify the table name
    id = Column(Integer, primary_key=True)  # Define an integer primary key column
    symbol = Column(String, unique=True)  # Define a string column for the stock symbol, ensuring it is unique
    price = Column(Float)  # Define a float column for the stock price

# Define the connection string to connect to the PostgreSQL database
DATABASE_URL = "postgresql+psycopg2://postgres:freedom85@localhost/financial_simulator"

# Create an engine object that manages the connection pool and database connections
engine = create_engine(DATABASE_URL)

# Create all tables in the database based on the ORM models
Base.metadata.create_all(engine)

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a session object that manages transactions with the database
session = Session()
