import math
import pickle
import pandas as pd

from UtilsClass import *

f = open("train_data_set_dict.txt", "rb")
inverted_dict = pickle.load(f)

f = open("train_data_set_tokens.txt", "rb")
tokens = pickle.load(f)

first_data_set = pd.read_excel('IR00_3_11k News.xlsx')
second_data_set = pd.read_excel('IR00_3_17k News.xlsx')
third_data_set = pd.read_excel('IR00_3_20k News.xlsx')

first_text = first_data_set['content']
second_text = second_data_set['content']
third_text = third_data_set['content']

all_text = []
all_text.extend(first_text)
all_text.extend(second_text)
all_text.extend(third_text)

vectors = []
utils = Utils()

inverted_dict_keys = list(inverted_dict.keys())

def calculate_tf(token, doc_id):
    inverted = inverted_dict[token]
    number_of_repetition_each_doc = inverted.get_number_of_repetition_each_doc()
    number_of_repetition = number_of_repetition_each_doc[doc_id]

    return 1 + math.log(number_of_repetition, 10)


def calculate_idf(token):
    inverted = inverted_dict[token]
    number = len(all_text) / len(inverted.get_doc_id_list())
    return math.log(number, 10)


def calculate_one_doc_weights(tokens, doc_id):
    weights = []
    indexes = []
    vector = []
    for token in tokens:
        tfidf = calculate_tf(token, doc_id) * calculate_idf(token)
        # tfidf = calculate_tf(token, doc_id) * 1
        weights.append(tfidf)
        indexes.append(inverted_dict_keys.index(token))
    new_indexes = list(dict.fromkeys(indexes))
    new_weights = []
    for index in new_indexes:
        new_weights.append(weights[indexes.index(index)])
    vector.append(new_indexes)
    vector.append(new_weights)
    vectors.append(vector)


for counter, t in enumerate(tokens):
    print(counter)
    calculate_one_doc_weights(t['tokens'], counter)

f = open("train_data_vectors.txt", "wb")
pickle.dump(vectors, f)
f.close()
