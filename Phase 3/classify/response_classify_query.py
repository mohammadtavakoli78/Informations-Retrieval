import math
import pickle
import pandas as pd

from UtilsClass import *

df = pd.read_excel('../IR1_7k_news.xlsx')
text = df['content']
title = df['title']
url = df['url']

f = open("../dict.txt", "rb")
inverted_dict = pickle.load(f)

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


f = open("../vectors2.txt", "rb")
vectors = pickle.load(f)

f = open("test_classification.txt", "rb")
classification = pickle.load(f)

print("Enter Category:\n")
topic = input()
# query = "بین الملل"
# query = "واکسن آسترازنکا"
# query = "دانشگاه صنعتی امیرکبیر"
# query = "دانشگاه امیرکبیر"
# query = "گزارش"
# query = "استقلال"
# query = "واکسن"
# query = "قیمت نفت"
query = "ایران"
# query = "بحران"
# query = "درصد"
# query = "نرخ"
# query = "رعایت"

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

for counter, v in enumerate(vectors):
    if counter in classification[topic]:
        vector_index = v[0]
        participation = intersection(vector_index, indexes)
        point = 0
        if participation:
            for p in participation:
                point += v[1][vector_index.index(p)] * weights[indexes.index(p)]
            point = point / ((val_of_vector(v[1])) * (val_of_vector(weights)))
            point_dict = {"id": counter, "point": point}
            scores.append(point_dict)

scores = sorted(scores, key=lambda x: x['point'], reverse=True)

print(scores)
print("\n")
for score in scores[:10]:
    print("id:  " + str(score['id']))
    print("title_of_doc:  " + title[score['id']])
    print("url_of_doc:  " + url[score['id']])
    print("***********")
