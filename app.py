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


# connect_to_table()

title = "Research Assistant 2.0"
title = st.markdown(
    f"<h1 style='text-align: center;'>{title}</h1>", unsafe_allow_html=True
)

# define LLM
service_context = ServiceContext.from_defaults(
    llm=OpenAI(model="gpt-4", temperature=1.0, max_tokens=700)
)

# Load knowledge base from disk
index = load_index_from_storage(StorageContext.from_defaults(persist_dir="storage"))

# Configure retriever
retriever = VectorIndexRetriever(
index=index,
similarity_top_k=5  # Modify this value to change top K retrievals
)
instructions = " Present your answer in bullet form and provide the page reference after each statement."

query = st.chat_input("Enter a question: ")
if query is not None:
    retrieved_nodes = retriever.retrieve(query + instructions)
    st.write(retrieved_nodes)
    sources = [node.metadata.get('document_id') for node in retrieved_nodes]
    # sources = [node.metadata.get('document_id', 'Unknown Source') for node in retrieved_nodes]

    response = index.as_query_engine(streaming=True).query(query + instructions)
    # response = query_engine.query(query + instructions)
    response.print_response_stream()
    st.write(response)
    for node in response.source_nodes:
        print("-----")
        text_fmt = node.node.get_content().strip().replace("\n", " ")[:1000]
        # print(f"Text:\t {text_fmt} ...")
        # print(f"Metadata:\t {node.node.metadata}")
        # print out the page number and the metadata
        st.write(f"Title:\t {node.node.metadata.get('title')}")
        st.write(f"Page:\t {node.node.metadata.get('page_number')}")
        st.write(f"Score:\t {node.score:.3f}")
    # print(response.get_formatted_sources())
