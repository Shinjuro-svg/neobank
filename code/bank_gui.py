import tkinter as tk
from tkinter import messagebox, ttk
from dbc_api import dbc
import json
from datetime import datetime

class BankAccount:
    def __init__(self, account_id, initial_balance=0):
        self.account_id = account_id
        self.balance = initial_balance
        self.transaction_history = []
    
    @dbc.requires(lambda self, amount: amount > 0, "Amount must be positive")
    @dbc.ensures(lambda result, self, amount: result == self.balance, "Balance update failed")
    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append((
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "DEPOSIT",
            amount,
            self.balance
        ))
        return self.balance
    
    @dbc.requires(lambda self, amount: amount > 0, "Amount must be positive")
    @dbc.requires(lambda self, amount: self.balance >= amount, "Insufficient funds")
    @dbc.ensures(lambda result, self, amount: result == self.balance, "Balance update failed")
    def withdraw(self, amount):
        self.balance -= amount
        self.transaction_history.append((
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "WITHDRAWAL",
            amount,
            self.balance
        ))
        return self.balance

class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NeoBank")
        self.geometry("900x700")
        self.configure(bg="#f5f7fa")
        
        # Modern color scheme
        self.primary_color = "#4a6bdf"
        self.secondary_color = "#6c757d"
        self.success_color = "#28a745"
        self.danger_color = "#dc3545"
        self.warning_color = "#ffc107"
        self.light_bg = "#f8f9fa"
        self.dark_bg = "#343a40"
        
        # Custom style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure styles
        self.style.configure('TFrame', background=self.light_bg)
        self.style.configure('TLabel', background=self.light_bg, font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), 
                           background=self.primary_color, foreground="white")
        self.style.configure('Amount.TLabel', font=('Segoe UI', 24, 'bold'))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=8)
        self.style.configure('Primary.TButton', background=self.primary_color, 
                           foreground="white", borderwidth=0)
        self.style.configure('Success.TButton', background=self.success_color, 
                           foreground="white", borderwidth=0)
        self.style.configure('Danger.TButton', background=self.danger_color, 
                           foreground="white", borderwidth=0)
        self.style.configure('TEntry', font=('Segoe UI', 12), padding=8)
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=25)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'))
        self.style.map('Primary.TButton', 
                      background=[('active', '#3a56b5')])
        self.style.map('Success.TButton', 
                      background=[('active', '#218838')])
        self.style.map('Danger.TButton', 
                      background=[('active', '#bd2130')])
        
        # Initialize account with $1000
        self.account = BankAccount("ACC-123", 1000)
        
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ttk.Frame(main_frame, style='TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header_frame, text="NeoBank", style='Header.TLabel',
                 padding=10).pack(fill=tk.X)
        
        # Account Info Card
        account_card = ttk.Frame(main_frame, style='TFrame', 
                               relief=tk.RAISED, borderwidth=1)
        account_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(account_card, text="Account Information", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        info_frame = ttk.Frame(account_card)
        info_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ttk.Label(info_frame, text="Account ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Label(info_frame, text=self.account.account_id, 
                 font=('Segoe UI', 10, 'bold')).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(info_frame, text="Current Balance:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.balance_var = tk.StringVar(value="$1,000.00")
        self.balance_label = ttk.Label(info_frame, textvariable=self.balance_var, 
                                     style='Amount.TLabel')
        self.balance_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Transaction Card
        txn_card = ttk.Frame(main_frame, style='TFrame', 
                            relief=tk.RAISED, borderwidth=1)
        txn_card.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(txn_card, text="Quick Transactions", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        txn_frame = ttk.Frame(txn_card)
        txn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        ttk.Label(txn_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.amount_entry = ttk.Entry(txn_frame, style='TEntry', width=15)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)
        
        button_frame = ttk.Frame(txn_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Deposit", style='Success.TButton',
                  command=self.do_deposit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Withdraw", style='Danger.TButton',
                  command=self.do_withdraw).pack(side=tk.LEFT, padx=5)
        
        # Transaction History Card
        history_card = ttk.Frame(main_frame, style='TFrame', 
                               relief=tk.RAISED, borderwidth=1)
        history_card.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(history_card, text="Transaction History", 
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Treeview with scrollbars
        tree_frame = ttk.Frame(history_card)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        columns = ("date", "type", "amount", "balance")
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        
        # Configure columns
        self.history_tree.heading("date", text="Date/Time")
        self.history_tree.heading("type", text="Type")
        self.history_tree.heading("amount", text="Amount")
        self.history_tree.heading("balance", text="Balance")
        
        self.history_tree.column("date", width=180, anchor=tk.W)
        self.history_tree.column("type", width=120, anchor=tk.W)
        self.history_tree.column("amount", width=120, anchor=tk.E)
        self.history_tree.column("balance", width=120, anchor=tk.E)
        
        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.history_tree.xview)
        self.history_tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
        
        # Grid layout
        self.history_tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Add sample transactions
        for txn in self.account.transaction_history:
            self.history_tree.insert("", tk.END, values=txn)
        
        # Bottom buttons
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(bottom_frame, text="View Contract Violations", style='Primary.TButton',
                  command=self.show_violations).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="Exit", command=self.destroy).pack(side=tk.RIGHT, padx=5)
    
    def update_display(self):
        self.balance_var.set(f"${self.account.balance:,.2f}")
        # Update balance color based on amount
        if self.account.balance < 500:
            self.balance_label.configure(foreground=self.danger_color)
        elif self.account.balance < 1000:
            self.balance_label.configure(foreground=self.warning_color)
        else:
            self.balance_label.configure(foreground=self.success_color)
    
    def add_transaction_to_history(self, txn):
        self.history_tree.insert("", 0, values=txn)
    
    def do_deposit(self):
        amount_str = self.amount_entry.get()
        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount", parent=self)
            return
            
        try:
            amount = float(amount_str)
            new_balance = self.account.deposit(amount)
            self.update_display()
            self.add_transaction_to_history(self.account.transaction_history[-1])
            messagebox.showinfo("Success", 
                              f"Deposited ${amount:,.2f}\nNew balance: ${new_balance:,.2f}", 
                              parent=self)
            self.amount_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Transaction Error", str(e), parent=self)
    
    def do_withdraw(self):
        amount_str = self.amount_entry.get()
        if not amount_str:
            messagebox.showerror("Error", "Please enter an amount", parent=self)
            return
            
        try:
            amount = float(amount_str)
            new_balance = self.account.withdraw(amount)
            self.update_display()
            self.add_transaction_to_history(self.account.transaction_history[-1])
            messagebox.showinfo("Success", 
                              f"Withdrew ${amount:,.2f}\nNew balance: ${new_balance:,.2f}", 
                              parent=self)
            self.amount_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Transaction Error", str(e), parent=self)
    
    def show_violations(self):
        try:
            with open("contract_violations.json", "r") as f:
                violations = json.load(f)
            
            if not violations:
                messagebox.showinfo("Contract Violations", 
                                  "No contract violations recorded", 
                                  parent=self)
                return
                
            # Create a new window to display violations
            violations_window = tk.Toplevel(self)
            violations_window.title("Design by Contract Violations")
            violations_window.geometry("900x600")
            violations_window.configure(bg=self.light_bg)
            
            # Header
            header = ttk.Frame(violations_window, style='TFrame')
            header.pack(fill=tk.X, pady=(0, 15))
            ttk.Label(header, text="Contract Violations Log", 
                     style='Header.TLabel', padding=10).pack(fill=tk.X)
            
            # Main content
            content_frame = ttk.Frame(violations_window)
            content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
            
            # Create a treeview to display violations
            columns = ("timestamp", "type", "function", "message")
            tree = ttk.Treeview(content_frame, columns=columns, show="headings", height=20)
            
            tree.heading("timestamp", text="Timestamp")
            tree.heading("type", text="Type")
            tree.heading("function", text="Function")
            tree.heading("message", text="Message")
            
            tree.column("timestamp", width=180, anchor=tk.W)
            tree.column("type", width=120, anchor=tk.W)
            tree.column("function", width=180, anchor=tk.W)
            tree.column("message", width=400, anchor=tk.W)
            
            # Add scrollbars
            y_scroll = ttk.Scrollbar(content_frame, orient=tk.VERTICAL, command=tree.yview)
            x_scroll = ttk.Scrollbar(content_frame, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)
            
            # Grid layout
            tree.grid(row=0, column=0, sticky="nsew")
            y_scroll.grid(row=0, column=1, sticky="ns")
            x_scroll.grid(row=1, column=0, sticky="ew")
            
            content_frame.grid_rowconfigure(0, weight=1)
            content_frame.grid_columnconfigure(0, weight=1)
            
            for violation in violations:
                tree.insert("", tk.END, values=(
                    violation.get("timestamp"),
                    violation.get("type"),
                    violation.get("function"),
                    violation.get("message")
                ))
                
        except FileNotFoundError:
            messagebox.showinfo("Contract Violations", 
                              "No violations recorded yet", 
                              parent=self)
        except json.JSONDecodeError:
            messagebox.showerror("Error", 
                               "Could not read violations file", 
                               parent=self)

if __name__ == "__main__":
    app = BankingApp()
    app.mainloop()