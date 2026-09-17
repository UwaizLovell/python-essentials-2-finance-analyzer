import os
import platform
from datetime import datetime

from analytics import category_totals, find_duplicates, find_outliers


def monthly_summary(
    transactions,
    rejection_reasons=None,
    duplicates=None,
    outliers=None
):
    # Use empty lists when no rejection or analysis results are supplied
    if rejection_reasons is None:
        rejection_reasons = []

    if duplicates is None:
        duplicates = find_duplicates(transactions)

    if outliers is None:
        outliers = find_outliers(transactions)

    # Calculate income and expense totals
    income_total = sum(
        transaction.amount
        for transaction in transactions
        if transaction.is_income()
    )

    expense_total = sum(
        transaction.amount
        for transaction in transactions
        if not transaction.is_income()
    )

    # Get the category totals from the analytics module
    totals = category_totals(transactions)

    # Create the data directory if it does not already exist
    os.makedirs("data", exist_ok=True)

    # Write the monthly summary report
    with open("data/report.txt", "w") as file:
        file.write("===== MONTHLY FINANCE SUMMARY =====\n")
        file.write(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        )
        file.write(f"System: {platform.system()}\n")
        file.write(f"Python: {platform.python_version()}\n\n")

        file.write(f"Total income: {income_total:.2f}\n")
        file.write(f"Total expenses: {expense_total:.2f}\n")
        file.write(
            f"Net total: {income_total + expense_total:.2f}\n\n"
        )

        file.write("Income by category:\n")
        for category, amount in totals["income"].items():
            file.write(f"  {category}: {amount:.2f}\n")

        file.write("\nExpenses by category:\n")
        for category, amount in totals["expense"].items():
            file.write(f"  {category}: {amount:.2f}\n")

        file.write(
            f"\nRejected rows: {len(rejection_reasons)}\n"
        )

        file.write(
            f"Duplicate transactions: {len(duplicates)}\n"
        )

        file.write(
            f"Outlier transactions: {len(outliers)}\n"
        )

    return "data/report.txt"

def log_run(transaction_count, rejection_count):
    # Create the data directory if it does not already exist
    os.makedirs("data", exist_ok=True)

    # Create a timestamp for this analyzer run
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Append the run information to the log file
    with open("data/analyzer.log", "a") as file:
        file.write(
            f"{timestamp} | "
            f"Transactions: {transaction_count} | "
            f"Rejected: {rejection_count}\n"
        )

    return "data/analyzer.log"

