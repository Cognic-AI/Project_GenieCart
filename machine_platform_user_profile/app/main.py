import sys
import os
import jwt  # Install via `pip install PyJWT`
import streamlit as st
from datetime import datetime, timedelta

# Add the absolute path of the root directory to sys.path
sys.path.append(r"D:\\Project_GenieCart\\machine_platform_user_profile")

from app.database import get_connection
from app.queries import fetch_previous_orders, fetch_suggestions

# Secret key for encoding and decoding JWT
SECRET_KEY = "your-secret-key"  # Use a secure key in production

# Set Streamlit page configuration
st.set_page_config(page_title="User Profile", layout="wide")

# Helper function to generate a JWT token
def generate_jwt(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Helper function to verify a JWT token
def verify_jwt(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        st.error("Session expired. Please log in again.")
        return None
    except jwt.InvalidTokenError:
        st.error("Invalid token. Please log in again.")
        return None

# Simulated function to check if a user exists in the database
def user_exists(username):
    # Replace this logic with an actual database query
    return username == "test_user"

# Simulated function to register a new user
def register_user(username, password):
    # Replace this logic with an actual database insertion
    return "2"  # Simulated new user ID

# Main application function
def main():
    try:
        st.title("User Profile")

        # Check if the user is already logged in (token in query params or session state)
        token = st.experimental_get_query_params().get("token", [None])[0]
        if not token and "token" in st.session_state:
            token = st.session_state["token"]

        # If a valid token exists, verify it
        if token:
            decoded = verify_jwt(token)
            if decoded:
                user_id = decoded["user_id"]

                # User is authenticated; fetch and display their data
                st.write(f"Welcome, User ID: {user_id}")

                try:
                    # Connect to the database
                    connection = None
                    try:
                        connection = get_connection()
                        st.success("Database connection successful.")
                    except Exception as e:
                        st.error(f"Database connection failed: {e}")
                    finally:
                        if connection and connection.is_connected():
                            connection.close()

                    # Fetch previous orders
                    with st.spinner("Fetching your previous orders..."):
                        orders = fetch_previous_orders(user_id, connection)
                    st.subheader("Your Previous Orders")
                    if orders:
                        st.table(orders)
                    else:
                        st.info("You have no previous orders.")

                    # Fetch platform suggestions
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
                    if "connection" in locals() and connection.is_connected():
                        connection.close()

                # Logout button
                if st.button("Log out"):
                    st.session_state.pop("token", None)
                    st.query_params()  # Clear token from query params
                    st.experimental_rerun()

            return  # Exit the main function after user data is displayed

        # Sign in or Login form for unauthenticated users
        st.subheader("Sign In / Log In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Submit"):
            if user_exists(username):
                # Login existing user
                if username == "test_user" and password == "password123":  # Dummy credentials
                    token = generate_jwt(user_id="1")  # Replace "1" with the actual user ID from DB
                    st.session_state["token"] = token
                    st.query_params(token=token)  # Store token in query params
                    st.success("Login successful!")
                    st.experimental_rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                # Sign in new user
                user_id = register_user(username, password)
                if user_id:
                    token = generate_jwt(user_id=user_id)
                    st.session_state["token"] = token
                    st.query_params(token=token)  # Store token in query params
                    st.success("Sign-in successful! Welcome, new user.")
                    st.experimental_rerun()
                else:
                    st.error("Sign-in failed. Please try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        raise  # Re-raise the exception to view details in the terminal


if __name__ == "__main__":
    main()
