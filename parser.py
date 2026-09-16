from models import Transaction
from datetime import datetime


def generate_sample_file(path):
    # Create a sample statement containing both valid and broken rows
    sample_data = [
        "2026-08-01,Salary,15000.00,SALARY",
        "2026-08-01,Groceries,-450.50,FOOD",
        "2026/08/03,Transport,-120.00,TRANSPORT",
        "2026-08-04,Coffee,-45.00,FOOD",
        "hello world",
        "2026-08-05,Shopping,abc,SHOPPING",
        "2026-08-06,Rent,-8000.00,HOUSING",
        "2026-08-07,Bonus,2500.00,SALARY",
        "2026-08-07,Bonus,2500.00,SALARY",
        "2026-08-08,Electricity,-1200.00,UTILITIES",
        "2026-08-09,Refund,500.00,SHOPPING",
        "2026-08-10,MissingAmount,SHOPPING",
        "2026-08-11, Groceries , -450.50 , FOOD ",
        "",
    ]

    # Write the sample rows into the requested file
    with open(path, "w") as file:
        for row in sample_data:
            file.write(row + "\n")

    print(f"Sample statement created: {path}")

def load_transactions(path):
    # Store valid Transaction objects
    transactions = []

    # Store reasons for rows that could not be loaded
    rejection_reasons = []

    try:
        # Open the statement file for reading
        with open(path, "r") as file:
            # Read all rows so we can detect an empty statement
            lines = file.readlines()

            if not lines:
                rejection_reasons.append("File is empty")

            else:
                # Process each row separately
                for line_number, line in enumerate(lines, start=1):
                    try:
                        # Remove whitespace from the beginning and end
                        line = line.strip()

                        # Ignore completely empty lines
                        if not line:
                            continue

                        # Split the row into its four expected fields
                        parts = line.split(",")

                        # A valid transaction must have exactly four fields
                        if len(parts) != 4:
                            raise ValueError(
                                "missing or incorrect number of fields"
                            )

                        date, description, amount, category = parts

                        # Remove extra whitespace from each field
                        date = date.strip()
                        description = description.strip()
                        amount = amount.strip()
                        category = category.strip()

                        # Normalise dates using either / or - as the separator
                        date = date.replace("/", "-")

                        # Check that the date is a valid date
                        datetime.strptime(date, "%Y-%m-%d")

                        # Convert the amount from text to a float
                        amount = float(amount)

                        # Create a Transaction object from the valid row
                        transaction = Transaction(
                            date,
                            description,
                            amount,
                            category
                        )

                        transactions.append(transaction)

                    except Exception as error:
                        # Reject only the bad row and continue with the next one
                        rejection_reasons.append(
                            f"Line {line_number}: {error}"
                        )

    except FileNotFoundError:
        # Handle a file that does not exist without crashing
        rejection_reasons.append(f"File not found: {path}")

    except Exception as error:
        # Handle any other file-reading problem gracefully
        rejection_reasons.append(f"Could not read file: {error}")

    return transactions, rejection_reasons


