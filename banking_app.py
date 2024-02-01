from models import BankAccount, AccountType
from colorama import Fore, Style

import datetime, bcrypt, getpass, random, json

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

    def update_account(self, username):
        if username in self.users:
            account_number = int(input("Enter Your account number = "))
            if account_number in self.accounts:
                print("Select the information to update:\n")
                print("1. Account Holder's Name")
                print("2. Mobile Number")
                print("3. Both\n")
                option = int(input("Enter any number for an update (1-3): "))

                if option == 1 or option == 3:
                    updated_account_holder = input("Enter account holder's name = ")
                    self.accounts[account_number].account_holder = updated_account_holder

                if option == 2 or option == 3:
                    updated_mobile_number = input("Enter updated mobile number = ")
                    self.accounts[account_number].mobile_number = updated_mobile_number

                print("Account updated successfully.\n")
            else:
                # for color using colorama
                print(f"{Fore.RED}Update failed. Account not found.{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}User not logged in.{Style.RESET_ALL}\n")
            return "main"

    def delete_account(self, username):
        if username in self.users:
            account_number = int(input("Enter account number to delete: "))
            if account_number in self.accounts:
                del self.accounts[account_number]
                print("Account deleted successfully.\n")
            else:
                print(f"{Fore.RED}Delete failed. Account not found.{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}User not logged in.{Style.RESET_ALL}\n")
            return "main"

    def deposit_amount(self, username):
        account_number = int(input("Enter account number to deposit = "))
        account = self.accounts.get(account_number)

        if account:
            deposit_amount = float(input("Enter deposit amount = "))
            if deposit_amount < account.account_type.min_balance:
                print(f"{Fore.RED}Deposit failed. (Minimum Deposit: {account.account_type.min_balance}){Style.RESET_ALL}\n")
            else:
                account.balance += deposit_amount
                print("Amount deposited successfully.\n")
        else:
            print(f"{Fore.RED}Deposit failed. Account not found.{Style.RESET_ALL}\n")
            return "main"



    def withdraw_amount(self, username):
        if username in self.users:
            account_number = int(input("Enter account number to withdraw = "))
            if account_number in self.accounts:
                withdraw_amount = float(input("Enter withdrawal amount = "))
                if withdraw_amount <= self.accounts[account_number].balance - self.accounts[account_number].account_type.min_balance:
                    self.accounts[account_number].balance -= withdraw_amount
                    print("Amount withdrawn successfully.\n")
                else:
                    print(f"{Fore.RED}Withdraw failed for Insufficient Funds.{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}Withdraw failed for Account not found.{Style.RESET_ALL}\n")
        else:
            print(f"{Fore.RED}User not logged in.{Style.RESET_ALL}\n")
            return "main"

    def search_account(self):
        search_term = input("Enter account holder's name to search = ")
        found_accounts = [account for account in self.accounts.values()
                          if str(account.account_number) == search_term or account.account_holder == search_term]

        if found_accounts:
            print("\nSearch Results:\n")
            for account in found_accounts:
                print(f"Account Holder = {account.account_holder}, "
                      f"Mobile Number = {account.mobile_number}, "
                      f"Account Type = {account.account_type.name}, "
                      f"Balance = {account.balance}")
        else:
            print(f"{Fore.RED}No matching accounts found.{Style.RESET_ALL}\n")

    def operation(self, username):
        while True:
            print("\nAccount Operations Menu:\n")
            print("Enter 1. Display All Accounts")
            print("Enter 2. Update Account")
            print("Enter 3. Delete Account")
            print("Enter 4. Deposit Amount")
            print("Enter 5. Withdraw Amount")
            print("Enter 6. Search for Account")
            print("Enter 7. Logout")
            option = int(input("Enter any option (1-7): "))

            if option == 1:
                self.display_all_accounts()
            elif option == 2:
                self.update_account(username)
            elif option == 3:
                self.delete_account(username)
            elif option == 4:
                self.deposit_amount(username)
            elif option == 5:
                self.withdraw_amount(username)
            elif option == 6:
                self.search_account()
            elif option == 7:
                print("Logout successful.\n\n")
                return "main"
            else:
                print("Please enter a number between 1 to 7.\n")

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


