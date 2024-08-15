# user.py

class User:
    def __init__(self, name, user_id, email, role='user'):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.borrowed_items = []
        self.loan_history = []  # Nuevo atributo para almacenar el historial de préstamos
        self.role = role

    def borrow_item(self, item):
        self.borrowed_items.append(item)
        self.loan_history.append(loan)  # Registrar el préstamo en el historial

    def return_item(self, item):
        self.borrowed_items.remove(item)

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