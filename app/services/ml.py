import yake
import re


# Basic ML classification of logs
def get_tags(msg: str) -> list:
    kw_extractor = yake.KeywordExtractor(n=1, top=5)
    # For YAKE: the lower the score, the higher the relevance
    # keywords is a list of (immutable) tuples (keyword, score). Tuples are arrays in Python, but cannot be altered
    keywords = kw_extractor.extract_keywords(msg)
    tags = []
    seen = set()  # to avoid duplicates
    # kw gets the first element of the tuple (string), score gets the second (float)
    for kw in keywords:
        keyword = kw[0]  # extract the keyword from the tuple
        # split by dot or underscore
        # re - regular expressions
        parts = re.split(r"[._]", keyword)
        for p in parts:
            word = re.sub(r"[^a-zA-Z0-9]", "", p).lower()
            if word not in seen:
                tags.append(word)
                seen.add(word)
    return tags
