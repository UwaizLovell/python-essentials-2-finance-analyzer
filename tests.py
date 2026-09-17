from models import (
    Transaction,
    RecurringTransaction,
    TransferTransaction
)
from parser import load_transactions
from analytics import (
    running_balance,
    make_flagger,
    find_duplicates,
    find_outliers,
    category_totals
)


def run_tests():
    # Test a valid transaction
    transaction = Transaction(
        "2026-08-01",
        "Groceries",
        -450.50,
        "FOOD"
    )

    assert transaction.date == "2026-08-01", (
        "Valid transaction should keep the correct date"
    )

    assert transaction.amount == -450.50, (
        "Valid transaction should convert amount to float"
    )

    assert transaction.category == "FOOD", (
        "Valid transaction should keep the correct category"
    )

    # Test income detection
    income = Transaction(
        "2026-08-02",
        "Salary",
        15000.00,
        "SALARY"
    )

    assert income.is_income() is True, (
        "Positive amount should be recognised as income"
    )

    assert transaction.is_income() is False, (
        "Negative amount should not be recognised as income"
    )

    # Test parser with the messy sample statement
    transactions, rejections = load_transactions(
        "data/sample_statement.txt"
    )

    # Check that the wrong date separator was normalised
    normalised_date_found = False

    for item in transactions:
        if item.date == "2026-08-03":
            normalised_date_found = True

    assert normalised_date_found is True, (
        "Wrong date separator should be normalised"
    )

    # Check that invalid rows were rejected
    assert len(rejections) == 3, (
        "Three invalid rows should be rejected"
    )

    # Check that the junk line was rejected
    junk_rejection_found = False

    for reason in rejections:
        if "missing or incorrect number of fields" in reason:
            junk_rejection_found = True

    assert junk_rejection_found is True, (
        "Junk line should be rejected safely"
    )

    # Check that the nonnumeric amount was rejected
    amount_rejection_found = False

    for reason in rejections:
        if "could not convert string to float" in reason:
            amount_rejection_found = True

    assert amount_rejection_found is True, (
        "Nonnumeric amount should be rejected"
    )

    # Check that the missing-field row was rejected
    missing_field_rejection_found = False

    for reason in rejections:
        if "missing or incorrect number of fields" in reason:
            missing_field_rejection_found = True

    assert missing_field_rejection_found is True, (
        "Missing fields should be rejected"
    )

    # Test that whitespace was stripped correctly
    whitespace_transaction_found = False

    for item in transactions:
        if (
            item.description == "Groceries"
            and item.amount == -450.50
            and item.category == "FOOD"
        ):
            whitespace_transaction_found = True

    assert whitespace_transaction_found is True, (
        "Whitespace should be stripped from transaction fields"
    )

    # Test missing file handling
    missing_transactions, missing_rejections = load_transactions(
        "data/file_that_does_not_exist.txt"
    )

    assert missing_transactions == [], (
        "Missing file should return an empty transaction list"
    )

    assert len(missing_rejections) == 1, (
        "Missing file should return one rejection reason"
    )

    assert "File not found" in missing_rejections[0], (
        "Missing file should report a clear reason"
    )

    # Test empty file handling
    empty_file_path = "data/empty_test_file.txt"

    with open(empty_file_path, "w") as file:
        file.write("")

    empty_transactions, empty_rejections = load_transactions(
        empty_file_path
    )

    assert empty_transactions == [], (
        "Empty file should return an empty transaction list"
    )

    assert empty_rejections == ["File is empty"], (
        "Empty file should report that the file is empty"
    )

    # Test an additional parser edge case
    # with whitespace, a slash date and a zero amount
    edge_case_path = "data/edge_case_test.txt"

    with open(edge_case_path, "w") as file:
        file.write(
            " 2026/08/15 , Test Transaction , 0.00 , TEST \n"
        )

    edge_transactions, edge_rejections = load_transactions(
        edge_case_path
    )

    # Check that the valid edge-case row was loaded
    assert len(edge_transactions) == 1, (
        "Valid edge-case row should be loaded"
    )

    # Check that the slash date was normalised
    assert edge_transactions[0].date == "2026-08-15", (
        "Slash date should be normalised to the required format"
    )

    # Check that whitespace was removed from the description
    assert edge_transactions[0].description == "Test Transaction", (
        "Extra whitespace should be removed from the description"
    )

    # Check that whitespace was removed from the category
    assert edge_transactions[0].category == "TEST", (
        "Extra whitespace should be removed from the category"
    )

    # Check that zero was converted to a float
    assert edge_transactions[0].amount == 0.0, (
        "Zero amount should be converted to float"
    )

    # Check that the valid edge-case row was not rejected
    assert edge_rejections == [], (
        "Valid edge-case row should not be rejected"
    )

    # Check zero-income behaviour
    assert edge_transactions[0].is_income() is False, (
        "Zero amount should not be recognised as income"
    )

    # Test running balance
    balance_transactions = [
        Transaction(
            "2026-08-01",
            "Salary",
            1000.00,
            "SALARY"
        ),
        Transaction(
            "2026-08-02",
            "Food",
            -200.00,
            "FOOD"
        ),
        Transaction(
            "2026-08-03",
            "Transport",
            -100.00,
            "TRANSPORT"
        )
    ]

    balances = list(
        running_balance(balance_transactions)
    )

    assert balances == [1000.0, 800.0, 700.0], (
        "Running balance should produce the correct sequence"
    )

    # Test the closure-based flagger
    flagger = make_flagger(1000)

    large_transaction = Transaction(
        "2026-08-04",
        "Large Purchase",
        -5000.00,
        "SHOPPING"
    )

    small_transaction = Transaction(
        "2026-08-05",
        "Coffee",
        -50.00,
        "FOOD"
    )

    assert flagger(large_transaction) is True, (
        "Flagger should flag amounts above the threshold"
    )

    assert flagger(small_transaction) is False, (
        "Flagger should not flag amounts below the threshold"
    )

    # Test exact duplicate detection
    duplicate_transactions = [
        Transaction(
            "2026-08-01",
            "Food",
            -200.00,
            "FOOD"
        ),
        Transaction(
            "2026-08-02",
            "Transport",
            -100.00,
            "TRANSPORT"
        ),
        Transaction(
            "2026-08-01",
            "Food",
            -200.00,
            "FOOD"
        )
    ]

    duplicates = find_duplicates(
        duplicate_transactions
    )

    assert len(duplicates) == 1, (
        "Duplicate detection should find the planted duplicate"
    )

    clean_transactions = [
        Transaction(
            "2026-08-01",
            "Food",
            -200.00,
            "FOOD"
        ),
        Transaction(
            "2026-08-02",
            "Transport",
            -100.00,
            "TRANSPORT"
        )
    ]

    assert find_duplicates(clean_transactions) == [], (
        "Clean transaction list should have no duplicates"
    )

    # Test statistical outlier detection
    outlier_transactions = [
        Transaction("2026-08-01", "Food", -100.00, "FOOD"),
        Transaction("2026-08-02", "Food", -101.00, "FOOD"),
        Transaction("2026-08-03", "Food", -99.00, "FOOD"),
        Transaction("2026-08-04", "Food", -100.00, "FOOD"),
        Transaction("2026-08-05", "Food", -102.00, "FOOD"),
        Transaction("2026-08-06", "Food", -98.00, "FOOD"),
        Transaction("2026-08-07", "Food", -100.00, "FOOD"),
        Transaction("2026-08-08", "Food", -101.00, "FOOD"),
        Transaction("2026-08-09", "Food", -99.00, "FOOD"),
        Transaction(
            "2026-08-10",
            "Large Purchase",
            -10000.00,
            "SHOPPING"
        )
    ]

    outliers = find_outliers(
        outlier_transactions
    )

    assert len(outliers) == 1, (
        "Outlier detection should find the planted outlier"
    )

    assert outliers[0].amount == -10000.00, (
        "The large transaction should be identified as the outlier"
    )

    # Test category totals
    category_transactions = [
        Transaction(
            "2026-08-01",
            "Salary",
            15000.00,
            "SALARY"
        ),
        Transaction(
            "2026-08-02",
            "Food",
            -450.00,
            "FOOD"
        ),
        Transaction(
            "2026-08-03",
            "More Food",
            -250.00,
            "FOOD"
        ),
        Transaction(
            "2026-08-04",
            "Transport",
            -300.00,
            "TRANSPORT"
        )
    ]

    totals = category_totals(
        category_transactions
    )

    assert totals["income"]["SALARY"] == 15000.00, (
        "Income total should be correct"
    )

    assert totals["expense"]["FOOD"] == -700.00, (
        "Food expense total should be correct"
    )

    assert totals["expense"]["TRANSPORT"] == -300.00, (
        "Transport expense total should be correct"
    )

    # Test the RecurringTransaction subclass
    recurring = RecurringTransaction(
        "2026-08-01",
        "Rent",
        -8000.00,
        "HOUSING",
        "Monthly"
    )

    assert recurring.interval == "Monthly", (
        "Recurring transaction should store its interval"
    )

    assert recurring.is_income() is False, (
        "Negative recurring transaction should not be income"
    )

    # Test the TransferTransaction subclass
    transfer = TransferTransaction(
        "2026-08-15",
        "Bank Transfer",
        -1000.00,
        "TRANSFER",
        "Savings"
    )

    assert transfer.transfer_account == "Savings", (
        "Transfer transaction should store the transfer account"
    )

    assert transfer.amount == -1000.00, (
        "Transfer transaction should keep the correct amount"
    )

    assert transfer.is_income() is False, (
        "Negative transfer transaction should not be income"
    )

    transfer_text = str(transfer)

    assert "Transfer: Savings" in transfer_text, (
        "Transfer transaction string should include the transfer account"
    )

    print("All tests passed")


if __name__ == "__main__":
    run_tests()

