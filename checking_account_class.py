# In checking_account_class.py
import streamlit as st
import pandas as pd
from database_class import DatabaseConnector

class CheckingAccount:
    def __init__(self):
        self.db = DatabaseConnector()
        self.db.connect()  # Call the connect method to establish the database connection
        st.header("Checking Account Transactions")

    def check_this_account(self):
        if 'account_number' in st.session_state:
            account_number = st.session_state['account_number']
            st.write(f"Transactions for Account Number: {account_number}")


            transactions = self.db.fetch_transactions(account_number)
            if transactions:
                df = pd.DataFrame(transactions)
                df['account_number'] = df['account_number'].astype(str)
                df['date_time'] = df['date_time'].dt.strftime('%Y-%m-%d')
                df['amount'] = df['amount'].apply(lambda x: "£ {:,.2f}".format(x))
                st.dataframe(df, width=1200)
            else:
                st.write("No transactions found for this account.")
        else:
            st.error("Please select an account to view transactions.")