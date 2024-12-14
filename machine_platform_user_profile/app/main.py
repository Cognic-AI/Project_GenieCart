# app/main.py

import sys
import os

# Add the absolute path of the root directory to sys.path
sys.path.append(r"D:\Project_GenieCart\machine_platform_user_profile")

import streamlit as st
from app.database import get_connection
from app.queries import fetch_previous_orders, fetch_suggestions

# Set Streamlit page configuration
st.set_page_config(page_title="User Profile", layout="wide")

# Streamlit UI
def main():
    st.title("User Profile")
    st.write("View your previous orders and platform suggestions.")

    # Simulate user login
    user_id = st.text_input("Enter your User ID", value="1")

    # Establish database connection
    try:
        connection = get_connection()
        if user_id:
            # Fetch previous orders
            with st.spinner("Fetching your previous orders..."):
                orders = fetch_previous_orders(user_id, connection)

            st.subheader("Your Previous Orders")
            if orders:
                st.table(orders)
            else:
                st.info("You have no previous orders.")

            # Fetch suggestions
            with st.spinner("Fetching platform suggestions..."):
                suggestions = fetch_suggestions(user_id, connection)

            st.subheader("Platform Suggestions")
            if suggestions:
                for suggestion in suggestions:
                    st.write(f"**{suggestion['suggested_product']}** - {suggestion['reason']}")
            else:
                st.info("No suggestions available for you.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()
