import pickle
import pandas as pd

from UtilsClass import *
from InvertedIndexClass import *

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['content']

tokens_list = []
inverted_dict = {}
utils = Utils()

for counter, t in enumerate(text):
    a = utils.normalize(t)
    words = utils.get_tokens(a)
    words = utils.get_steams(words)
    words = utils.delete_stop_words(words)
    token_dict = {"id": counter, "tokens": words}
    tokens_list.append(token_dict)

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

f = open("dict.txt", "wb")
pickle.dump(inverted_dict, f)
f.close()
