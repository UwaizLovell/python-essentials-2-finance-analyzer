## Personal Finance Transaction Analyzer

A menu-driven Python application that loads, validates and analyses personal finance transactions from a statement file.

The project was built as part of the Melsoft Academy Python Essentials 2 Advanced Challenge.

## Project Features

The analyzer can:

1. Generate a messy sample statement file
2. Load and validate transactions
3. Reject invalid rows without crashing
4. Show a running balance
5. Break transactions down by category
6. Detect exact duplicate transactions
7. Detect unusual transactions using statistical outlier calculations
8. Generate a monthly finance report
9. Run the self-test suite
10. Export valid transactions to CSV

## Defensive Parsing

The sample statement deliberately contains messy and broken data.

The parser handles:

- Wrong date separators such as `2026/08/03`
- Missing fields
- Junk lines
- Nonnumeric amounts
- Duplicate transactions
- Whitespace around fields
- Empty files
- Missing files

Bad rows are rejected individually so that one broken row does not stop the rest of the statement from loading.

The loader returns:

- A list of valid `Transaction` objects
- A list of rejection reasons

## Object Model

The project uses a `Transaction` class containing:

- Date
- Description
- Amount
- Category

The class also includes:

- `__str__()`
- `is_income()`
- `formatted()`
- A class variable counting transactions

Two subclasses are also included:

- `RecurringTransaction`
- `TransferTransaction`

Both subclasses inherit from `Transaction` and add their own information.

## Analytics

The `analytics.py` module provides:

### Running Balance

Uses a generator to calculate the balance after each transaction while keeping the original transaction order.

### Transaction Flagger

Uses a closure to remember a threshold and flag transactions whose amount magnitude exceeds that threshold.

### Duplicate Detection

Uses transaction signatures and a set to identify exact duplicate transactions.

### Outlier Detection

Uses the mean and standard deviation of transaction amounts to identify transactions more than two standard deviations from the mean.

### Category Totals

Separates income and expense totals by category.

## Reporting

The `reporting.py` module creates a monthly summary containing:

- Total income
- Total expenses
- Net total
- Income by category
- Expenses by category
- Rejected row count
- Duplicate count
- Outlier count
- System information
- Python version
- Date and time

Analyzer runs are also recorded in an append-only log.

Valid transactions can additionally be exported to CSV.

## Project Structure

```text
python-essentials-2-finance-analyzer/
|
|-- main.py
|-- models.py
|-- parser.py
|-- analytics.py
|-- reporting.py
|-- tests.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|
|-- data/
    |-- .gitkeep

