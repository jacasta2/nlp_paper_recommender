"""
text_preparation.py
    This script contains all supportinhg functions to prepare text data.
"""

import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# from nltk.tokenize import word_tokenize


def nlp_preparation(abstract: str) -> str:
    """
    This function prepares an abstract or an user's input for the embedding. It removes
    punctuation from the abstract, lower cases it, removes stopwords from it and
    lemmatizes it.

    Args:
        abstract: string with the abstract content.

    Returns:
        prepared_abstract: string prepared for the embedding.
    """

    # Replace hyphens, en-dashes and em-dashes with a space
    prepared_abstract = re.sub(r"[-\u2013\u2014]", " ", abstract)

    # Remove punctuation
    prepared_abstract = prepared_abstract.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Lower case
    prepared_abstract = prepared_abstract.lower()

    # Get list of English stopwords
    english_stopwords = stopwords.words("english")

    # Tokenize text
    # tokens = word_tokenize(prepared_abstract)

    # Remove stopwords
    # text_clean = [word for word in tokens if word not in english_stopwords]
    prepared_abstract = " ".join(
        [word for word in prepared_abstract.split() if word not in english_stopwords]
    )

    # Lemmatizer object
    lemmatizer = WordNetLemmatizer()
    # Lemmatization on all rows
    prepared_abstract = " ".join(
        lemmatizer.lemmatize(word) for word in prepared_abstract.split()
    )
    # prepared_abstract = " ".join(lemmatizer.lemmatize(word) for word in text_clean)

    return prepared_abstract
    return prepared_abstract
