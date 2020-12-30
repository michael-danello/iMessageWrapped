import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sql_queries import ALL_TEXT
import sqlite3

import pickle
import os
import re
import string

# trained with oanc data ~ 16 million words from spoken and written
# http://www.anc.org/data/oanc/download/

def get_training_text():
    """
    iterate through training data and return all text files in training data
    """
    path = "training_data"

    text_files = []
    # walking through the entire folder,
    # including subdirectories

    for folder, subfolders, files in os.walk(path):

        for file in files:
            if file.endswith(".txt"):
                text_files.append(os.path.join( folder, file))

    return text_files


def build_tfidf_model(text_files, ngram_range):
    """

    """

    tfidf_vectorizer= TfidfVectorizer(input='filename',stop_words='english', ngram_range=(ngram_range,ngram_range))
    fitted = tfidf_vectorizer.fit_transform(text_files)

    return tfidf_vectorizer


def pickle_model(model, filename):
    """
    pickles vectorizer for use in actual app
    """
    with open(filename, 'wb') as file:
        pickle.dump(model, file)


if __name__ == '__main__':

    training_text = get_training_text()

    tf_idf_model = build_tfidf_model(training_text, 1)

    print("Finished creating single model")

    tf_idf_bigram_model = build_tfidf_model(training_text, 2)

    print("Finished creating bigram model")

    pickle_model(tf_idf_model, 'tfidf_single.pickle')
    pickle_model(tf_idf_bigram_model, 'tfidf_bigram.pickle')
