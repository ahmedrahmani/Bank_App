import streamlit as st
from database_class import DatabaseConnector
import datetime
import random
class Bank():
    def __init__(self):

        self.db = DatabaseConnector()
        self.db.connect()

        st.write("""
            <h3 style="color: #FF4B4B; text-align: center;">UCB Bank Project</h3>
            <div style="background-color: #03e6ff; padding: 20px; border-radius: 10px; text-align: center;">
                <p style="color: #505454; font-size: 14px; line-height: 1.5; ">
                    UCB Bank is an Object-Oriented Programming System (OOPs) Project developed for learning Software Development using OOPs techniques by a University College Birmingham UK, Student of MSc. Computer Science.
                </p>
            </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image("images/bank_accounts.png", width=300)

    def account_number_form(self):
        with st.expander("Create New Account"):

            st.subheader("Welcome to UCB Bank")
            if st.button("Click to Generate New Account Number"):
                account_number = self.generate_account_number()
                st.session_state['account_number'] = account_number
                st.write(f"Generated Account Number: {account_number}")

            # Initialize session state for form visibility
            if 'show_form' not in st.session_state:
                st.session_state['show_form'] = True  # Form is visible by default
            if 'form_container' not in st.session_state:
                # Initialize the form container in the session state
                st.session_state['form_container'] = st.empty()

    def generate_account_number(self):
        # Generate a random number with the prefix "2405"
        random_part = random.randint(0, 9999)
        account_number = int("2405" + f"{random_part:04d}")  # Ensures the random part is 4 digits

        # Check if the generated account number is unique
        if self.is_unique_account_number(account_number):
            return account_number
        else:
            # Recursively try to generate a unique number if the first attempt was not unique
            return self.generate_account_number()

    def is_unique_account_number(self, account_number):
        query = f"SELECT COUNT(*) FROM accounts_data WHERE account_number = {account_number}"
        cursor = self.db.connection.cursor()
        cursor.execute(query)
        (count,) = cursor.fetchone()
        return count == 0

    def create_account_form(self):
        if st.session_state.get('show_form', True):
            with st.session_state['form_container']:
                st.subheader("Create New Account")
                if 'account_number' in st.session_state:
                    st.success(f"Generated Account Number is : {st.session_state['account_number']}")
                else:
                    st.info("Please generate an account number to create a new account.")
                    return
                st.markdown("<h1 style='text-align: center;'>New Account Form</h1>", unsafe_allow_html=True)
                with st.form("New Account Form"):

                    col1, col2= st.columns([1, 2])
                    with col1:
                        st.info("Generated Account Number is")
                    with col2:
                        st.success(f"{st.session_state['account_number']}")
                        #st.header(st.session_state['account_number'])

                    #customer_name = st.text_input("Customer Name")

                    # Input boxes for first name and last name
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        first_name = st.text_input("First Name")
                    with col2:
                        last_name = st.text_input("Last Name")

                    # Combine the first name and last name into one variable
                    customer_name = f"{first_name} {last_name}"

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        email_id = st.text_input("Email ID")
                    with col2:
                        phone_number = st.text_input("Phone Number")

                    with col1:
                        account_type = st.selectbox("Account Type", ['savings', 'current'])
                    with col2:
                        total_balance = st.number_input("Initial Deposit", min_value=0.0)

                    customer_address = st.text_input("Customer Address")

                    submit_button = st.form_submit_button("Create Account")
                    if submit_button:
                        if not customer_name:
                            st.error("Customer Name cannot be left empty.")
                        if not email_id:
                            st.error("Email ID cannot be left empty.")
                        if not phone_number:
                            st.error("Phone Number cannot be left empty.")
                        if not customer_address:
                            st.error("Customer Address cannot be left empty.")
                        if customer_name and email_id and phone_number and customer_address:
                            self.create_account(customer_name, email_id, phone_number, account_type, total_balance,
                                                customer_address)
                            st.success("Account created successfully!")


    def create_account(self, customer_name, email_id, phone_number, account_type, total_balance, customer_address):
        account_number = st.session_state['account_number']
        created_on = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = f"""INSERT INTO accounts_data (account_number, customer_name, email_id, phone_number, account_type, total_balance, customer_address, created_on) 
                    VALUES ({account_number}, '{customer_name}', '{email_id}', '{phone_number}', '{account_type}', {total_balance}, '{customer_address}', '{created_on}');"""
        self.db.execute_query(query)

        # Insert initial deposit transaction
        transaction_details = "initial deposit"
        transaction_query = f"""INSERT INTO transactions (account_number, date_time, amount, transaction_type, transaction_details) 
                                VALUES ({account_number}, '{created_on}', {total_balance}, 'deposit', '{transaction_details}');"""
        self.db.execute_query(transaction_query)