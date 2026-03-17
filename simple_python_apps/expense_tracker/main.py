def add_expense(expenses):
    category = input("Enter category: ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount!")
        return

    expense = {
        "category": category,
        "amount": amount
    }

    expenses.append(expense)
    print("Expense added!")


def show_expenses(expenses):
    if not expenses:
        print("No expenses found")
        return

    print("\n--- All Expenses ---")
    for exp in expenses:
        print(f"{exp['category']} - {exp['amount']}")


def total_spent(expenses):
    total = sum(exp["amount"] for exp in expenses)
    print(f"\nTotal spent: {total}")


def highest_expense(expenses):
    if not expenses:
        print("No expenses found")
        return

    highest = max(expenses, key=lambda x: x["amount"])
    print(f"\nHighest expense: {highest['category']} - {highest['amount']}")


def filter_by_category(expenses):
    category = input("Enter category to filter: ")

    filtered = [exp for exp in expenses if exp["category"] == category]

    if not filtered:
        print("No expenses found for this category")
        return

    print(f"\n--- Expenses for {category} ---")
    for exp in filtered:
        print(f"{exp['amount']}")

def group_by_category(expenses):
    summary = {}

    for exp in expenses:
        category = exp["category"]
        amount = exp["amount"]

        if category in summary:
            summary[category] += amount
        else:
            summary[category] = amount

    print("\n--- Expense Summary ---")
    for category, total in summary.items():
        print(f"{category} - {total}")

def main():
    expenses = []

    while True:
        print("\n1. Add Expense")
        print("2. Show Expenses")
        print("3. Total Spent")
        print("4. Highest Expense")
        print("5. Filter by Category")
        print("6. Grouped Summary")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice not in ["1", "2", "3", "4", "5", "6", "7"]:
            print("Please enter a valid option (1-7)")
            continue

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            show_expenses(expenses)
        elif choice == "3":
            total_spent(expenses)
        elif choice == "4":
            highest_expense(expenses)
        elif choice == "5":
            filter_by_category(expenses)
        elif choice == "6":
            group_by_category(expenses)
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()