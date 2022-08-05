import math
import pickle
import pandas as pd
import numpy as np

from UtilsClass import *
from InvertedIndexClass import *

df = pd.read_excel('../IR1_7k_news.xlsx')
text = df['content']

f = open("../vectors2.txt", "rb")
test_vectors = pickle.load(f)

f = open("../dict.txt", "rb")
test_inverted_dict = pickle.load(f)

f = open("train_data_set_dict.txt", "rb")
train_inverted_dict = pickle.load(f)

f = open("train_data_set_tokens.txt", "rb")
tokens = pickle.load(f)

f = open("train_data_set_topics.txt", "rb")
topics = pickle.load(f)

f = open("train_data_vectors.txt", "rb")
vectors = pickle.load(f)

f = open("test_data_tokens.txt", "rb")
tokens_list = pickle.load(f)

utils = Utils()

point_dict = {}

test_data_topics = {}


def calculate_tf(tf):
    return 1 + math.log(tf, 10)


def calculate_idf(idf, n):
    if n == 0:
        len_text = len(train_inverted_dict)
    else:
        len_text = len(test_inverted_dict)
    number = len_text / idf
    return math.log(number, 10)


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def val_of_vector(input_vector):
    return np.linalg.norm(input_vector)


def maxFreq(arr, n):
    res = 0
    count = 1

    for i in range(1, n):
        if arr[i] == arr[res]:
            count += 1
        else:
            count -= 1
        if count == 0:
            res = i
            count = 1

    return arr[res]


# for counter, t in enumerate(text):
#     print(counter)
#     a = utils.normalize(t)
#     words = utils.get_tokens(a)
#     words = utils.get_steams(words)
#     words = utils.delete_stop_words(words)
#     token_dict = {"id": counter, "tokens": words}
#     tokens_list.append(token_dict)
#

# for counter, doc in enumerate(tokens_list):
#     doc_tokens = doc['tokens']
#     points_list = []
#     for counter2, doc2 in enumerate(tokens):
#         train_doc_tokens = doc2['tokens']
#         intersects = intersection(doc_tokens, train_doc_tokens)
#         point = 0
#         if intersects:
#             for intersect in intersects:
#                 train_idf = len(train_inverted_dict[intersect].number_of_repetition_each_doc)
#                 train_tf = train_inverted_dict[intersect].number_of_repetition_each_doc[counter2]
#                 test_idf = train_idf
#                 test_tf = test_inverted_dict[intersect].number_of_repetition_each_doc[counter]
#                 point += calculate_tf(train_tf) * calculate_idf(train_idf, 0) * calculate_tf(test_tf) * calculate_idf(test_idf, 1)
#         point = point / (val_of_vector(vectors[counter2][1]) * val_of_vector(test_vectors[counter][1]))
#         points_list.append({'id': counter, 'point': point})
#     point_dict[counter] = points_list


for counter, doc in enumerate(tokens_list):
    print(counter)
    doc_tokens = doc['tokens']
    points_list = []
    new_token = []
    new_train_doc_id = []
    for token in doc_tokens:
        if token in train_inverted_dict:
            if len(train_inverted_dict[token].number_of_repetition_each_doc) < 200:
                new_token.append(token)
                new_train_doc_id.extend(train_inverted_dict[token].doc_id_list)
    new_train_doc_id = list(dict.fromkeys(new_train_doc_id))
    for doc_id in new_train_doc_id:
        new_train_doc = tokens[doc_id]['tokens']
        intersects = intersection(new_token, new_train_doc)
        point = 0
        if intersects:
            for intersect in intersects:
                train_idf = len(train_inverted_dict[intersect].number_of_repetition_each_doc)
                train_tf = train_inverted_dict[intersect].number_of_repetition_each_doc[doc_id]
                test_idf = train_idf
                test_tf = test_inverted_dict[intersect].number_of_repetition_each_doc[counter]
                point += calculate_tf(train_tf) * calculate_idf(train_idf, 0) * calculate_tf(test_tf) * calculate_idf(
                    test_idf, 1)
        point = point / (val_of_vector(vectors[doc_id][1]) * val_of_vector(test_vectors[counter][1]))
        points_list.append({'id': doc_id, 'point': point})
    points_list = sorted(points_list, key=lambda x: x['point'], reverse=True)

    topics_list = []
    if len(points_list) > 0:
        len_point_list = len(points_list)
        topic = topics[points_list[0]["id"]]
        if topic == "sport":
            topics_list.append("sports")
        elif topic == "political":
            topics_list.append("politics")
        else:
            topics_list.append(topic)
        if len_point_list > 1:
            topic = topics[points_list[1]["id"]]
            if topic == "sport":
                topics_list.append("sports")
            elif topic == "political":
                topics_list.append("politics")
            else:
                topics_list.append(topic)
        if len_point_list > 2:
            topic = topics[points_list[2]["id"]]
            if topic == "sport":
                topics_list.append("sports")
            elif topic == "political":
                topics_list.append("politics")
            else:
                topics_list.append(topic)

        max_term = maxFreq(topics_list, len(topics_list))
        topic_list = []
        if max_term in test_data_topics:
            topic_list = test_data_topics[max_term]
        topic_list.append(counter)
        test_data_topics[max_term] = topic_list

    point_dict[counter] = points_list

f = open("test_classification.txt", "wb")
pickle.dump(test_data_topics, f)
f.close()

f = open("test_all_points.txt", "wb")
pickle.dump(point_dict, f)
f.close()

print()