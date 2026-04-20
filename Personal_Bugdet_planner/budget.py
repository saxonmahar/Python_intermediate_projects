import matplotlib.pyplot as plt
from collections import defaultdict

expenses = []  # Renamed from 'expense' to avoid confusion

def set_savings_goals():
    goal = float(input("Enter your monthly saving goals: "))
    print(f"Your savings goal is set to ${goal:.2f}")
    return goal
    
def add_income():
    income = float(input("Enter your monthly income: "))
    print(f"Your monthly income is ${income:.2f}")
    return income

def add_expense():
    category = input("Enter your expense category (eg, Food, Housing): ").capitalize()
    amount = float(input("Enter your monthly expenses amount: "))
    expenses.append({"category": category, "amount": amount})
    print(f"Expense of ${amount:.2f} added under {category}")
    
def view_expenses_by_category():
    category_totals = defaultdict(float)
    for exp in expenses:  # Changed from 'expense' to 'exp'
        category_totals[exp["category"]] += exp["amount"]
    
    print("\nExpenses by category:")
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")

def calculate_remaining_budget(income, expenses):
    total_expenses = sum(exp["amount"] for exp in expenses)
    remaining = income - total_expenses
    print(f"Total expenses: ${total_expenses:.2f}")
    print(f"Remaining budget: ${remaining:.2f}")  
    return remaining  # FIXED: Added return statement

def check_savings_goal(remaining, goal):  # FIXED: Typo in function name
    if remaining >= goal:
        print(f"Congratulations! You have met your savings goal with ${remaining - goal:.2f} extra!")
    else:
        print(f"You are ${goal - remaining:.2f} short of your savings goal")

def plot_expenses():  # FIXED: Typo in function name
    category_totals = defaultdict(float)
    for exp in expenses:
        category_totals[exp["category"]] += exp["amount"]

    labels = category_totals.keys()
    values = category_totals.values()
    
    if values:  # Check if there are expenses to plot
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Expense Distribution")
        plt.show()
    else:
        print("No expenses to plot. Please add expenses first.")

def main():
    print("Welcome to the Personal Finance Manager")
    goal = set_savings_goals()
    income = add_income()
    remaining = 0  # FIXED: Initialize remaining variable
    
    while True:
        print("\nPlease select an option:")
        print("1. Add expense")
        print("2. View expenses by category")
        print("3. Calculate remaining budget")
        print("4. Check savings goal")
        print("5. Plot expense distribution")
        print("6. Exit")
        choice = input("Enter your choice (1/2/3/4/5/6): ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses_by_category()
        elif choice == "3":
            remaining = calculate_remaining_budget(income, expenses)  # FIXED: Store returned value
        elif choice == "4":
            if remaining > 0 or remaining == 0:  # Check if budget was calculated
                check_savings_goal(remaining, goal)
            else:
                print("Please calculate your remaining budget first (option 3).")
        elif choice == "5":
            plot_expenses()  # FIXED: Correct function name      
        elif choice == "6":
            print("Good Bye!!!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
            
if __name__ == "__main__":
    main()