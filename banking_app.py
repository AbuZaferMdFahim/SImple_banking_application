# banking_app.py
from models import BankAccount, AccountType
from colorama import Fore, Style

import datetime, bcrypt, getpass,random

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
        return f"Account Holder: {self.account_holder}\nAccount Type: {self.account_type.name}\nBalance: {self.balance}\nMobile Number: {self.mobile_number}\nCreation Date: {self.creation_date}"

class AccountType:
    def __init__(self, name, min_balance):
        self.name = name
        self.min_balance = min_balance

class BankingApplication:
    def __init__(self):
        self.accounts = {}
        self.users = {}  
        self.account_types = {
            "Salary": AccountType("Salary", 1000),
            "General": AccountType("General", 500),
            "Savings": AccountType("Savings", 1000),
            "Student": AccountType("Student", 200),
        }
        self.account_counter = 1 

    


