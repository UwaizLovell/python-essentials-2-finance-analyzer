import statistics

def running_balance(transactions, start=0.0):
    # Keep track of the current balance as transactions are processed
    balance = start

    # Process transactions in their original order
    for transaction in transactions:
        balance += transaction.amount

        # Yield the balance after each transaction
        yield balance

def make_flagger(threshold):
    # Remember the threshold inside the returned function
    def flagger(transaction):
        # Flag transactions whose amount magnitude exceeds the threshold
        return abs(transaction.amount) > threshold

    return flagger

def find_duplicates(transactions):
    # Keep track of transaction signatures we have already seen
    seen = set()

    # Store transactions that appear more than once
    duplicates = []

    for transaction in transactions:
        # Use all transaction fields to identify an exact duplicate
        signature = (
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.category
        )

        if signature in seen:
            # This transaction is an exact duplicate
            duplicates.append(transaction)
        else:
            # Remember this transaction for future comparisons
            seen.add(signature)

    return duplicates

def find_outliers(transactions):
    # Return no outliers when there are too few transactions
    if len(transactions) < 2:
        return []

    # Collect all transaction amounts for the statistical calculation
    amounts = [transaction.amount for transaction in transactions]

    # Calculate the mean and standard deviation
    mean = statistics.mean(amounts)
    standard_deviation = statistics.stdev(amounts)

    # Avoid division-style problems when every amount is identical
    if standard_deviation == 0:
        return []

    outliers = []

    for transaction in transactions:
        # Calculate how far the amount is from the mean
        distance_from_mean = abs(transaction.amount - mean)

        # Flag amounts more than 2 standard deviations from the mean
        if distance_from_mean > 2 * standard_deviation:
            outliers.append(transaction)

    return outliers

def category_totals(transactions):
    # Store income and expense totals separately by category
    totals = {
        "income": {},
        "expense": {}
    }

    for transaction in transactions:
        # Positive amounts are treated as income
        if transaction.is_income():
            category = totals["income"]
            category[transaction.category] = (
                category.get(transaction.category, 0.0)
                + transaction.amount
            )

        # Negative amounts are treated as expenses
        else:
            category = totals["expense"]
            category[transaction.category] = (
                category.get(transaction.category, 0.0)
                + transaction.amount
            )

    return totals

