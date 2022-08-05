import pickle
import pandas as pd

from UtilsClass import *
from InvertedIndexClass import *

first_data_set = pd.read_excel('IR00_3_11k News.xlsx')
second_data_set = pd.read_excel('IR00_3_17k News.xlsx')
third_data_set = pd.read_excel('IR00_3_20k News.xlsx')

first_text = first_data_set['content']
second_text = second_data_set['content']
third_text = third_data_set['content']

first_topic = first_data_set['topic']
second_topic = second_data_set['topic']
third_topic = third_data_set['topic']

all_text = []
all_text.extend(first_text)
all_text.extend(second_text)
all_text.extend(third_text)

all_topic = []
all_topic.extend(first_topic)
all_topic.extend(second_topic)
all_topic.extend(third_topic)

tokens_list = []
category_dict = {}
inverted_dict = {}
utils = Utils()

for counter, t in enumerate(all_text):
    a = utils.normalize(t)
    words = utils.get_tokens(a)
    words = utils.get_steams(words)
    words = utils.delete_stop_words(words)
    token_dict = {"id": counter, "tokens": words}
    tokens_list.append(token_dict)
    category_dict[counter] = all_topic[counter]

for tokens in tokens_list:
    token = tokens['tokens']
    id = tokens['id']
    for counter, t in enumerate(token):
        if t not in inverted_dict:
            inverted_index = InvertedIndex()
        else:
            inverted_index = inverted_dict.get(t)
        doc_id_list = inverted_index.doc_id_list
        all_number_of_repetition = inverted_index.all_number_of_repetition
        number_of_repetition_each_doc = inverted_index.number_of_repetition_each_doc
        if id not in doc_id_list:
            doc_id = doc_id_list.copy()
            doc_id.append(id)
            inverted_index.set_doc_id_list(doc_id)
        inverted_index.set_all_number_of_repetition(all_number_of_repetition + 1)
        if id not in number_of_repetition_each_doc:
            number_of_repetition_each_doc[id] = 1

            inverted_index.set_number_of_repetition_each_doc(number_of_repetition_each_doc)
        else:
            number = number_of_repetition_each_doc[id]
            number_of_repetition_each_doc[id] = number + 1

            inverted_index.set_number_of_repetition_each_doc(number_of_repetition_each_doc)
        inverted_dict[t] = inverted_index

f = open("train_data_set_dict.txt", "wb")
pickle.dump(inverted_dict, f)
f.close()

f = open("train_data_set_topics.txt", "wb")
pickle.dump(category_dict, f)
f.close()

