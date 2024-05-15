import streamlit as st
from database_class import DatabaseConnector  # Ensure this import is correct based on your project structure
from decimal import Decimal

class Account:
    def __init__(self):
        st.header("Account Search")
        self.db = DatabaseConnector()
        self.db.connect()
        self.apply_styles()

    def apply_styles(self):
        css_style = """
        <style>
        
        .card {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            border-radius: 20px;
            padding: 10px;
            box-shadow: 0px 0px 5px rgba(0, 0, 0, 0.2);
            margin: 0 auto;
            width: 80%;
            height: 490px;
            background: rgb(40,0,88);
            background: linear-gradient(145deg, rgba(40,0,88,1) 40%, rgba(77,0,0,1) 99%);
        }
        
        .left-container {
            background: #000000; 
            background: -webkit-linear-gradient(to right, #434343, #000000);
            background: linear-gradient(to right, #2a4d4f, #000000); 
            flex: 1;
            max-width: 30%;
            display: flex;
            flex-direction: column;
            align-items: center;
            height:450px;
            padding: 10px;
            margin: 10px;
            border-radius: 20px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
          }
  
          .right-container {
            background: #000000; 
            background: -webkit-linear-gradient(to left, #434343, #000000);
            background: linear-gradient(to left, #434343, #000000); 
            flex: 1;
            max-width:70%;
            height:450px;
            padding: 30px 40px;
            margin: 10px;
            border-radius:20px;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
          }
          
          .gradienttext{
            background-image: linear-gradient(to right, #ee00ff 0%, #fbff00 100%);
            color: transparent;
            -webkit-background-clip: text;
            font-size: 40px;
            text-align: center;
          }
          
          .h1{
            padding-top: 50%;
            font-size: 50px;
          }
          
          .h2 {
          
            font-size: 24px;
            margin-bottom: 25px;
            text-align: center;
            
            background-image: linear-gradient(to right, #ee00ff 0%, #fbff00 100%);
            color: transparent;
            -webkit-background-clip: text;
          }
          
          .h3 {
            text-align: center;
            font-size: 24px;
            margin-bottom: 5px;
          }
          
          .h4 {
            font-size: 16px;
            margin-bottom: 20px;  
            color: #ff4b4b;
          }
          
          .details{
            color: yellowgreen;
            padding-left: 10px;
          }
          
          .h4{
            background-color: #282828;
            width: 350px;
            margin: 0 auto;
            padding: 5px 20px;
            
          }
          
          .profile_box{
            background-color: #282828;
            border-radius: 10px; !important
          }
          
         
        /* Add the rest of your CSS here */
        </style>
        """
        st.markdown(css_style, unsafe_allow_html=True)

    def display_account_details(self, result):
        if result:
            # Dynamically generate the profile card HTML with account details
            account_id = result[0]
            account_number = result[1]
            customer_name = result[2]
            email_ID = result[3]
            phone_number = result[4]
            account_type = result[5]
            total_balance = result[6]
            customer_address = result[7]
            created_on = result[8]

            # Store in session state
            st.session_state['account_number'] = account_number
            st.session_state['account_type'] = account_type
            st.session_state['total_balance'] = total_balance

            profile_card_html = f"""
            <div class="card">
              <div class="left-container">
                <p class="gradienttext h1">{customer_name}</p>
                
            
              </div>
              <div class="right-container">
                <p class="h2">Profile Details</p>
                <div class="profile_box">
                    <p class="h4"><span class="list_item"><strong>Account ID:</strong></span><span class="details"> {account_id}</span></p>
                    <p class="h4"><strong>Account Type:</strong><span class="details"> {account_type} Account</span></p>
                    <p class="h4"><strong>Account Number:</strong><span class="details"> {account_number}</span></p>
                    <p class="h4"><strong>Email ID:</strong><span class="details"> {email_ID}</span></p>
                    <p class="h4"><strong>Phone Number:</strong><span class="details"> {phone_number}</span></p>
                    <p class="h4"><strong>Total Balance:</strong><span class="details"> {total_balance}</span></p>
                    <p class="h4"><strong>Customer Address:</strong><span class="details"> {customer_address}</span></p>
                    <p class="h4"><strong>Created On:</strong><span class="details"> {created_on}</span></p>
                </div>
              </div>
            </div>
            """
            st.markdown(profile_card_html, unsafe_allow_html=True)
        else:
            st.write("Account not found.")


    def search_account(self):
        account_number = st.text_input("Enter account number to search:", "")
        if st.button("Search"):
            if account_number:

                result = self.db.search_account(account_number)
                self.display_account_details(result)  # Adjusted to display the account details
            else:
                st.error("Please enter an account number.")

    def select_account(self):
        self.search_account()


class SavingsAccount(Account):
    def withdraw(self, amount):
        fee = Decimal('0.00')
        if amount > 1000:
            fee = amount * Decimal('0.02')
        return amount + fee

class CurrentAccount(Account):
    def withdraw(self, amount):
        fee = Decimal('0.00')
        if amount > 5000:
            fee = amount * Decimal('0.02')
        return amount + fee


