# Define the base class Material, which will represent general material (e.g., books, magazines).
class Material:
    def __init__(self, title, author, year, categories=None):
        self.title = title
        self.author = author
        self.year = year
        self.categories = categories if categories else []

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}, Categories: {', '.join(self.categories)}"

# Define a subclass of Material called Book, which represents a book and adds specific attributes like ISBN and genre.
class Book(Material):
    def __init__(self, title, author, year, isbn, genre, categories=None):
        super().__init__(title, author, year, categories)
        self.isbn = isbn
        self.genre = genre
        if genre not in self.categories:
            self.categories.append(genre)

    def __str__(self):
        return super().__str__() + f", ISBN: {self.isbn}, Genre: {self.genre}"

# Define a subclass of Material called Magazine, which represents a magazine and adds a specific attribute for issue number.
class Magazine(Material):
    def __init__(self, title, author, year, issue_number, categories=None):
        super().__init__(title, author, year, categories)
        self.issue_number = issue_number

    def __str__(self):
        return super().__str__() + f", Issue: {self.issue_number}"
