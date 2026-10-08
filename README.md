# 🏦 QuickBalance

A mock banking self-service application built with Python and Streamlit.  
Developed to explore Python web application development using real world banking concepts.

---

## Problem Statement

Bank customers need a simple way to check their account information without calling the bank or visiting a branch. QuickBalance solves this by providing a self-service interface where a customer can log in and immediately access their balance, recent transactions, and full account statement.

---

## Features

- **Mock Customer Login** — customers log in using a unique customer ID with full error handling for empty inputs and invalid IDs
- **Account Summary** — displays account holder name, account number, account type, and customer ID
- **Current Balance** — prominently displays the available balance in South African Rand
- **Last 5 Transactions** — shows the 5 most recent transactions with date, time, description, type, and amount
- **Mini Statement** — shows all transactions with a running balance, filterable by date range
- **Tab Navigation** — clean tabbed interface so only one section is visible at a time
- **Logout** — clears the session completely and returns to the login screen

---

## Tools and Technologies

| Tool | Purpose | Why I chose it |
|---|---|---|
| Python | Core programming language | Language I am currently learning, widely used in financial services |
| Streamlit | Web interface | Builds a web app in pure Python without needing HTML or CSS |
| JSON | Mock data storage | Human readable, Python reads it natively, simulates a real database |

---

## Project Structure

```
QuickBalance/
├── app.py              # Main Streamlit application - UI and logic
├── utils.py            # Helper functions - load data and find customer
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── data/
    └── mock_data.json  # Mock database with 3 customers and 7 transactions each
```

---

## How to Run

**1. Clone the repository**
```bash
git clone https://github.com/kgotso-mapulane/QuickBalance.git
cd QuickBalance
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py
```

**4. Open your browser**  
Streamlit will open automatically at `http://localhost:8501`

---

## Test Customers

| Customer ID | Name | Account Type |
|---|---|---|
| CUST001 | Alice Johnson | Current Account |
| CUST002 | Bob Smith | Savings Account |
| CUST003 | Carol White | Current Account |

---

## Data Design

Each customer has:
- A unique customer ID used for login
- An opening balance representing funds before the recorded transactions
- 7 transactions covering a mix of credits and debits
- All balances are mathematically verified — opening balance plus all transactions equals the current balance

---

## What I Learned

- **Data integrity** — all parts of the application must tell the same consistent story. I caught a balance inconsistency early and recalculated all balances from the transactions.
- **Separation of concerns** — keeping data logic in utils.py and UI in app.py makes the code easier to maintain and explain.
- **Thinking beyond making it work** — error handling, edge cases, and user experience matter as much as the core functionality.
