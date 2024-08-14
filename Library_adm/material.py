# material.py

class Material:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}"

class Book(Material):
    def __init__(self, title, author, year, isbn, genre):
        super().__init__(title, author, year)
        self.isbn = isbn
        self.genre = genre

    def __str__(self):
        return super().__str__() + f", ISBN: {self.isbn}, Genre: {self.genre}"

class Magazine(Material):
    def __init__(self, title, author, year, issue_number):
        super().__init__(title, author, year)
        self.issue_number = issue_number

    def __str__(self):
        return super().__str__() + f", Issue: {self.issue_number}"
