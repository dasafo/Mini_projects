# loan.py
from datetime import datetime, timedelta
from material import Book, Magazine
from user import User

class Loan:
    def __init__(self, user, material, loan_duration=30):
        self.user = user
        self.material = material
        self.loan_date = datetime.now()
        self.due_date = self.loan_date + timedelta(days=loan_duration)
        self.returned = False

    def return_item(self):
        self.returned = True

    def is_overdue(self):
        return datetime.now() > self.due_date
    
    def days_until_due(self):
        return (self.due_date - datetime.now()).days

    def is_due_soon(self, days_before=3):
        return 0 < self.days_until_due() <= days_before

    def __str__(self):
        return (f"Loan - User: {self.user.name}, Material: {self.material.title}, "
                f"Loan Date: {self.loan_date.strftime('%Y-%m-%d')}, "
                f"Due Date: {self.due_date.strftime('%Y-%m-%d')}, "
                f"Returned: {'Yes' if self.returned else 'No'}")
