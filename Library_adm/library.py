from material import Book, Magazine
from user import User
from loan import Loan
import json
import csv
import smtplib
from email.mime.text import MIMEText

class Library:
    def __init__(self):
        self.materials = []
        self.users = []
        self.loans = []

    def add_material(self, material, user):
        if user.has_permission('add_material'):
            self.materials.append(material)
            print(f"Material '{material.title}' added to the library by {user.name}.")
        else:
            print(f"User '{user.name}' does not have permission to add materials.")

    def add_user(self, new_user, admin_user):
        if admin_user.has_permission('add_user'):
            self.users.append(new_user)
            print(f"User '{new_user.name}' added to the library by {admin_user.name}.")
        else:
            print(f"User '{admin_user.name}' does not have permission to add users.")

    def lend_material(self, user_id, material_title, loan_duration=30):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user and user.has_permission('borrow'):
            material = next((m for m in self.materials if m.title == material_title), None)
            if material:
                loan = Loan(user, material, loan_duration)
                self.loans.append(loan)
                user.borrow_item(material, loan_duration)
                print(f"Material '{material.title}' lent to '{user.name}'.")
            else:
                raise ValueError(f"Material '{material_title}' not found.")
        else:
            raise ValueError("User not found or does not have permission to borrow materials.")

    def remove_material(self, material_title, user):
        if user.has_permission('remove_material'):
            material = next((m for m in self.materials if m.title == material_title), None)
            if material:
                self.materials.remove(material)
                print(f"Material '{material.title}' removed by {user.name}.")
            else:
                raise ValueError(f"Material '{material_title}' not found.")
        else:
            raise ValueError(f"User '{user.name}' does not have permission to remove materials.")

    def return_material(self, user_id, material_title):
        loan = next((l for l in self.loans if l.user.user_id == user_id and l.material.title == material_title and not l.returned), None)
        if loan:
            loan.return_item()
            loan.user.return_item(loan.material)
            print(f"Material '{material_title}' returned by '{loan.user.name}'.")
        else:
            raise ValueError(f"Loan for material '{material_title}' not found or already returned.")

    def search_materials(self, keyword=None, category=None):
        results = []
        if keyword:
            results = [m for m in self.materials if keyword.lower() in m.title.lower() or keyword.lower() in m.author.lower()]
        if category:
            results = [m for m in self.materials if category.lower() in (cat.lower() for cat in m.categories)]
        
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
            
    def save_to_json(self, file_path):
        data = {
            "materials" : [material.__dict__ for material in self.materials],
            "users" : [user.__dict__ for user in self.users],
            "loans" : [loan.__dict__ for loan in self.loans]
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent = 4)
            
    def load_from_json(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.materials = [Book(**item) if "isbn" in item else Magazine(**item) for item in data["materials"]]
            self.users = [User(**item) for item in data["users"]]
            self.loans = [Loan(
                User(**item["user"]), 
                Book(**item["material"]) if "isbn" in item["material"] else Magazine(**item["material"]), 
                loan_duration=30) 
                for item in data["loans"]]
    
    def save_to_csv(self, materials_path, users_path, loans_path):
        with open(materials_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Author", "Year", "ISBN", "Genre/Issue"])
            for material in self.materials:
                if isinstance(material, Book):
                    writer.writerow([material.title, material.author, material.year, material.isbn, material.genre])
                elif isinstance(material, Magazine):
                    writer.writerow([material.title, material.author, material.year, "", material.issue_number])

        with open(users_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "User ID", "Email"])
            for user in self.users:
                writer.writerow([user.name, user.user_id, user.email])

        with open(loans_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Material", "Loan Date", "Due Date", "Returned"])
            for loan in self.loans:
                writer.writerow([loan.user.name, loan.material.title, loan.loan_date, loan.due_date, loan.returned])

    def load_from_csv(self, materials_path, users_path, loans_path):
        with open(materials_path, 'r') as file:
            reader = csv.DictReader(file)
            self.materials = []
            for row in reader:
                if row["ISBN"]:
                    self.materials.append(Book(row["Title"], row["Author"], row["Year"], row["ISBN"], row["Genre/Issue"]))
                else:
                    self.materials.append(Magazine(row["Title"], row["Author"], row["Year"], row["Genre/Issue"]))

        with open(users_path, 'r') as file:
            reader = csv.DictReader(file)
            self.users = [User(row["Name"], row["User ID"], row["Email"]) for row in reader]

        with open(loans_path, 'r') as file:
            reader = csv.DictReader(file)
            self.loans = []
            for row in reader:
                user = next((u for u in self.users if u.name == row["User"]), None)
                material = next((m for m in self.materials if m.title == row["Material"]), None)
                loan = Loan(user, material, loan_duration=30)
                loan.loan_date = row["Loan Date"]
                loan.due_date = row["Due Date"]
                loan.returned = row["Returned"] == 'True'
                self.loans.append(loan)
                
    def send_due_soon_notifications(self, days_before=3):
        for loan in self.loans:
            if loan.is_due_soon(days_before) and not loan.returned:
                self.send_email_notification(loan.user, loan)

    def send_email_notification(self, user, loan):
        sender = "your_email@example.com"
        receiver = user.email
        subject = f"Loan is about to expire: {loan.material.title}"
        body = (f"Hi {user.name},\n\nThe material '{loan.material.title}' you have loaned "
                f"is about to expire on the {loan.due_date.strftime('%Y-%m-%d')}.\n\n"
                "Please make the return before the deadline.\n\nThanks!")

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        try:
            with smtplib.SMTP('smtp.example.com') as server:
                server.login("your_email@example.com", "your_password")
                server.sendmail(sender, [receiver], msg.as_string())
                print(f"Notification sent to {user.email}")
        except Exception as e:
            print(f"Error sending notification: {e}")       
                 
    def view_user_loan_history(self, user_id):
        user = next((u for u in self.users if u.user_id == user_id), None)
        if user:
            if user.loan_history:
                print(f"Loan History for {user.name}:")
                for loan in user.loan_history:
                    print(loan)
            else:
                print(f"No loan history for {user.name}.")
        else:
            raise ValueError("User not found.")
