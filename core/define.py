from os.path import dirname as dn, join as jn

this_folder = dn(__file__)

# Context data
CONTEXT_CLEANED_FILE = jn(this_folder, "../data/wikipedia_20220620_cleaned/wikipedia_20220620_cleaned.jsonl")
CONTEXT_PARTIALS_FOLDER = jn(this_folder, "../data/wikipedia_20220620_cleaned/partials")
CONTEXT_FOLDER = jn(this_folder, "../data/context")

# TOKEN
STOPWORDS_FILES = [
    jn(this_folder, "./data/stop_words.txt"),
    jn(this_folder, "./data/stop_words_2.txt"),
]