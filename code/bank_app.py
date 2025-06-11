from dbc_api import dbc

class BankAccount:
    def __init__(self, account_id, initial_balance=0):
        self.account_id = account_id
        self.balance = initial_balance
    
    def __str__(self):
        return f"BankAccount({self.account_id}, balance=${self.balance})"
    
    @dbc.requires(
        lambda self, amount: amount > 0,
        "Amount must be positive"
    )
    @dbc.ensures(
        lambda result, self, amount: result == self.balance,
        "Balance not correctly updated"
    )
    def deposit(self, amount):
        old_balance = self.balance
        self.balance += amount
        return self.balance
    
    @dbc.requires(
        lambda self, amount: amount > 0,
        "Amount must be positive"
    )
    @dbc.requires(
        lambda self, amount: self.balance >= amount,
        "Insufficient funds"
    )
    @dbc.ensures(
        lambda result, self, amount: result == self.balance,
        "Balance not correctly updated"
    )
    def withdraw(self, amount):
        old_balance = self.balance
        self.balance -= amount
        return self.balance

if __name__ == "__main__":
    account = BankAccount("ACC-123", 1000)
    
    print("=== Banking System ===")
    print(f"Starting balance: ${account.balance}")
    
    operations = [
        ("Deposit $500", lambda: account.deposit(500)),
        ("Withdraw $200", lambda: account.withdraw(200)),
        ("Invalid deposit (-$100)", lambda: account.deposit(-100)),
        ("Over-withdraw ($2000)", lambda: account.withdraw(2000))
    ]
    
    for desc, op in operations:
        print(f"\nOperation: {desc}")
        try:
            new_balance = op()
            print(f"New balance: ${new_balance}")
        except ValueError as e:
            print(f"ERROR! {e}")
    
    print("\n=== Final Status ===")
    print(f"Account balance: ${account.balance}")
    print(f"Violations logged to: contract_violations.json")