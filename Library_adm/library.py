from material import Book, Magazine
from user import User
from loan import Loan
import json
import csv
import smtplib
from email.mime.text import MIMEText

class Library:
    def __init__(self):
        # Initialize lists to store materials, users, and loans in the library.
        self.materials = []
        self.users = []
        self.loans = []

    def add_material(self, material, user):
        # Check if the user has permission to add materials to the library.
        if user.has_permission('add_material'):
            # Add the material to the library's collection.
            self.materials.append(material)
            print(f"Material '{material.title}' added to the library by {user.name}.")
        else:
            print(f"User '{user.name}' does not have permission to add materials.")

    def add_user(self, new_user, admin_user):
        # Check if the admin user has permission to add new users.
        if admin_user.has_permission('add_user'):
            # Add the new user to the library's user list.
            self.users.append(new_user)
            print(f"User '{new_user.name}' added to the library by {admin_user.name}.")
        else:
            print(f"User '{admin_user.name}' does not have permission to add users.")

    def lend_material(self, user_id, material_title, loan_duration=30):
        # Find the user by their ID.
        user = next((u for u in self.users if u.user_id == user_id), None)
        # Check if the user exists and has permission to borrow materials.
        if user and user.has_permission('borrow'):
            # Find the material by its title.
            material = next((m for m in self.materials if m.title == material_title), None)
            if material:
                # Create a loan for the material and add it to the loan list.
                loan = Loan(user, material, loan_duration)
                self.loans.append(loan)
                # Add the material to the user's borrowed items.
                user.borrow_item(material, loan_duration)
                print(f"Material '{material.title}' lent to '{user.name}'.")
            else:
                print("Material not found.")
        else:
            print("User not found or does not have permission to borrow materials.")

    def remove_material(self, material_title, user):
        # Check if the user has permission to remove materials from the library.
        if user.has_permission('remove_material'):
            # Find the material by its title.
            material = next((m for m in self.materials if m.title == material_title), None)
            if material:
                # Remove the material from the library's collection.
                self.materials.remove(material)
                print(f"Material '{material.title}' removed by {user.name}.")
            else:
                print(f"Material '{material_title}' not found.")
        else:
            print(f"User '{user.name}' does not have permission to remove materials.")

    def return_material(self, user_id, material_title):
        # Find the loan that matches the user ID and material title, and check if it's not already returned.
        loan = next((l for l in self.loans if l.user.user_id == user_id and l.material.title == material_title and not l.returned), None)        
        if loan:
            # Mark the loan as returned.
            loan.return_item()
            # Remove the material from the user's borrowed items.
            loan.user.return_item(loan.material)
            print(f"Material '{material_title}' returned by '{loan.user.name}'.")
        else:
            print("Loan not found or already returned.")

    def search_materials(self, keyword=None, category=None):
        results = []
        if keyword:
            # Search for materials by keyword in the title or author.
            results = [m for m in self.materials if keyword.lower() in m.title.lower() or keyword.lower() in m.author.lower()]
        if category:
            # Search for materials by category.
            results = [m for m in self.materials if category.lower() in (cat.lower() for cat in m.categories)]
        
        if results:
            print("Search Results:")
            for material in results:
                # Print each material found in the search.
                print(material)
        else:
            print("No materials found.")

    def list_overdue_loans(self):
        # Find all loans that are overdue and not yet returned.
        overdue_loans = [loan for loan in self.loans if loan.is_overdue() and not loan.returned]
        if overdue_loans:
            print("Overdue Loans:")
            for loan in overdue_loans:
                # Print each overdue loan.
                print(loan)
        else:
            print("No overdue loans.")
            
    def save_to_json(self, file_path):
        # Prepare the data for JSON serialization by converting objects to dictionaries.
        data = {
            "materials" : [material.__dict__ for material in self.materials],
            "users" : [user.__dict__ for user in self.users],
            "loans" : [loan.__dict__ for loan in self.loans]
        }
        # Save the data to a JSON file.
        with open(file_path, 'w') as file:
            json.dump(data, file, indent = 4)
            
    def load_from_json(self, file_path):
        # Load the data from a JSON file.
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Recreate the materials, users, and loans from the loaded data.
            self.materials = [Book(**item) if "isbn" in item else Magazine(**item) for item in data["materials"]]
            self.users = [User(**item) for item in data["users"]]
            self.loans = [Loan(
                User(**item["user"]), 
                Book(**item["material"]) if "isbn" in item["material"] else Magazine(**item["material"]), 
                loan_duration=30) 
                for item in data["loans"]]
    
    def save_to_csv(self, materials_path, users_path, loans_path):
        # Save materials to a CSV file.
        with open(materials_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author", "Year", "ISBN", "Genre/Issue"])
            for material in self.materials:
                if isinstance(material, Book):
                    # Write book details to the CSV.
                    writer.writerow([material.title, material.author, material.year, material.isbn, material.genre])
                elif isinstance(material, Magazine):
                    # Write magazine details to the CSV.
                    writer.writerow([material.title, material.author, material.year, "", material.issue_number])

        # Save users to a CSV file.
        with open(users_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "User ID", "Email"])
            for user in self.users:
                # Write user details to the CSV.
                writer.writerow([user.name, user.user_id, user.email])

        # Save loans to a CSV file.
        with open(loans_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Material", "Loan Date", "Due Date", "Returned"])
            for loan in self.loans:
                # Write loan details to the CSV.
                writer.writerow([loan.user.name, loan.material.title, loan.loan_date, loan.due_date, loan.returned])

    def load_from_csv(self, materials_path, users_path, loans_path):
        # Load materials from a CSV file.
        with open(materials_path, 'r') as file:
            reader = csv.DictReader(file)
            self.materials = []
            for row in reader:
                if row["ISBN"]:
                    # Create a book from the CSV data and add it to materials.
                    self.materials.append(Book(row["Title"], row["Author"], row["Year"], row["ISBN"], row["Genre/Issue"]))
                else:
                    # Create a magazine from the CSV data and add it to materials.
                    self.materials.append(Magazine(row["Title"], row["Author"], row["Year"], row["Genre/Issue"]))

        # Load users from a CSV file.
        with open(users_path, 'r') as file:
            reader = csv.DictReader(file)
            self.users = [User(row["Name"], row["User ID"], row["Email"]) for row in reader]

        # Load loans from a CSV file.
        with open(loans_path, 'r') as file:
            reader = csv.DictReader(file)
            self.loans = []
            for row in reader:
                # Find the corresponding user and material for each loan.
                user = next((u for u in self.users if u.name == row["User"]), None)
                material = next((m for m in self.materials if m.title == row["Material"]), None)
                loan = Loan(user, material, loan_duration=30)
                # Set the loan dates and return status from the CSV data.
                loan.loan_date = row["Loan Date"]
                loan.due_date = row["Due Date"]
                loan.returned = row["Returned"] == 'True'
                # Add the loan to the list of loans.
                self.loans.append(loan)
                
    def send_due_soon_notifications(self, days_before=3):
        # Send notifications for loans that are due soon.
        for loan in self.loans:
            if loan.is_due_soon(days_before) and not loan.returned:
                # Send an email notification to the user.
                self.send_email_notification(loan.user, loan)

    def send_email_notification(self, user, loan):
        # Basic email configuration.
        sender = "your_email@example.com"
        receiver = user.email
        subject = f"Préstamo próximo a vencer: {loan.material.title}"
        body = (f"Hola {user.name},\n\nEl material '{loan.material.title}' que has prestado "
                f"está próximo a vencer el {loan.due_date.strftime('%Y-%m-%d')}.\n\n"
                "Por favor, realiza la devolución antes de la fecha límite.\n\nGracias.")

        # Create the email message.
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # Send the email.
        try:
            with smtplib.SMTP('smtp.example.com') as server:
                server.login("your_email@example.com", "your_password")
                server.sendmail(sender, [receiver], msg.as_string())
                print(f"Notification sent to {user.email}")
        except Exception as e:
            print(f"Error sending notification: {e}")       
                 
    def view_user_loan_history(self, user_id):
        # Find the user by their ID.
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user:
            if user.loan_history:
                # Print the user's loan history.
                print(f"Loan History for {user.name}:")
                for loan in user.loan_history:
                    print(loan)
            else:
                print(f"No loan history for {user.name}.")
        else:
            print("User not found.")

"""
# Example usage:
if __name__ == "__main__":
    library = Library()
    
    # Create user with admin role.
    admin_user = User("Admin", "A001", "admin@example.com", role='admin')
    normal_user = User("User", "U001", "user@example.com", role='user')
    
    # Add materials to the library.
    book1 = Book("1984", "George Orwell", 1949, "978-0451524935", "Dystopian", ["Classic", "Political"])
    book2 = Book("Animal Farm", "George Orwell", 1945, "978-0451526342", "Political Satire")
    magazine1 = Magazine("National Geographic", "Various", 2023, "August", ["Science", "Photography"])

    library.add_material(book1, admin_user)
    library.add_material(book2, admin_user)  # Changed to admin_user to reflect permissions
    library.add_material(magazine1, admin_user)  # Changed to admin_user to reflect permissions

    # Add users to the library.
    user1 = User("Alice Smith", "U001", "alice@example.com")
    library.add_user(user1, admin_user)  # Added admin_user to reflect permissions

    library.add_user(normal_user, admin_user)
    
    # Lend a material to a user.
    library.lend_material("U001", "1984")

    # Attempt to remove a material with normal user (should fail).
    library.remove_material("1984", normal_user)
    # Remove a material with admin user (should succeed).
    library.remove_material("1984", admin_user)
    
    # Lend another material.
    library.lend_material("U001", "1984")

    # Search for materials by keyword.
    library.search_materials("George")

    # List all overdue loans.
    library.list_overdue_loans()

    # Return a material to the library.
    library.return_material("U001", "1984")
    
    # Send notifications for loans that are due soon.
    library.send_due_soon_notifications()
    
    # View the loan history for a user.
    library.view_user_loan_history("U001")
"""