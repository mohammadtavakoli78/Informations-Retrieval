import math
import multiprocessing
from gensim.models import Word2Vec
import time
import numpy as np
import pandas as pd
import os
import pickle
from numpy.linalg import norm

from UtilsClass import *

scores = []


def calculate_idf(token):
    inverted = inverted_dict[token]
    number = len(text) / len(inverted.get_doc_id_list())
    return math.log(number, 10)


def check_similarity(first_doc, query_doc, doc_id):
    score = np.dot(first_doc, query_doc) / (norm(first_doc) * norm(query_doc))
    scores.append({"id": doc_id, "score": (score + 1) / 2})


f = open("dict.txt", "rb")
inverted_dict = pickle.load(f)
f.close()

f = open("vectors2.txt", "rb")
vectors = pickle.load(f)
f.close()

cores = multiprocessing.cpu_count()

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['content']
titles = df['title']

filename = dir_path = os.path.dirname(os.path.realpath(__file__)) + "\my_model.model"
w2v_model = Word2Vec.load(filename)

docs_embedding = []
for doc in vectors:
    doc_vector = np.zeros(300)
    weight_sum = 0
    indexes = doc[0]
    weights = doc[1]
    list_of_terms = list(inverted_dict)
    for index in indexes:
        term = list_of_terms[index]
        if term in w2v_model.wv:
            doc_vector += w2v_model.wv[term] * weights[indexes.index(index)]
            weight_sum += weights[indexes.index(index)]
    docs_embedding.append(doc_vector / weight_sum)

query = "دانشگاه صنعتی امیرکبیر"
# query = "واکسن"
# query = "دانشگاه ها باز شده ؟"
# query = "آیا ژیمناستیک ورزش خوبی است ؟"

utils = Utils()

a = utils.normalize(query)
words = utils.get_tokens(a)
words = utils.get_steams(words)
words = utils.delete_stop_words(words)

query_vector = np.zeros(300)
weight_sum = 0

for word in words:
    occurrence = words.count(word)
    tf = 1 + math.log(occurrence, 10)
    weight = tf * calculate_idf(word)
    if word in w2v_model.wv:
        query_vector += w2v_model.wv[word] * weight
        weight_sum += weight

query_vector = query_vector / weight_sum

for counter, doc in enumerate(docs_embedding):
    check_similarity(doc, query_vector, counter)

scores = sorted(scores, key=lambda x: x['score'], reverse=True)
for score in scores[:10]:
    print("doc_id:  " + str(score['id']))
    print("title:  " + titles[score['id']])
    print("======================")
print(scores)
