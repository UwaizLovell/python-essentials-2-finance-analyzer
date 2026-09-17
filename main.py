from models import Transaction
from parser import generate_sample_file, load_transactions
from analytics import (
    running_balance,
    category_totals,
    find_duplicates,
    find_outliers
)
from reporting import monthly_summary, log_run
from tests import run_tests


def show_menu():
    # Display the main finance analyzer menu
    print("\n===== FINANCE TRANSACTION ANALYZER =====")
    print("1. Generate a messy sample statement file")
    print("2. Load & validate transactions (reject bad rows)")
    print("3. Show running balance (ledger)")
    print("4. Category breakdown (income vs expense by tag)")
    print("5. Detect duplicate transactions")
    print("6. Flag unusual transactions (statistical outliers)")
    print("7. Monthly summary report -> file")
    print("8. Run self-tests (tests.py)")
    print("9. Exit")


def main():
    # Keep the loaded transactions available between menu choices
    transactions = []

    # Keep track of rejected rows from the latest file load
    rejection_reasons = []

    # Keep the current statement path in one place
    statement_path = "data/sample_statement.txt"

    while True:
        show_menu()

        try:
            choice = input("Choose an option (1-9): ").strip()

            if choice == "1":
                # Generate the messy sample statement
                generate_sample_file(statement_path)

            elif choice == "2":
                # Load the statement and reject bad rows safely
                transactions, rejection_reasons = load_transactions(
                    statement_path
                )

                print(f"\nValid transactions loaded: {len(transactions)}")
                print(f"Rejected rows: {len(rejection_reasons)}")

                # Display the reason for each rejected row
                if rejection_reasons:
                    print("\nRejection reasons:")

                    for reason in rejection_reasons:
                        print(f"- {reason}")

                # Show any valid transactions that were loaded
                if transactions:
                    print("\nValid transactions:")

                    for transaction in transactions:
                        print(transaction.formatted())

                # Record this analyzer run
                log_run(
                    len(transactions),
                    len(rejection_reasons)
                )

            elif choice == "3":
                # Show the running balance in transaction order
                if not transactions:
                    print("\nNo transactions loaded.")
                else:
                    print("\n===== RUNNING BALANCE =====")

                    balances = running_balance(transactions)

                    for transaction, balance in zip(
                        transactions,
                        balances
                    ):
                        print(
                            f"{transaction.formatted()} "
                            f"| Balance: {balance:.2f}"
                        )

            elif choice == "4":
                # Show income and expense totals by category
                if not transactions:
                    print("\nNo transactions loaded.")
                else:
                    totals = category_totals(transactions)

                    print("\n===== CATEGORY BREAKDOWN =====")

                    print("\nIncome:")
                    if totals["income"]:
                        for category, amount in totals["income"].items():
                            print(f"{category}: {amount:.2f}")
                    else:
                        print("No income transactions.")

                    print("\nExpenses:")
                    if totals["expense"]:
                        for category, amount in totals["expense"].items():
                            print(f"{category}: {amount:.2f}")
                    else:
                        print("No expense transactions.")

            elif choice == "5":
                # Find exact duplicate transactions
                if not transactions:
                    print("\nNo transactions loaded.")
                else:
                    duplicates = find_duplicates(transactions)

                    print("\n===== DUPLICATE TRANSACTIONS =====")
                    print(f"Duplicates found: {len(duplicates)}")

                    for duplicate in duplicates:
                        print(duplicate.formatted())

            elif choice == "6":
                # Find transactions that are more than
                # two standard deviations from the mean
                if not transactions:
                    print("\nNo transactions loaded.")
                else:
                    outliers = find_outliers(transactions)

                    print("\n===== UNUSUAL TRANSACTIONS =====")
                    print(f"Outliers found: {len(outliers)}")

                    for outlier in outliers:
                        print(outlier.formatted())

            elif choice == "7":
                # Generate the monthly summary report
                if not transactions:
                    print("\nNo transactions loaded.")
                else:
                    duplicates = find_duplicates(transactions)
                    outliers = find_outliers(transactions)

                    report_path = monthly_summary(
                        transactions,
                        rejection_reasons,
                        duplicates,
                        outliers
                    )

                    print(f"\nReport created: {report_path}")

            elif choice == "8":
                # Run the complete self-test suite
                print("\n===== RUNNING SELF-TESTS =====")

                try:
                    run_tests()
                except AssertionError as error:
                    print(f"Test failed: {error}")
                except Exception as error:
                    print(f"Test error: {error}")

            elif choice == "9":
                # Exit the menu loop
                print("\nExiting Finance Transaction Analyzer.")
                break

            else:
                # Handle anything outside the valid menu choices
                print("\nPlease choose a number from 1 to 9.")

        except Exception as error:
            # Prevent unexpected user input errors from crashing the menu
            print(f"\nSomething went wrong: {error}")


if __name__ == "__main__":
    main()

