import streamlit as st
import pandas as pd


class Transactions():
    def __init__(self, db_connector):
        self.db_connector = db_connector
        st.header("TRANSACTIONS CLASS")


    def show_transactions(self):
        self.db_connector.connect()
        transactions = self.db_connector.fetch_all_transactions()
        self.db_connector.disconnect()


        if 'account_number' in st.session_state:
            account_number = st.session_state['account_number']
            if account_number:
                if transactions:
                    df = pd.DataFrame(transactions)
                    df['account_number'] = df['account_number'].astype(str)
                    df['date_time'] = df['date_time'].dt.strftime('%Y-%m-%d')
                    df['amount'] = df['amount'].apply(lambda x: "£ {:,.2f}".format(x))
                    st.dataframe(df, width=1200)
                else:
                    st.write("No transactions found.")
            else:
                st.error("Please select an account to view transactions.")
        else:
            st.error("Please select an account to view transactions.")
