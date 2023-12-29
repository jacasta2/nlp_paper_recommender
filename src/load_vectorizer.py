"""
load_vectorizer.py
    This script contains all supportinhg functions to load a vectorizer.
"""

from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


def load_tfidf_vectorizer() -> TfidfVectorizer:
    """
    This function loads the TF-IDF vectorizer fitted to abstracts from behavioral
    operations papers.

    Returns:
        model: TfidfVectorizer.
    """

    # Instantiate a Path object pointing to the project's root
    model_path = Path(Path.cwd().parent)

    # Modify the object to point to the TF-IDF vectorizer
    model_path = model_path.joinpath("models", "tfidf_model.joblib")

    # Load vectorizer
    model = joblib.load(model_path)
    return model
