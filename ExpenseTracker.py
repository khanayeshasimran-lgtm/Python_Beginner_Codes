import os

FILE_NAME = "expenses.txt"

def add_expense():
    date = input("Enter date (DD-MM-YYYY): ")
    category = input("Enter category (Food, Travel, etc.): ")
    amount = float(input("Enter amount: "))

    with open(FILE_NAME, "a") as file:
        file.write(f"{date},{category},{amount}\n")

    print("Expense added successfully!\n")

def view_expenses():
    if not os.path.exists(FILE_NAME):
        print("\nNo expenses recorded yet.\n")
        return

    total = 0
    print("\n--- Expense History ---")
    with open(FILE_NAME, "r") as file:
        for line in file:
            date, category, amount = line.strip().split(",")
            total += float(amount)
            print(f"Date: {date} | Category: {category} | Amount: ₹{amount}")

    print("----------------------")
    print(f"Total Spent: ₹{total}\n")

def main():
    while True:
        print("=== EXPENSE TRACKER ===")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()
