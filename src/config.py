"""
config.py
    This script loads Pinecone-related info stored in Streamlit secrets file.
"""

import streamlit as st


class Config:
    """
    Pinecone-related info.
    """

    def __init__(self):
        self.pinecone_api_key = None
        self.pinecone_environment = None
        self.pinecone_table = None


    def update_attributes(self) -> None:
        """
        Update instance attributes.
        """

        self.pinecone_api_key = st.secrets['PINECONE_API_KEY']
        self.pinecone_environment = st.secrets['PINECONE_ENVIRONMENT']
        self.pinecone_table = st.secrets['PINECONE_TABLE']
