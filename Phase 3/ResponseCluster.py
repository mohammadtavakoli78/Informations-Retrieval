import math
import pickle
import time

import pandas as pd
import numpy as np

from UtilsClass import *

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['content']
titles = df['title']
url = df['url']

first_data_set = pd.read_excel('classify/IR00_3_11k News.xlsx')
second_data_set = pd.read_excel('classify/IR00_3_17k News.xlsx')
third_data_set = pd.read_excel('classify/IR00_3_20k News.xlsx')

first_text = first_data_set['content']
second_text = second_data_set['content']
third_text = third_data_set['content']

first_url = first_data_set['url']
second_url = second_data_set['url']
third_url = third_data_set['url']

all_text = []
all_text.extend(first_text)
all_text.extend(second_text)
all_text.extend(third_text)

all_url = []
all_url.extend(first_url)
all_url.extend(second_url)
all_url.extend(third_url)

f = open("classify/train_data_set_dict.txt", "rb")
inverted_dict = pickle.load(f)
f.close()

f = open("cluster2.txt", "rb")
cluster = pickle.load(f)
f.close()

f = open("clusters_centroid_indexes2.txt", "rb")
clusters_centroid_indexes = pickle.load(f)
f.close()

f = open("clusters_centroid_weights2.txt", "rb")
clusters_centroid_weights = pickle.load(f)
f.close()

scores = []
utils = Utils()


def calculate_idf(token):
    inverted = inverted_dict[token]
    number = len(all_text) / len(inverted.get_doc_id_list())
    return math.log(number, 10)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def val_of_vector(input_vector):
    return np.linalg.norm(input_vector)


f = open("classify/train_data_vectors.txt", "rb")
vectors = pickle.load(f)

# query = input()
# query = "بین الملل"
# query = "واکسن آسترازنکا"
# query = "سازمان ملل متحد"
# query = "ژیمناستیک"
# query = "فوتبال"
# query = "غذا"
# query = "دانشگاه صنعتی امیرکبیر"
# query = "استقلال آزادی"
query = "استقلال"

start = time.time()

a = utils.normalize(query)
words = utils.get_tokens(a)
words = utils.get_steams(words)
words = utils.delete_stop_words(words)
edited_words = list(dict.fromkeys(words))

weights = []
indexes = []
vector = []

for word in edited_words:
    occurrence = words.count(word)
    tf = 1 + math.log(occurrence, 10)
    weight = tf * calculate_idf(word)
    weights.append(weight)
    indexes.append(list(inverted_dict.keys()).index(word))

vector.append(weights)
vector.append(indexes)

for counter, v in enumerate(clusters_centroid_indexes):
    vector_index = v
    weight_cluster = clusters_centroid_weights[counter]
    participation = intersection(vector_index, indexes)
    point = 0
    if participation:
        for p in participation:
            point += weight_cluster[vector_index.index(p)] * weights[indexes.index(p)]
        point = point / ((val_of_vector(weight_cluster)) * (val_of_vector(weights)))
        point_dict = {"id": counter, "point": point}
        scores.append(point_dict)

scores = sorted(scores, key=lambda x: x['point'], reverse=True)

doc_id_list = []
final_score = []

for score in scores[:5]:
    id = score['id']
    doc_id = cluster[id]
    doc_id_list.extend(doc_id)

for counter, id in enumerate(doc_id_list):
    vector_index = vectors[id][0]
    participation = intersection(vector_index, indexes)
    point = 0
    if participation:
        for p in participation:
            point += vectors[id][1][vector_index.index(p)] * weights[indexes.index(p)]
        point = point / ((val_of_vector(vectors[id][1])) * (val_of_vector(weights)))
        point_dict = {"id": id, "point": point}
        final_score.append(point_dict)

final_score = sorted(final_score, key=lambda x: x['point'], reverse=True)

print(final_score)
# print("\n")
for score in final_score[:10]:
    print("doc_id:  " + str(score['id']))
    # print("title:  " + titles[score['id']])
    print("url:  " + all_url[score['id']])
    print("======================")

print(f"Total time : {time.time() - start}")