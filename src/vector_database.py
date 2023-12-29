"""
vector_database.py
    This script contains all supportinhg functions to connect to Pinecone.
"""

import pinecone

from config import Config


def pinecone_index_connection() -> pinecone.Index:
    """
    This function connects to the Picone API and returns a pointer to the index
    containing the vector embeddings of abstracts from behavioral operations papers.

    Returns:
        index: pinecone.Index pointer to index containing the vector embeddings of
            abstracts from behavioral operations papers.
    """

    my_config = Config()
    my_config.update_attributes()

    pinecone.init(
        api_key=my_config.pinecone_api_key, environment=my_config.pinecone_environment
    )

    index = pinecone.Index(my_config.pinecone_table)
    return index
