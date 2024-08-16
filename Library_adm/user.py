
class User:
    def __init__(self, name, user_id, email, role='user'):
        # Initialize the User object with the provided name, user_id, email, and role (default is 'user').
        self.name = name
        self.user_id = user_id
        self.email = email
        # Initialize an empty list to track items currently borrowed by the user.
        self.borrowed_items = []
        # Initialize an empty list to store the user's loan history.
        self.loan_history = []
        # Set the user's role (e.g., 'user' or 'admin').
        self.role = role

    def borrow_item(self, item, loan_duration=30):
        # Add the borrowed item to the list of currently borrowed items.
        self.borrowed_items.append(item)
        from loan import Loan

        # Create a new Loan instance for this borrowed item.
        loan = Loan(user=self, material=item, loan_duration=loan_duration)
        # Create a new Loan instance for this borrowed item and add it to the loan history.
        self.loan_history.append(loan)

    def return_item(self, item):
        # Remove the item from the list of currently borrowed items.
        self.borrowed_items.remove(item)
        # Iterate through the loan history to find the corresponding loan and mark it as returned.
        for loan in self.loan_history:
            # Check if the loan corresponds to the item and hasn't been returned yet.
            if loan.material == item and not loan.returned:
                # Mark the loan as returned.
                loan.return_item()
                # Exit the loop once the item is marked as returned.
                break

    def has_permission(self, action):
        # If the user is an admin, they have permission for any action.
        if self.role == 'admin':
            return True
        # If the user is a regular user, they have permission for specific actions.
        elif self.role == 'user' and action in ['borrow', 'return', 'view']:
            return True
        # For any other cases, the user does not have permission.
        return False

    def __str__(self):
        # Return a string representation of the User object, including name, ID, email, role,
        # a list of currently borrowed items, and the loan history.
        return (f"User: {self.name}, ID: {self.user_id}, Email: {self.email}, "
                f"Role: {self.role}, Borrowed Items: {[str(item) for item in self.borrowed_items]}, "
                f"Loan History: {[str(loan) for loan in self.loan_history]}")
