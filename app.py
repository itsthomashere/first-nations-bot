import streamlit as st
from streamlit_option_menu import option_menu

from sqlalchemy import create_engine, text
import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.chains import QAGenerationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

def qa_main():
    st.file_uploader("Upload a PDF file", type="pdf")

def chat_main():
    st.chat_input("Send a message...", key="user_input")

def connect_to_table() -> None:
    conn = st.connection("digitalocean", type="sql")
    with conn.session as s:
        if table_exists := s.execute(
            text(
                """
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'pdf_content'
            );
        """
            )
        ).scalar():
            st.write("Connected to 'pdf_content' table.")
        else:
            st.write("Table 'pdf_content' does not exist.")


connect_to_table()
st.title("Research Assistant 2.0")

qa_bot = "Q&A Bot"
chatbot = "Chatbot"


nav_bar = option_menu(
    menu_title=None,
    options=[qa_bot, chatbot],
    icons=["suit-heart-fill", "piggy-bank"],  # https://icons.getbootstrap.com/
    menu_icon="menu-up",
    default_index=0,
    orientation="horizontal",
    styles=None,
)

executable = {
    qa_bot: qa_main(),
    chatbot: chat_main(),
}

executable[nav_bar]()
