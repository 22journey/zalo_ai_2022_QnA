from underthesea import text_normalize, word_tokenize
import string
import os
from core import define

SCORE_HIGHLIGHT = 3
SCORE_NORMAL = 1

MAX_TOKEN_LENGTH = 40
MIN_TOKEN_LENGTH = 2

this_dir = os.path.dirname(__file__)

def load_stopwords():
    stopwords_filename = define.STOPWORDS_FILES
    stopwords = []
    for sw in stopwords_filename:
        with open(sw, "r") as f:
            stopwords += [l.strip() for l in f]
    stopwords = set(stopwords)
    return stopwords


stopwords = load_stopwords()


def valid_token(token):
    if 'bullet' in token:
        return False
    if MIN_TOKEN_LENGTH > len(token) or len(token) > MAX_TOKEN_LENGTH:
        return False
    return True


def token_and_score(text):
    # normalize
    text = text_normalize(text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', string.digits))
    text = text.translate(str.maketrans('', '', r"-–°"))
    text = word_tokenize(text)
    d = {}
    for t in text:
        if not valid_token(t):
            continue
        s = SCORE_HIGHLIGHT if t[0].isupper() else SCORE_NORMAL
        tl = t.lower()
        if tl not in stopwords:
            d[tl] = s 
    return d