import streamlit as st                       # Streamlit builds the web UI
from utils import load_data, find_customer  # Our helper functions from utils.py
from datetime import datetime               # datetime lets us work with dates and times

# --- Page Configuration ---
# This must be the FIRST Streamlit command in the file
st.set_page_config(
    page_title="QuickBalance",   # Title shown on the browser tab
    page_icon="🏦",              # Icon shown on the browser tab
    layout="centered"            # Centers the content on the page
)

# --- Load Data ---
# We load the mock data once when the app starts.
# st.cache_data tells Streamlit to remember the result so it doesn't
# re-read the file every time the user clicks something.
@st.cache_data
def get_data():
    return load_data()

data = get_data()  # data is now the full dictionary from mock_data.json

# --- Session State ---
# st.session_state is like a memory for the app.
# Streamlit reruns the whole script every time a user interacts with it,
# so we use session_state to remember whether someone is logged in.
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False   # Default: not logged in

if "customer" not in st.session_state:
    st.session_state.customer = None     # Default: no customer loaded

# --- Login Screen ---
# We only show this block when the user is NOT logged in
if not st.session_state.logged_in:

    # App title and welcome message
    st.title("🏦 QuickBalance")
    st.subheader("Welcome! Please log in to view your account.")
    st.write("---")  # Draws a horizontal divider line

    # Text input box for the customer ID
    # The value the user types is stored in the variable 'customer_id'
    customer_id = st.text_input(
        label="Enter your Customer ID",   # Label shown above the box
        placeholder="e.g. CUST001",       # Grey hint text inside the box
        max_chars=10                       # Limit input to 10 characters
    )

    # Login button - when clicked, Streamlit reruns the script
    # and st.button returns True only on the click that triggered the rerun
    if st.button("Login", use_container_width=True):

        # Only try to find the customer if the user actually typed something
        if customer_id.strip() == "":
            st.warning("⚠️ Please enter a Customer ID.")

        else:
            # Call our find_customer function from utils.py
            customer = find_customer(customer_id, data)

            if customer is None:
                # No match found - show an error message in red
                st.error("❌ Invalid Customer ID. Please try again.")

            else:
                # Match found! Save to session_state and mark as logged in
                st.session_state.customer = customer
                st.session_state.logged_in = True
                # st.rerun() forces the page to refresh so the dashboard shows
                st.rerun()

# --- Dashboard (shown after login) ---
# We only show this block when the user IS logged in
else:
    customer = st.session_state.customer  # Retrieve the saved customer data

    # Greeting header
    st.title(f"👋 Welcome, {customer['name']}!")
    st.write("---")

    # --- Account Summary Section ---
    st.subheader("📋 Account Summary")

    # st.columns splits the page into side-by-side columns.
    # [1, 1] means two equal-width columns.
    col1, col2 = st.columns(2)

    # 'with col1' means everything inside this block goes into the left column
    with col1:
        st.write(f"**Account Holder:** {customer['name']}")
        st.write(f"**Account Number:** {customer['account_number']}")

    with col2:
        st.write(f"**Account Type:** {customer['account_type']}")
        st.write(f"**Customer ID:** {customer['customer_id']}")

    st.write("---")

    # --- Tabs ---
    # st.tabs creates clickable tabs at the top of the section.
    # We give each tab a label and unpack them into variables.
    # 'with tab1' means everything inside that block belongs to that tab.
    tab1, tab2, tab3 = st.tabs(["💰 Balance", "🧾 Last 5 Transactions", "📄 Mini Statement"])

    # ── TAB 1: Balance ──────────────────────────────────────────────────
    with tab1:

        st.subheader("💰 Current Balance")
        st.metric(
            label="Available Balance",
            value=f"R {customer['balance']:,.2f}"
        )

    # ── TAB 2: Last 5 Transactions ──────────────────────────────────────
    with tab2:

        st.subheader("🧾 Last 5 Transactions")

        # Take only the 5 most recent transactions
        recent = customer["transactions"][:5]
        table_data = []

        for txn in recent:
            if txn["type"] == "credit":
                amount_display = f"+ R {txn['amount']:,.2f}"
            else:
                amount_display = f"- R {txn['amount']:,.2f}"

            # Combine date and time into one readable field
            # e.g. "2026-08-30" + "08:00" becomes "2026-08-30 08:00"
            datetime_display = f"{txn['date']} {txn['time']}"

            table_data.append({
                "Date & Time":  datetime_display,   # Combined date and time column
                "Description":  txn["description"],
                "Type":         txn["type"].title(),
                "Amount (R)":   amount_display
            })

        st.dataframe(table_data, use_container_width=True, hide_index=True)

    # ── TAB 3: Mini Statement ───────────────────────────────────────────
    with tab3:

        st.subheader("📄 Mini Statement")
        st.caption("All transactions with running balance")

        # --- Date Filter ---
        # st.date_input shows a date picker widget the customer can use
        # to filter transactions between two dates.
        # We use st.columns to put the two date pickers side by side.
        col_from, col_to = st.columns(2)

        with col_from:
            # Default start date is the oldest transaction date
            # datetime.strptime converts a text date "2026-08-15" into a real date object
            # .date() removes the time part leaving just the date
            start_date = st.date_input(
                "From date",
                value=datetime.strptime("2026-08-15", "%Y-%m-%d").date()
            )

        with col_to:
            # Default end date is today
            # datetime.today() gives the current date and time
            end_date = st.date_input(
                "To date",
                value=datetime.today().date()
            )

        # Get all transactions and reverse to oldest first
        all_transactions = customer["transactions"]
        running_balance  = customer["opening_balance"]  # Start from opening balance
        statement_data   = []

        # Loop through transactions oldest first
        for txn in all_transactions[::-1]:

            # Apply the transaction to the running balance for every transaction
            # regardless of the filter — this keeps the running balance accurate
            if txn["type"] == "credit":
                running_balance = running_balance + txn["amount"]  # Money in
            else:
                running_balance = running_balance - txn["amount"]  # Money out

            # Convert the transaction date from text to a real date object
            # so we can compare it with the filter dates chosen by the customer
            # datetime.strptime reads a string and converts it to a datetime object
            # "%Y-%m-%d" tells Python the format: Year-Month-Day
            txn_date = datetime.strptime(txn["date"], "%Y-%m-%d").date()

            # Only add this transaction to the display if it falls within the filter range
            # start_date <= txn_date <= end_date means the transaction date is
            # on or after the start date AND on or before the end date
            if start_date <= txn_date <= end_date:

                if txn["type"] == "credit":
                    amount_display = f"+ R {txn['amount']:,.2f}"
                else:
                    amount_display = f"- R {txn['amount']:,.2f}"

                # Combine date and time into one readable field
                datetime_display = f"{txn['date']} {txn['time']}"

                statement_data.append({
                    "Date & Time":  datetime_display,
                    "Description":  txn["description"],
                    "Type":         txn["type"].title(),
                    "Amount (R)":   amount_display,
                    "Balance (R)":  f"R {running_balance:,.2f}"
                })

        # Show how many transactions matched the filter
        st.caption(f"Showing {len(statement_data)} transaction(s) for selected period")

        # If no transactions match the filter, show a friendly message
        if len(statement_data) == 0:
            st.info("No transactions found for the selected date range.")
        else:
            st.dataframe(statement_data, use_container_width=True, hide_index=True)

    # Logout button - resets session state and returns to login screen
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.customer = None
        st.rerun()
