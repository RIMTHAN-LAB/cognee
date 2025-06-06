from sklearn.feature_extraction.text import TfidfVectorizer

from cognee.exceptions import InvalidValueError
from cognee.shared.utils import extract_pos_tags


def extract_keywords(text: str) -> list[str]:
    """
    Extract keywords from the provided text string.

    This function raises an InvalidValueError if the input text is empty. It processes the
    text to extract parts of speech, focusing on nouns, and uses TF-IDF to identify the most
    relevant keywords based on their frequency. The function returns a list of up to 15
    keywords, each having more than 3 characters.

    Parameters:
    -----------

        - text (str): The input text from which to extract keywords.

    Returns:
    --------

        - list[str]: A list of keywords extracted from the text, containing up to 15 nouns
          with more than 3 characters.
    """
    if len(text) == 0:
        raise InvalidValueError(message="extract_keywords cannot extract keywords from empty text.")

    tags = extract_pos_tags(text)
    nouns = [word for (word, tag) in tags if tag == "NN"]

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(nouns)

    top_nouns = sorted(
        vectorizer.vocabulary_, key=lambda x: tfidf[0, vectorizer.vocabulary_[x]], reverse=True
    )

    keywords = []

    for word in top_nouns:
        if len(word) > 3:
            keywords.append(word)
        if len(keywords) >= 15:
            break

    return keywords
