# user.py

class User:
    def __init__(self, name, user_id, email):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.borrowed_items = []

    def borrow_item(self, item):
        self.borrowed_items.append(item)

    def return_item(self, item):
        self.borrowed_items.remove(item)

    def __str__(self):
        return f"User: {self.name}, ID: {self.user_id}, Email: {self.email}, Borrowed Items: {[str(item) for item in self.borrowed_items]}"
