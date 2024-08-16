# Define the base class Material, which will represent general material (e.g., books, magazines).
class Material:
    def __init__(self, title, author, year, categories=None):
        # Initialize the Material object with a title, author, year, and optional categories.
        self.title = title
        self.author = author
        self.year = year
        # If no categories are provided, initialize an empty list; otherwise, use the provided list.
        self.categories = categories if categories else []

    def __str__(self):
        # Return a string representation of the Material object, listing its title, author, year, and categories.
        return f"Title: {self.title}, Author: {self.author}, Year: {self.year}, Categories: {', '.join(self.categories)}"

# Define a subclass of Material called Book, which represents a book and adds specific attributes like ISBN and genre.
class Book(Material):
    def __init__(self, title, author, year, isbn, genre, categories=None):
        # Initialize the Book object using the constructor of the Material class, passing title, author, year, and categories.
        super().__init__(title, author, year, categories)
        # Add specific attributes for the Book: ISBN and genre.
        self.isbn = isbn
        self.genre = genre
        # If the genre is not already in the categories list, add it to the list.
        if genre not in self.categories:
            self.categories.append(genre)

    def __str__(self):
        # Return a string representation of the Book object, including all attributes from Material and adding ISBN and genre.
        return super().__str__() + f", ISBN: {self.isbn}, Genre: {self.genre}"

# Define a subclass of Material called Magazine, which represents a magazine and adds a specific attribute for issue number.
class Magazine(Material):
    def __init__(self, title, author, year, issue_number, categories=None):
        # Initialize the Magazine object using the constructor of the Material class, passing title, author, year, and categories.
        super().__init__(title, author, year, categories)
        # Add a specific attribute for the Magazine: issue number.
        self.issue_number = issue_number

    def __str__(self):
        # Return a string representation of the Magazine object, including all attributes from Material and adding the issue number.
        return super().__str__() + f", Issue: {self.issue_number}"
