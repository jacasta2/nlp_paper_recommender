"""
streamlit_app.py
    This script contains the app's frontend. 
"""

import nltk  # Necessary to avoid Streamlit issues
import pandas as pd
import streamlit as st

nltk.download("stopwords") # Necessary to avoid Streamlit issues
nltk.download("wordnet") # Necessary to avoid Streamlit issues
# nltk.download("punkt") # Needed if working with NLTK word tokenizer. Not sure if more
# nltk downloads were going to be necessary if working with its tokenizer

from load_data import load_scopus_data
from load_vectorizer import load_tfidf_vectorizer
from text_preparation import nlp_preparation
from vector_database import pinecone_index_connection


@st.cache_data
def load_papers_data() -> pd.DataFrame:
    """
    This function loads papers' data previously retrieved and prepared from a Scopus
    search.

    Returns:
        data: pd.DataFrame with papers' data.
    """

    data = load_scopus_data()
    return data


# Use all space in the layout
st.set_page_config(layout="wide")

# App's title (since all layout is used, we need to center-align the title)
APP_TITLE = """
<h1 style='text-align: center'>Behavioral Operations paper recommender</h1>
"""
st.markdown(
    APP_TITLE,
    unsafe_allow_html=True,
)

# App's description
DESCRIPTION = """
This app asks the user what Behavioral Operations (BeOps) topic she would like to read about and then:
1. Processes her input.
2. Generates its vector embedding.
3. Connects to a Pinecone index containing vector embeddings of abstracts from BeOps \
papers.
4. Finds what abstracts are the most similar to her input. 
"""
st.markdown(DESCRIPTION)

# User's input
INPUT_LABEL = """
<p style="font-size:20px">What BeOps topic would you like to read about?</p>
"""
st.markdown(INPUT_LABEL, unsafe_allow_html=True)
text_input = st.text_input(
    "What BeOps topic would you like to read about?", label_visibility="collapsed"
)

if st.button("Run"):
    # Prepare user's input for NLP
    NLP_TEXT = nlp_preparation(text_input)

    # Load the TF-IDF vectorizer fitted with the abstracts from BeOps papers
    tfidf_vectorizer = load_tfidf_vectorizer()

    # Vectorize the user's input
    text_tfidf = tfidf_vectorizer.transform([NLP_TEXT])

    # Transform the vectorized input into a list so that it can be used as a query
    query = text_tfidf.toarray()[:].tolist()[0]

    # Connects to the vector database
    pinecone_index = pinecone_index_connection()

    # Query the vector database
    # This retrives a dictionary whose first key, 'matches', contains a list. The
    # elements of this list each contains one paper's info pulled from the vector
    # database, where this info is stored in a dictionary
    query_results = pinecone_index.query(query, top_k=10, include_metadata=True)

    st.write("The 10 papers with the most similar abstracts to your input are:")

    # Load papers' data to pull relevant info
    papers_data = load_papers_data()

    # Loop through query results to pull relevant info from resulting papers
    for i, paper in enumerate(query_results["matches"]):
        condition = papers_data["doi"] == paper["metadata"]["doi"]
        title = papers_data.loc[condition, "title"].values[0]
        journal = papers_data.loc[condition, "journal"].values[0]
        doi = papers_data.loc[condition, "doi"].values[0]
        st.write(str(i+1) + ". " + title + " | " + journal + " | ", doi)
