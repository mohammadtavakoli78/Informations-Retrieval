import itertools
import math
import pickle
import pandas as pd

from UtilsClass import *

f = open("dict.txt", "rb")
inverted_dict = pickle.load(f)

df = pd.read_excel('IR1_7k_news.xlsx')

text = df['content']
titles = df['title']
print(df['url'][2793])
title_list = []

scores = []
utils = Utils()


def calculate_idf(token):
    inverted = inverted_dict[token]
    number = len(text) / len(inverted.get_doc_id_list())
    return math.log(number, 10)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def val_of_vector(input_vector):
    temp = 0
    for input_v in input_vector:
        temp += math.pow(input_v, 2)
    temp = math.sqrt(temp)
    return temp


f = open("vectors2.txt", "rb")
vectors = pickle.load(f)

# query = input()
# query = "واکسن"
# query = "دانشگاه صنعتی امیرکبیر"
# query = "ژیمناستیک"
# query = "مرکز روابط عمومی"
# query = "دانشگاه ها باز شده ؟"
query = "آیا ژیمناستیک ورزش خوبی است ؟"

a = utils.normalize(query)
words = utils.get_tokens(a)
words = utils.get_steams(words)
words = utils.delete_stop_words(words)
edited_words = list(dict.fromkeys(words))

weights = []
indexes = []
vector = []
champion_dict = {}

for word in edited_words:
    occurrence = words.count(word)
    tf = 1 + math.log(occurrence, 10)
    weight = tf * calculate_idf(word)
    weights.append(weight)
    indexes.append(list(inverted_dict.keys()).index(word))

    for key, value in inverted_dict[word].get_number_of_repetition_each_doc().items():
        if key in champion_dict:
            champion_dict[key] += value
        else:
            champion_dict[key] = value

vector.append(weights)
vector.append(indexes)

champion_dict = {k: v for k, v in sorted(champion_dict.items(), key=lambda item: item[1], reverse=True)}

# champion_dict = dict(itertools.islice(champion_dict.items(), 10))

for key, value in champion_dict.items():
    v = vectors[key]
    vector_index = v[0]
    participation = intersection(vector_index, indexes)
    point = 0
    if participation:
        for p in participation:
            point += v[1][vector_index.index(p)] * weights[indexes.index(p)]
        point = point / ((val_of_vector(v[1])) * (val_of_vector(weights)))
        point_dict = {"id": key, "point": point}
        scores.append(point_dict)

scores = sorted(scores, key=lambda x: x['point'], reverse=True)
for score in scores[:10]:
    print("doc_id:  " + str(score['id']))
    print("title:  " + titles[score['id']])
    print("======================")
print(scores)
