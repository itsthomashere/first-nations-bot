import streamlit as st
from streamlit_option_menu import option_menu

from sqlalchemy import create_engine, text
import pandas as pd

from langchain.chat_models import ChatOpenAI
from langchain.chains import QAGenerationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


st.title("Research Assistant 2.0")

user_input = st.chat_input("Send a message...", key="user_input")
