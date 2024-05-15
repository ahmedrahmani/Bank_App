# login_view.py
import streamlit as st
from auth_controller import authenticate_user

def login_page():





    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        st.image("images/login_img.jpeg", width=200)  # Adjust the path to your logo image

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        username = st.text_input('Username', key="username")
        password = st.text_input('Password', type='password', key="password")

        if st.button('Login'):
            # Call the authentication function from auth_controller.py
            user_authenticated, user_details = authenticate_user(username, password)
            if user_authenticated:
                # Credentials are correct
                st.session_state['loggedin'] = True
                st.session_state['employee_id'] = user_details['employee_id']
                st.session_state['employee_name'] = user_details['employee_name']
                # Update the current_page to 'Dashboard'
                st.session_state['current_page'] = 'Dashboard'
                st.experimental_rerun()
            else:
                # Credentials are incorrect
                st.error("Incorrect details. Enter valid credentials.")

