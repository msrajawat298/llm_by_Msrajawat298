import streamlit as st
import os
from langchain_helper import get_qa_chain, create_vector_db
from dotenv import load_dotenv
from utils.customFunction import initialize_session_state, append_to_chat_history, save_to_csv, response_generator, display_social_media_icons
from utils.constant import MAIN_TITLE, CAPTION, SIDEBAR_TTILE, SIDEBAR_CAPTION
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Know more about Mayank singh kushwah | Msrajawt298",  # Change this to your desired title
    page_icon="https://raw.githubusercontent.com/msrajawat298/msrajawat298.github.io/main/images/favicon_icon-msrajawat298/favicon.ico",  # Change this to your desired favicon (emoji or URL)
    layout="wide",  # You can change the layout if needed (wide or centered)
    initial_sidebar_state="expanded",  # You can change the initial state of the sidebar
    menu_items={
        'Report a bug': "https://github.com/msrajawat298/llm_by_Msrajawat298/issues",
        # 'About': "# This is a header. This is an *extremely* cool app!"
    }
)
# Include FontAwesome CSS
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

with st.sidebar:
    # Add banner image
    st.image("https://raw.githubusercontent.com/msrajawat298/msrajawat298.github.io/main/images/background-images/msrajawat298_bg-min.png")
    st.header(SIDEBAR_TTILE)
    st.caption(SIDEBAR_CAPTION)

    "[![Google PaLM API Key](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Google_PaLM_Logo.svg/48px-Google_PaLM_Logo.svg.png) Google PaLM API Key](https://makersuite.google.com/)"
    "[![View the source code ](https://img.shields.io/github/downloads/msrajawat298/llm_by_Msrajawat298/total)](https://github.com/msrajawat298/llm_by_Msrajawat298)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/msrajawat298/llm_by_Msrajawat298?quickstart=1)"

    # Check if 'is_admin' is not in session state, initialize it to False
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

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
        # Download button for the CSV file
        st.download_button(
            label="Download Questions Bank file",
            data=open("questions.csv", 'rb').read(),
            key='download_button',
            file_name='questions.csv',
            mime='text/csv'
        )
        # Use st.button for logout
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.success("Logout successful! You are no longer an admin.")
    # Social Media Icons
    display_social_media_icons()

st.title(MAIN_TITLE)
st.caption(CAPTION)

def main():

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    if question := st.chat_input("Question: "):
        with st.chat_message("user"):
            st.markdown(question)

        chain = get_qa_chain()
        response = chain(question)

        # Add user message to chat history
        append_to_chat_history("user", question)
        append_to_chat_history("Assistant", response["result"])
        save_to_csv("user : ", question)
        save_to_csv("Assistant : ", response["result"])

        # Display user message in chat message container
        with st.chat_message("Assistant"):
            st.write_stream(response_generator(response["result"]))

if __name__ == "__main__":
    initialize_session_state()
    main()