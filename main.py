import streamlit as st
import os, csv
from langchain_helper import get_qa_chain, create_vector_db
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env (especially openai api key)

# Include FontAwesome CSS
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

# Check if 'is_admin' is not in session state, initialize it to False
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

with st.sidebar:
      # Add banner image
    st.image("https://raw.githubusercontent.com/msrajawat298/msrajawat298.github.io/main/images/background-images/msrajawat298_bg-min.png")
    st.header("LLM by Msrajawat298")
    st.caption("🚀 A streamlit chatbot powered by Google Plam LLM")

    "[![Google PaLM API Key](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Google_PaLM_Logo.svg/48px-Google_PaLM_Logo.svg.png) Google PaLM API Key](https://makersuite.google.com/)"
    "[![View the source code ](https://img.shields.io/github/downloads/msrajawat298/llm_by_Msrajawat298/total)](https://github.com/msrajawat298/llm_by_Msrajawat298)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/msrajawat298/llm_by_Msrajawat298?quickstart=1)"

    # Admin Controls section
    st.header("Admin Controls")
    is_admin = st.checkbox("Are you Admin ?")

    if is_admin and not st.session_state.is_admin:
        # Display login form
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")
        # Use st.button directly in the if condition for better readability
        if st.button("Login", key="login_button") and username == os.environ["ADMIN_USERNAME"] and password == os.environ["ADMIN_PASSWORD"]:
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
    # Social Media Icons
    st.header("Follow Me")
    st.markdown(
        """
        [![LinkedIn](https://img.shields.io/badge/LinkedIn-msrsajwat298-blue?style=social&logo=linkedin)](https://www.linkedin.com/in/msrsajwat298)
        """
    )
    st.markdown(
        """
        [![GitHub](https://img.shields.io/github/followers/msrajawat298?label=Follow&style=social&logo=github)](https://github.com/msrsajwat298)
        """
    )
    st.markdown(
        """
        [![YouTube](https://img.shields.io/youtube/channel/subscribers/UC325gI345WdVzDYMTxIQnqw?style=social&logo=youtube)](https://www.youtube.com/@msrajawat298)
        """
    )
    st.markdown(
        """
        [![Stack Overflow](https://img.shields.io/stackexchange/stackoverflow/r/9578353?style=social&logo=stackoverflow)](https://stackoverflow.com/users/9578353/msrajwat298)
        """
    )
    st.markdown(
        """
        [![Twitter](https://img.shields.io/twitter/follow/msrsajwat299?style=social&logo=twitter)](https://twitter.com/msrajawat299)
        """
    )
    st.markdown(
        """
        [![Blog](https://img.shields.io/badge/Read-YourBlog-red?style=social&logo=rss)](https://blog.vitabletech.in/)
        """
    )
    st.markdown(
        """
        [![Facebook](https://img.shields.io/badge/Facebook-msrajawat298-blue?style=social&logo=facebook)](https://www.facebook.com/msrajawat298)
        """
    )

st.title("🔎 Know more about Msrajawat298 Q&A  💻")
st.caption("The great aim of education is not knowledge but action. ― Herbert Spencer")

question = st.text_input("Question: ")
if "questions" not in st.session_state:
    st.session_state.questions = []

if question:
    chain = get_qa_chain()
    response = chain(question)

    st.header("Answer")
    st.write(response["result"])

    # Append the question to the list in session state
    st.session_state.questions.append(question)
    # Clear the input field after processing the question
    st.session_state.current_question = ""
    # Save the list of questions to a CSV file
    with open("questions.csv", "a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([question])