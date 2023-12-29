"""
load_data.py
    This script contains all supportinhg functions to load and prepare papers' data.
"""

import ast
from pathlib import Path

import pandas as pd


def extract_names(data: pd.Series) -> str:
    """
    This function extracts the author names (given-name and surname). They're stored in
    a list of dictionaries, where each dictionary stores the info from an author. Note
    that the list is stored as a string.

    Args:
        data: pd.Series with strings, each containing a list of dictionaries.

    Returns:
        author_list: string with the author names. The string contains each author's
            surname and given name separated by ',', while each author is separated by
            ';'.
    """

    # Extract the list
    data_list = ast.literal_eval(data)

    # Create the string that will store the author names
    author_list = ""

    # Loop through each item (i.e., dictionary) in the list
    for item in data_list:
        author_list += item.get("surname") + ", " + item.get("given-name") + "; "

    # Remove the trailing '; '
    author_list = author_list[:-2]

    return author_list


def clean_df(results_df: pd.DataFrame) -> pd.DataFrame:
    """
    This function cleans the title, keywords, author names, journal, publication date,
    doi and abstract retrieved from the Scopus search.

    Args:
        results_df: pd.DataFrame with the Scopus search results.

    Returns:
        clean_results_df: pd.DataFrame with the clean title, keywords, author names,
            journal, publication date, doi and abstract.
    """

    # Title
    # Some titles have non-breaking spaces (NBSP). We replace them by a normal space,
    # i.e., ' '.
    # A title has 'R&amp;D', which corresponds to 'R&D'. We make the corresponding
    # replacement
    title_series = (
        results_df["dc:title"]
        .str.replace("\xa0", " ")
        .str.replace("R&amp;D", "R&D")
        .str.strip()
    )
    title_series.rename("title", inplace=True)

    # Keywords
    # A keyword has 'R&amp;D', which corresponds to 'R&D'. We make the corresponding
    # replacement
    keyword_series = results_df["authkeywords"].str.replace("R&amp;D", "R&D")
    keyword_series.rename("keywords", inplace=True)

    # Authors
    authors_series = results_df["author"].apply(extract_names)
    authors_series.rename("authors", inplace=True)

    # Journal
    # Some journals have a country name inside parentheses. We remove such info from the
    # name
    journal_series = (
        results_df["prism:publicationName"]
        .str.replace(r"\(.*\)", "", regex=True)
        .str.strip()
    )
    journal_series.rename("journal", inplace=True)

    # Publication year
    pubyear_series = results_df["prism:coverDate"].str[:4].astype(int)
    pubyear_series.rename("publication_year", inplace=True)

    # doi
    doi_series = "https://doi.org/" + results_df["prism:doi"]
    doi_series.rename("doi", inplace=True)

    # Abstract
    # Some abstracts have non-breaking spaces (NBSP). We replace them by a normal
    # space, i.e., ' '
    # Some abstracts have copyright information. We remove this info
    abstract_series = (
        results_df["dc:description"]
        .str.replace("\xa0", " ")
        .str.replace(r" (©|Copyright).*", "", regex=True)
        .str.strip()
    )
    abstract_series.rename("abstract", inplace=True)

    clean_results_df = pd.concat(
        [
            title_series,
            keyword_series,
            authors_series,
            journal_series,
            pubyear_series,
            doi_series,
            abstract_series,
        ],
        axis=1,
    )

    return clean_results_df


def load_scopus_data() -> pd.DataFrame:
    """
    This function makes use of supporting functions to prepare papers' data previously
    retrieved from a Scopus search.

    Returns:
        data: pd.DataFrame with prepared papers' data.
    """

    # Instantiate a Path object pointing to the project's root
    data_path = Path(Path.cwd().parent)

    # Modify the object to point to the scopus data
    data_path = data_path.joinpath('data', 'beops_papers.csv')

    # Load scopus data from papers
    data = pd.read_csv(data_path, index_col=0)

    # Prepare data
    data = clean_df(data)
    return data
