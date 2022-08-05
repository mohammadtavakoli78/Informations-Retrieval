import pickle
from hazm import *
from parsivar import Normalizer, Tokenizer, FindStems
import pandas as pd

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['title']
text2 = df['content']

my_normalizer = Normalizer(date_normalizing_needed=True)
my_tokenizer = Tokenizer()
my_stemmer = FindStems()


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


f = open("dict.txt", "rb")
positional_dict = pickle.load(f)


def search_one_word(word):
    first_id_list = positional_dict[word].doc_id_list

    return first_id_list


def search_two_words(word1, word2):
    final_id_list = []

    first_id_list = positional_dict[word1].doc_id_list
    second_id_list = positional_dict[word2].doc_id_list

    first_occurrences_dict = positional_dict[word1].occurrences_in_one_doc
    second_occurrences_dict = positional_dict[word2].occurrences_in_one_doc

    occurrences_in_lists = set(first_id_list) & set(second_id_list)
    occurrences_in_lists = list(occurrences_in_lists)
    occurrences_in_lists.sort()

    for occurrences in occurrences_in_lists:
        first_occurrences_list = first_occurrences_dict[occurrences]
        second_occurrences_list = second_occurrences_dict[occurrences]

        for word in first_occurrences_list:
            if word + 1 in second_occurrences_list:
                final_id_list.append(occurrences)
                break

    return final_id_list


def search_n_words(words):
    final_id_list = []

    id_lists = []
    for word in words:
        id_lists.append(positional_dict[word].doc_id_list)

    positions_lists = []
    for word in words:
        positions_lists.append(positional_dict[word].occurrences_in_one_doc)

    occurrences_in_lists = []
    for counter, i in enumerate(id_lists):
        if counter == 0:
            occurrences_in_lists = set(i) & set(id_lists[1])
        else:
            occurrences_in_lists = set(i) & set(occurrences_in_lists)

    occurrences_in_lists = list(occurrences_in_lists)
    occurrences_in_lists.sort()

    for occurrences in occurrences_in_lists:

        occurrences_list = []
        for l in positions_lists:
            occurrences_list.append(l[occurrences])

        for counter, word_list in enumerate(occurrences_list):
            for word in word_list:
                check = 0
                for i in range(len(occurrences_list) - 1):
                    if word + i + 1 in occurrences_list[i + 1] and word + i in occurrences_list[i]:
                        check += 1
                if check == len(occurrences_list) - 1:
                    final_id_list.append(occurrences)
                    break


    return final_id_list


def powerset(s):
    subset = []
    x = len(s)
    for i in range(1 << x):
        subset.append([s[j] for j in range(x) if (i & (1 << j))])

    return subset


def sort_subsets(subset, len_max):
    sorted_list = []

    for i in range(len_max, 0, -1):
        for j in subset:
            if len(j) == i:
                sorted_list.append(j)

    return sorted_list


def powerset2(s):
    subset = []

    for i in range(len(s)):
        temp = []
        counter = 0
        for j in range(len(s) - i):
            temp.append(s[counter:counter + i + 1])
            counter += 1
        subset.extend(temp)
    return subset


# query = "دانشگاه صنعتی امیرکبیر"
# query = "دانشگاه امیرکبیر"
# query = "دانشگاه امیرکبیر"
# query = "واکسن آسترازنکا"
# query = "بین الملل"
query = "سازمان ملل متحد"
# query = "جمهوری اسلامی ایران"
# query = "ژیمناستیک"
# query = "ژیمناستیک"
# query = input()
a = normalize(query)
words = get_tokens(a)
words = get_steams(words)
words = delete_stop_words(words)

subsets = powerset2(words)

sorted_subsets = sort_subsets(subsets, len(query))

results = {}

len_subset = 0
last_index = 0
for counter, i in enumerate(sorted_subsets):
    if len(i) == len_subset:
        if len(i) > 1:
            prev_list = results[last_index]
            prev_list.extend(search_n_words(i))
            results[last_index] = prev_list
        else:
            prev_list = results[last_index]
            prev_list.extend(search_one_word(i[0]))
            results[last_index] = prev_list
    else:
        len_subset = len(i)
        last_index += 1
        if len(i) > 1:
            results[last_index] = search_n_words(i)
        else:
            results[last_index] = search_one_word(i[0])

final_results = {}

for key, value in results.items():
    temp_list = value
    temp_list = list(set(temp_list))
    temp_list.sort()
    final_results[key] = temp_list

final_results_title = {}

for key, value in results.items():
    temp_list = []
    for v in value:
        temp_list.append(text[v])
    final_results_title[key] = temp_list

final_id_list = []
for key, value in final_results.items():
    for v in value:
        final_id_list.append(v)

print(final_results)
for id in final_id_list[0:10]:
    print("doc_id:  "+str(id))
    print("title:  "+text[id])
    print("======================")
