# views/welcome_view.py
import streamlit as st


def welcome_page():
    # Set page configuration
    #st.set_page_config(page_title="Welcome to UCB Bank", layout="centered")

    # Apply CSS styling for background color and rounded border
    st.markdown(
        """
        <style>
        .welcome-container {
            background-color: #fe4b4b; /* Choose your desired background color */
            padding: 10px;
            border-radius: 0px; /* Adjust the border radius as needed */
            width: 50%;
            margin: 0 auto; !important

        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a container for the welcome content with the specified class
    with st.container():
        # Apply the welcome-container class to this container
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)

        st.markdown("""
            <style>
                .small-title {
                    font-size: 40px; /* Adjust the font size as needed */
                    font-weight: bold;
                    text-align: center;
                    color: gray;
                }
            </style>
            <div class='small-title'>WELCOME TO UCB BANK PROJECT</div>
                    """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image("images/bank.jpeg", width=400)  # Adjust the path to your logo image

        col1, col2, col3 = st.columns([4, 2, 3])
        with col2:
            if st.button('Bank Admin Login'):
                # Update the session state to trigger the login page display
                st.session_state['current_page'] = 'Login'
                st.experimental_rerun()  # Use st.rerun() if using a newer version of Streamlit

        # Close the container with the specified class
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

