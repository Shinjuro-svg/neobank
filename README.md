# NeoBank - Modern Banking Application

## Overview
NeoBank is a modern desktop banking application built with Python and Tkinter that demonstrates:
- Clean GUI design with a contemporary interface
- Design-by-Contract (DbC) principles implementation
- Secure transaction handling
- Comprehensive transaction history

## Key Features
- **Account Management**:
  - Deposit funds with validation
  - Withdraw funds with balance checks
  - Real-time balance updates
- **Transaction History**:
  - Detailed record of all transactions
  - Timestamped operations
- **Design by Contract**:
  - Precondition checks for all operations
  - Postcondition verification
  - Violation logging and viewing
- **Modern UI**:
  - Clean, responsive interface
  - Color-coded balance indicators
  - Intuitive transaction controls

## Technical Architecture
mermaid
classDiagram
    class BankAccount {
        +account_id: str
        +balance: float
        +transaction_history: list
        +deposit(amount: float) float
        +withdraw(amount: float) float
    }
    
    class BankingApp {
        -account: BankAccount
        +create_widgets()
        +update_display()
        +do_deposit()
        +do_withdraw()
        +show_violations()
    }
    
    BankingApp --> BankAccount: manages


## Installation
1. Clone the repository:
   bash
   git clone https://github.com/Shinjuro-svg/neobank.git
   cd neobank
   

2. Install dependencies:
   bash
   pip install sv-ttk
   

3. Run the application:
   bash
   python code/banking_app.py
   

## Usage
### Making Transactions
1. Enter amount in the input field
2. Click "Deposit" or "Withdraw" button
3. View updated balance and transaction history

### Viewing Contract Violations
1. Click "View Contract Violations" button
2. Review any DbC precondition/postcondition failures

## Quality Assurance
The application implements multiple correctness strategies:

| Strategy | Implementation | Benefit |
|----------|----------------|---------|
| Design by Contract | `@dbc` decorators for all account operations | Prevents invalid transactions |
| Input Validation | Type and range checking | Ensures only valid amounts processed |
| Transaction Logging | Complete history with timestamps | Provides audit trail |
| UI Feedback | Color-coded balance indicators | Immediate visual status |

## Development
### Key Components
- **BankAccount Class**: Core banking logic with DbC enforcement
- **BankingApp Class**: Tkinter-based GUI interface
- **dbc_api**: Contract validation decorators

### Extending the Application
To add new features:
1. Implement methods in `BankAccount` with proper contracts
2. Add corresponding UI elements in `BankingApp`
3. Update transaction history handling as needed

## License
MIT License - See [LICENSE](LICENSE) for details.

## References
- Design by Contract: Meyer, B. (1997). Object-Oriented Software Construction
- Tkinter Documentation: https://docs.python.org/3/library/tkinter.html
- Modern GUI Design Principles
