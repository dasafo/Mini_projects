import tkinter as tk
from tkinter import messagebox, simpledialog
from library import Library
from material import Book, Magazine
from user import User

class LibraryApp:
    def __init__(self, root):
        self.library = Library()
        self.root = root
        self.root.title("Library Management System")

        # Menú principal
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        # Menú de Materiales
        material_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Materials", menu=material_menu)
        material_menu.add_command(label="Add Book", command=self.add_book)
        material_menu.add_command(label="Add Magazine", command=self.add_magazine)
        material_menu.add_command(label="List Materials", command=self.list_materials)

        # Menú de Usuarios
        user_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Users", menu=user_menu)
        user_menu.add_command(label="Add User", command=self.add_user)
        user_menu.add_command(label="List Users", command=self.list_users)

        # Menú de Préstamos
        loan_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Loans", menu=loan_menu)
        loan_menu.add_command(label="Lend Material", command=self.lend_material)
        loan_menu.add_command(label="Return Material", command=self.return_material)
        loan_menu.add_command(label="View Loan History", command=self.view_loan_history)

        # Cuadro de texto para mostrar resultados
        self.text_area = tk.Text(root, wrap='word')
        self.text_area.pack(expand=True, fill='both')

    def add_book(self):
        title = simpledialog.askstring("Input", "Enter book title:")
        author = simpledialog.askstring("Input", "Enter book author:")
        year = simpledialog.askinteger("Input", "Enter publication year:")
        isbn = simpledialog.askstring("Input", "Enter ISBN:")
        genre = simpledialog.askstring("Input", "Enter genre:")
        if title and author and year and isbn and genre:
            book = Book(title, author, year, isbn, genre)
            self.library.add_material(book, admin_user)
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")

    def add_magazine(self):
        title = simpledialog.askstring("Input", "Enter magazine title:")
        author = simpledialog.askstring("Input", "Enter magazine author:")
        year = simpledialog.askinteger("Input", "Enter publication year:")
        issue_number = simpledialog.askstring("Input", "Enter issue number:")
        if title and author and year and issue_number:
            magazine = Magazine(title, author, year, issue_number)
            self.library.add_material(magazine, admin_user)
            messagebox.showinfo("Success", f"Magazine '{title}' added successfully!")

    def list_materials(self):
        self.text_area.delete(1.0, tk.END)
        if self.library.materials:
            self.text_area.insert(tk.END, "Materials in Library:\n")
            for material in self.library.materials:
                self.text_area.insert(tk.END, str(material) + "\n")
        else:
            self.text_area.insert(tk.END, "No materials found.")

    def add_user(self):
        name = simpledialog.askstring("Input", "Enter user name:")
        user_id = simpledialog.askstring("Input", "Enter user ID:")
        email = simpledialog.askstring("Input", "Enter user email:")
        role = simpledialog.askstring("Input", "Enter role (admin/user):", initialvalue="user")
        if name and user_id and email:
            user = User(name, user_id, email, role=role)
            self.library.add_user(user, admin_user)
            messagebox.showinfo("Success", f"User '{name}' added successfully!")

    def list_users(self):
        self.text_area.delete(1.0, tk.END)
        if self.library.users:
            self.text_area.insert(tk.END, "Users in Library:\n")
            for user in self.library.users:
                self.text_area.insert(tk.END, str(user) + "\n")
        else:
            self.text_area.insert(tk.END, "No users found.")

    def lend_material(self):
        user_id = simpledialog.askstring("Input", "Enter user ID:")
        material_title = simpledialog.askstring("Input", "Enter material title:")
        if user_id and material_title:
            self.library.lend_material(user_id, material_title)
            messagebox.showinfo("Success", f"Material '{material_title}' lent successfully!")

    def return_material(self):
        user_id = simpledialog.askstring("Input", "Enter user ID:")
        material_title = simpledialog.askstring("Input", "Enter material title:")
        if user_id and material_title:
            self.library.return_material(user_id, material_title)
            messagebox.showinfo("Success", f"Material '{material_title}' returned successfully!")

    def view_loan_history(self):
        user_id = simpledialog.askstring("Input", "Enter user ID to view loan history:")
        if user_id:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, f"Loan History for User ID '{user_id}':\n")
            self.library.view_user_loan_history(user_id)

# Ejecución de la aplicación
if __name__ == "__main__":
    admin_user = User("Admin", "A001", "admin@example.com", role='admin')
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
