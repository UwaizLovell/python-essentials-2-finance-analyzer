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

class RecurringTransaction(Transaction):
    # Create a recurring transaction with an additional interval
    def __init__(self, date, description, amount, category, interval):
        # Use the parent class constructor for the main transaction details
        super().__init__(date, description, amount, category)

        # Store the recurring interval as an instance variable
        self.interval = interval

    def __str__(self):
        # Override the parent string method to include the recurring interval
        return (
            f"{self.date} | {self.description} | "
            f"{self.amount:.2f} | {self.category} | "
            f"Recurring: {self.interval}"
        )
    