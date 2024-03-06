import streamlit as st
import os, csv, time
from utils.constant import SOCIAL_LINKS

def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

def append_to_chat_history(role, content):
    st.session_state.chat_history.append({"role": role, "content": content})

def save_to_csv(role, content):
    with open("questions.csv", "a", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([role, content])

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def display_social_media_icons():
        st.header("Follow Me")
        for link in SOCIAL_LINKS:
            st.markdown(f"[![{link['name']}]( {link['badge']} )]({link['url']})")
