from datetime import datetime, timedelta
from material import Book, Magazine
from user import User

# Define the Loan class, which represents a loan of a material (like a book or magazine) by a user.
class Loan:
    def __init__(self, user, material, loan_duration=30):
        # Initialize the Loan object with the user, material being borrowed, and the loan duration (default is 30 days).
        self.user = user
        self.material = material
        # Record the current date and time as the loan date.
        self.loan_date = datetime.now()
        # Calculate the due date by adding the loan duration to the loan date.
        self.due_date = self.loan_date + timedelta(days=loan_duration)
        # A boolean to track whether the item has been returned (initially False).
        self.returned = False

    # Mark the loan as returned.
    def return_item(self):
        self.returned = True

    # Check if the loan is overdue (i.e., if the current date is past the due date).
    def is_overdue(self):
        return datetime.now() > self.due_date
    
    # Calculate the number of days remaining until the due date.
    def days_until_due(self):
        return (self.due_date - datetime.now()).days

    # Check if the loan is due soon, within a specified number of days (default is 3 days).
    def is_due_soon(self, days_before=3):
        return 0 < self.days_until_due() <= days_before

    # Return a string representation of the Loan object, showing details like user name, material title, loan date, due date, and whether it has been returned.
    def __str__(self):
        return (f"Loan - User: {self.user.name}, Material: {self.material.title}, "
                f"Loan Date: {self.loan_date.strftime('%Y-%m-%d')}, "
                f"Due Date: {self.due_date.strftime('%Y-%m-%d')}, "
                f"Returned: {'Yes' if self.returned else 'No'}")
