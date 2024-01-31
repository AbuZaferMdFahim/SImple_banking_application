from models import BankAccount, AccountType
from colorama import Fore, Style, json

import datetime, bcrypt, getpass, random

class User:
    def __init__(self, username, hashed_password):
        self.username = username
        self.hashed_password = hashed_password

class BankAccount:
    def __init__(self, account_holder, account_number, account_type, balance=0.0, mobile_number=None):
        self.account_holder = account_holder
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.creation_date = datetime.datetime.now()
        self.mobile_number = mobile_number

    def __str__(self):
        return f"Account Holder = {self.account_holder}\nAccount Type = {self.account_type.name}\nBalance = {self.balance}\nMobile Number = {self.mobile_number}\nCreation Date = {self.creation_date}"

class AccountType:
    def __init__(self, name, min_balance):
        self.name = name
        self.min_balance = min_balance

class BankingApplication:
    def __init__(self):
        self.load_data()  # Load existing accounts and users
        self.account_types = {
            "Salary": AccountType("Salary", 1000),
            "General": AccountType("General", 500),
            "Savings": AccountType("Savings", 1000),
            "Student": AccountType("Student", 200),
        }
        self.account_counter = 1 

    def load_data(self):
        try:
            with open("accounts.json", "r") as file:
                data = json.load(file)
                self.accounts = {int(account_number): BankAccount(**account_data) for account_number, account_data in data["accounts"].items()}
                self.users = {username: User(**user_data) for username, user_data in data["users"].items()}
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file is not found or cannot be decoded, initialize with empty data
            self.accounts = {}
            self.users = {}

    def save_data(self):
        data = {
            "accounts": {str(account.account_number): vars(account) for account in self.accounts.values()},
            "users": {username: vars(user) for username, user in self.users.items()},
        }
        with open("accounts.json", "w") as file:
            json.dump(data, file, default=str)

    def generate_account_number(self):
        while True:
            account_number = random.randint(10**9, 10**10 - 1) 
            if account_number not in self.accounts:
                return account_number

    def create_account(self):
        username = input("Enter a username =  ")
        mobile_number = input("Enter mobile number =  ")

        # Check if the username is already taken
        if username in self.users:
            print(f"{Fore.RED}Account creation failed. Username already taken.{Style.RESET_ALL}\n")
            return

        password = getpass.getpass("Enter a password =  ")
        confirm_password = getpass.getpass("Confirm the password =  ")

        # Check if the passwords match
        if password != confirm_password:
            print(f"{Fore.RED}Account creation failed. Passwords do not match. {Style.RESET_ALL}\n")
            return

        name = input("Enter account holder's name = ")

        print("Available Account Types:\n")
        for i, (account_type_name, account_type) in enumerate(self.account_types.items(), 1):
            print(f"{i}. {account_type_name} (Minimum Deposit: {account_type.min_balance})")

        account_type_choice = int(input("Select account types: (1-4) "))
        account_type_names = list(self.account_types.keys())
        account_type_name = account_type_names[account_type_choice - 1]
        account_type = self.account_types[account_type_name]

        initial_balance = float(input("Enter deposit amount = "))

        if initial_balance < account_type.min_balance:
            print(f"Deposit must be at least {account_type.min_balance}. Account creation failed.\n")
            return

        account_number = self.generate_account_number()
        new_account = BankAccount(name, account_number, account_type, initial_balance, mobile_number)
        self.accounts[account_number] = new_account 

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(username, hashed_password)
        self.users[username] = new_user

        print(f"Account created successfully. Account number: {account_number}")

    def login(self):
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")

        if username in self.users:
            stored_hashed_password = self.users[username].hashed_password
            hashed_password_input = bcrypt.hashpw(password.encode("utf-8"), stored_hashed_password)
            if hashed_password_input == stored_hashed_password:
                print(f"Login successful for user: {username}\n")
                self.operation(username)
            else:
                print(f"{Fore.RED}Invalid password. Login failed.{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}User not found. Login failed.{Style.RESET_ALL}\n")
            return "main"

    def display_all_accounts(self):
        if not self.accounts:
            print("No accounts found.\n")
            return

        print("All Accounts:\n")
        for account_number, account in self.accounts.items():
            print(account)
            print("...............................\n")

    

    def operation(self, username):
        while True:
            print("\nAccount Operations Menu:\n")
            print("Enter 1. Display All Accounts")


            if option == 1:
                self.display_all_accounts()
        

if __name__ == "__main__":
    banking_app = BankingApplication()

    while True:
        print("Welcome to the Banking Application!\n")
        print("Enter 1 For. LOG IN (If you have an account)")
        print("Enter 2 For. CREATE AN ACCOUNT (If you haven't any account)")
        print("Enter 3 For. EXIT")

        option = input("Enter your option (1-3): ")

        if option == "1":
            banking_app.login()
        elif option == "2":
            banking_app.create_account()
        elif option == "3":
            print("Exiting the application.")
            break
        else:
            print("Please enter a number between 1 and 3.")


