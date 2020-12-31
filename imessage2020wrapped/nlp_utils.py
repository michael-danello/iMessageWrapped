import pandas as pd
import numpy as np
import nltk
# standard library
import re
import pickle
from collections import Counter

nltk.download('averaged_perceptron_tagger')

def clean_text(text):
    return re.sub(r"[^A-Za-z0-9 ']+", '', text)

def get_top_tf_idf(vectorizer, text, num = 50):

    text = clean_text(text)

    with open('chats.txt', 'w') as file:
        file.write(text)

    transformed_vector = vectorizer.transform(['chats.txt'])
    results = np.ndarray.flatten(transformed_vector[0].T.toarray())

    df = pd.DataFrame(data={"tfidf":results, "phrase":vectorizer.get_feature_names()})
    df = df.sort_values(by=["tfidf"],ascending=False)

    return list(df['phrase'][:num])

def tag_text(tokens):
    return nltk.pos_tag(tokens)

def count_pos(type, tagged_text):
    pos_counter = Counter()
    for word in tagged_text:
        if word[1] ==  type and len(word[0]) > 1:
            pos_counter[word[0]] += 1
    return pos_counter

def common_word_dict(pos_counter, num=100):
    common_words = pos_counter.most_common(num)
    return dict((k,v) for k,v in common_words)
