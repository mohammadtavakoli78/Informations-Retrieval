import pickle
import pandas as pd
from hazm import *
from parsivar import Normalizer, Tokenizer, FindStems

from PositionalIndexClass import *

my_normalizer = Normalizer(date_normalizing_needed=True)
my_tokenizer = Tokenizer()
my_stemmer = FindStems()

df = pd.read_excel('IR1_7k_news.xlsx')

text = df['content']

tokens_list = []

positional_dict = {}


def normalize(input_text):
    output_text = my_normalizer.normalize(input_text)
    return output_text


def get_tokens(input_text):
    words = my_tokenizer.tokenize_words(my_normalizer.normalize(input_text))
    return words


def get_steams(input_words):
    words = []
    for word in input_words:
        words.append(my_stemmer.convert_to_stem(word))
    return words


def delete_stop_words(input_words):
    news_words = []
    stop_words = stopwords_list()
    for word in input_words:
        if word not in stop_words:
            news_words.append(word)

    return news_words


for counter, t in enumerate(text):
    a = normalize(t)
    words = get_tokens(a)
    words = get_steams(words)
    words = delete_stop_words(words)
    token_dict = {"id": counter, "tokens": words}
    tokens_list.append(token_dict)

for tokens in tokens_list:
    token = tokens['tokens']
    id = tokens['id']
    for counter, t in enumerate(token):
        if t not in positional_dict:
            positional_index = PositionalIndex()
        else:
            positional_index = positional_dict.get(t)
        doc_id_list = positional_index.doc_id_list
        all_number_of_repetition = positional_index.all_number_of_repetition
        occurrences_in_one_doc = positional_index.occurrences_in_one_doc
        number_of_repetition_each_doc = positional_index.number_of_repetition_each_doc
        if id not in doc_id_list:
            doc_id = doc_id_list.copy()
            doc_id.append(id)
            positional_index.set_doc_id_list(doc_id)
        positional_index.set_all_number_of_repetition(all_number_of_repetition + 1)
        if id not in occurrences_in_one_doc:
            occurrences_in_one_doc[id] = []
            occurrences = []
            occurrences.append(counter)
            occurrences_in_one_doc[id] = occurrences

            number_of_repetition_each_doc[id] = 1

            positional_index.set_occurrences_in_one_doc(occurrences_in_one_doc)
            positional_index.set_number_of_repetition_each_doc(number_of_repetition_each_doc)
        else:
            occurrences = occurrences_in_one_doc[id]
            occurrences_temp = []
            occurrences_temp = occurrences.copy()
            occurrences_temp.append(counter)
            occurrences_in_one_doc[id] = occurrences_temp
            positional_index.set_occurrences_in_one_doc(occurrences_in_one_doc)

            number = number_of_repetition_each_doc[id]
            number_of_repetition_each_doc[id] = number + 1

            positional_index.set_number_of_repetition_each_doc(number_of_repetition_each_doc)
        positional_dict[t] = positional_index


f = open("dict2.txt", "wb")
pickle.dump(positional_dict, f)
f.close()
