import datetime
class AccountType:
    def __init__(self, type_name, min_balance):
        self.type_name = type_name
        self.min_balance = min_balance

    def __str__(self):
        return self.type_name

class BankAccount:
    def __init__(self, account_holder, account_number, account_type, balance=0.0, mobile_number=None):
        self.account_holder = account_holder
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.creation_date = datetime.datetime.now()
        self.mobile_number = mobile_number

    def deposit(self, amount):
        self.balance = self.deposit + amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance = self.deposit - amount
            return True
        else:
            return False

    def __str__(self):
        return f"Account Holder: {self.account_holder}\nAccount Type: {self.account_type.name}\nBalance: {self.balance}\nMobile Number: {self.mobile_number}\nCreation Date: {self.creation_date}"
