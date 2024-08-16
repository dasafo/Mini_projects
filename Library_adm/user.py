class User:
    def __init__(self, name, user_id, email, role='user'):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.borrowed_items = []
        self.loan_history = []
        self.role = role

    def borrow_item(self, item, loan_duration=30):
        self.borrowed_items.append(item)
        from loan import Loan

        loan = Loan(user=self, material=item, loan_duration=loan_duration)
        self.loan_history.append(loan)

    def return_item(self, item):
        if item in self.borrowed_items:
            self.borrowed_items.remove(item)
        else:
            raise ValueError(f"Item '{item.title}' not found in borrowed items.")

        for loan in self.loan_history:
            if loan.material == item and not loan.returned:
                loan.return_item()
                break

    def has_permission(self, action):
        if self.role == 'admin':
            return True
        elif self.role == 'user' and action in ['borrow', 'return', 'view']:
            return True
        return False

    def __str__(self):
        return (f"User: {self.name}, ID: {self.user_id}, Email: {self.email}, "
                f"Role: {self.role}, Borrowed Items: {[str(item) for item in self.borrowed_items]}, "
                f"Loan History: {[str(loan) for loan in self.loan_history]}")
