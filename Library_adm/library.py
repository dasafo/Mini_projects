# library.py
from material import Book, Magazine
from user import User
from loan import Loan

class Library:
    def __init__(self):
        self.materials = []
        self.users = []
        self.loans = []

    def add_material(self, material):
        self.materials.append(material)
        print(f"Material '{material.title}' added to the library.")

    def add_user(self, user):
        self.users.append(user)
        print(f"User '{user.name}' added to the library.")

    def lend_material(self, user_id, material_title, loan_duration=14):
        user = next((u for u in self.users if u.user_id == user_id), None)
        material = next((m for m in self.materials if m.title == material_title), None)
        
        if user and material:
            loan = Loan(user, material, loan_duration)
            self.loans.append(loan)
            user.borrow_item(material)
            print(f"Material '{material.title}' lent to '{user.name}'.")
        else:
            print("User or material not found.")

    def return_material(self, user_id, material_title):
        loan = next((l for l in self.loans if l.user.user_id == user_id and l.material.title == material_title and not l.returned), None)
        
        if loan:
            loan.return_item()
            loan.user.return_item(loan.material)
            print(f"Material '{material_title}' returned by '{loan.user.name}'.")
        else:
            print("Loan not found or already returned.")

    def search_materials(self, keyword):
        results = [m for m in self.materials if keyword.lower() in m.title.lower() or keyword.lower() in m.author.lower()]
        if results:
            print("Search Results:")
            for material in results:
                print(material)
        else:
            print("No materials found.")

    def list_overdue_loans(self):
        overdue_loans = [loan for loan in self.loans if loan.is_overdue() and not loan.returned]
        if overdue_loans:
            print("Overdue Loans:")
            for loan in overdue_loans:
                print(loan)
        else:
            print("No overdue loans.")

# Example usage:
if __name__ == "__main__":
    library = Library()

    # Add materials
    book1 = Book("1984", "George Orwell", 1949, "978-0451524935", "Dystopian")
    magazine1 = Magazine("National Geographic", "Various", 2023, "August")

    library.add_material(book1)
    library.add_material(magazine1)

    # Add users
    user1 = User("Alice Smith", "U001", "alice@example.com")
    library.add_user(user1)

    # Lend material
    library.lend_material("U001", "1984")

    # Search materials
    library.search_materials("George")

    # List overdue loans
    library.list_overdue_loans()

    # Return material
    library.return_material("U001", "1984")
