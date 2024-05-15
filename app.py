import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
from database_class import DatabaseConnector
from account_class import Account
from deposit_class import Deposit
from withdraw_class import Withdraw
from fund_transfer_class import FundTransfer
from transactions_class import Transactions
from checking_account_class import CheckingAccount
from bank_class import Bank


class BankApp:
    def __init__(self):
        super().__init__()
        #self.apps = []
        self.db = DatabaseConnector()
        self.db.connect()


    def navigation(self):
        with st.sidebar:
            app = option_menu(
                menu_title='UCB Bank',
                options=['Bank', 'Select Account','Deposit','Withdraw','Fund Transfer','Check Account'],
                icons=['bank', 'person-square','upload','download','arrows-expand-vertical','wallet'],
                menu_icon='list',  # Changed to a valid icon
                default_index=0,
                styles={
                    "container": {"padding": "16px", "background-color": "#fcfcfc"},
                    "icon": {"color": "black", "font-size": "16px"},

                }
            )


        if app == "Bank":
            bank = Bank()
            bank.account_number_form()
            bank.create_account_form()
            #bank.sub_menu()

        if app == "Select Account":
            account = Account()
            account.select_account()

        if app == "Transactions":
            db_connector = DatabaseConnector()
            transactions = Transactions(db_connector)
            transactions.show_transactions()

        if app == "Deposit":
            st.header("Deposit Class")
            deposit = Deposit(self.db)
            deposit.perform_deposit()

        if app == "Withdraw":
            st.header("Withdraw Funds")
            withdraw = Withdraw(self.db)
            withdraw.perform_withdraw()

        if app == "Fund Transfer":
            st.header("Fund Transfer Class")
            fund_transaction = FundTransfer()
            fund_transaction.perform_fund_transfer()

        if app == "Check Account":
            st.header("Check Account Class")
            check_account = CheckingAccount()
            check_account.check_this_account()

    def __del__(self):
        self.db.disconnect()


if __name__ == "__main__":
    bank_app = BankApp()
    bank_app.navigation()

