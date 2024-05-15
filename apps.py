# apps.py
import streamlit as st
from login import login_page
from app import BankApp
from welcome import welcome_page


st.set_page_config(
    page_title="UCB BANK",  # Title of the page
    page_icon=":bank:",     # Favicon (you can use emojis)
    layout="wide",          # Page layout: "centered" or "wide"
    initial_sidebar_state="auto"  # Initial state of the sidebar: "expanded", "collapsed", or "auto"
)


app = BankApp()  # Create an instance of the BankApp class
# Define the navigation structure
PAGES = {
    "Welcome": welcome_page,
    "Login": login_page,
    "Dashboard": app.navigation,
}

# Display the appropriate page based on the session state
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'Welcome'

# Render the selected page
if st.session_state['current_page'] in PAGES:
    PAGES[st.session_state['current_page']]()
