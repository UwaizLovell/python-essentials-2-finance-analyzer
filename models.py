class Transaction:
    # Class variable shared by all Transaction objects
    total_transactions = 0

    def __init__(self, date, description, amount, category):
        # Store the transaction information as instance variables
        self.date = date
        self.description = description
        self.amount = amount
        self.category = category

        # Increase the transaction count whenever a new object is created
        Transaction.total_transactions += 1

    def __str__(self):
        # Return a clean, readable description of the transaction
        return f"{self.date} | {self.description} | {self.amount:.2f} | {self.category}"

    def is_income(self):
        # Return True when the transaction amount is positive
        return self.amount > 0

    def formatted(self):
        # Return the transaction in a simple financial statement format
        return f"{self.date} {self.description} {self.amount:.2f} {self.category}"

    