import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import QAGenerationChain
from langchain.chat_models import ChatOpenAI

from llama_index import Document, ServiceContext, VectorStoreIndex, set_global_service_context, StorageContext, load_index_from_storage
from llama_index.embeddings import OpenAIEmbedding
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.llms import OpenAI
from llama_index.node_parser import SentenceSplitter
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.retrievers import VectorIndexRetriever

# def qa_main():
#     st.file_uploader("Upload a PDF file", type="pdf")

# def chat_main():
#     st.chat_input("Send a message...", key="user_input")

# def qa_list_main():
#     st.write("Sample Questions")

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

title = "Research Assistant 2.0"
title = st.markdown(
    f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True
)



# qa_bot = "Q&A Bot"
# chatbot = "Chatbot"
# qa_list = "Sample Questions"


# nav_bar = option_menu(
#     menu_title=None,
#     options=[qa_bot, chatbot, qa_list],
#     icons=["suit-heart-fill", "piggy-bank", "piggy-bank"],  # https://icons.getbootstrap.com/
#     menu_icon="menu-up",
#     default_index=1,
#     orientation="horizontal",
#     styles=None,
# )

# executable = {
#     qa_bot: qa_main,
#     chatbot: chat_main,
#     qa_list: qa_list_main,
# }
# executable[nav_bar]()
