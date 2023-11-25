import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

# Hardcoded admin credentials (replace these with your actual admin credentials)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Check if 'is_admin' is not in session state, initialize it to False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

st.title("Know more about Msrajawat298 Q&A  💻")

# Use st.checkbox for a better UI for admin check
is_admin = st.checkbox("Are you Admin ?")

if is_admin and not st.session_state.is_admin:
    # Display login form
    username = st.text_input("Username:")
    password = st.text_input("Password:", type="password")
    # Use st.button directly in the if condition for better readability
    if st.button("Login", key="login_button") and username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        st.session_state.is_admin = True
        st.success("Login successful! You are now an admin.")

if st.session_state.is_admin:
    # Display the "Create Knowledgeable" button only if the user is an admin
    if st.button("Create Knowledgeable"):
        create_vector_db()

    # Use st.button for logout
    if st.button("Logout"):
        st.session_state.is_admin = False
        st.success("Logout successful! You are no longer an admin.")

question = st.text_input("Question: ")

if question:
    chain = get_qa_chain()
    response = chain(question)

    st.header("Answer")
    st.write(response["result"])
