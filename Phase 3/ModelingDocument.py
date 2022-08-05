import math
import pickle
import pandas as pd

from UtilsClass import *

f = open("dict.txt", "rb")
inverted_dict = pickle.load(f)

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['content']

vectors = []
utils = Utils()


def calculate_tf(token, doc_id):
    inverted = inverted_dict[token]
    number_of_repetition_each_doc = inverted.get_number_of_repetition_each_doc()
    number_of_repetition = number_of_repetition_each_doc[doc_id]

    return 1 + math.log(number_of_repetition, 10)


def calculate_idf(token):
    inverted = inverted_dict[token]
    number = len(text) / len(inverted.get_doc_id_list())
    return math.log(number, 10)


def calculate_one_doc_weights(tokens, doc_id):
    weights = []
    indexes = []
    vector = []
    for token in tokens:
        # tfidf = calculate_tf(token, doc_id) * calculate_idf(token)
        tfidf = calculate_tf(token, doc_id) * 1
        weights.append(tfidf)
        indexes.append(list(inverted_dict.keys()).index(token))
    new_indexes = list(dict.fromkeys(indexes))
    new_weights = []
    for index in new_indexes:
        new_weights.append(weights[indexes.index(index)])
    vector.append(new_indexes)
    vector.append(new_weights)
    vectors.append(vector)


for counter, t in enumerate(text):
    a = utils.normalize(t)
    words = utils.get_tokens(a)
    words = utils.get_steams(words)
    words = utils.delete_stop_words(words)
    calculate_one_doc_weights(words, counter)
    print(counter)

f = open("vectors2.txt", "wb")
pickle.dump(vectors, f)
f.close()
