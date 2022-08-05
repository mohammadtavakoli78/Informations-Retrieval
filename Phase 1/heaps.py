import math

import pandas as pd
from hazm import *
from parsivar import Normalizer, Tokenizer, FindStems
import matplotlib.pyplot as plt

my_normalizer = Normalizer(date_normalizing_needed=True)
my_tokenizer = Tokenizer()
my_stemmer = FindStems()

df = pd.read_excel('IR1_7k_news.xlsx')

text = df['content']


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
    print(stop_words)
    input()
    for word in input_words:
        if word not in stop_words:
            news_words.append(word)

    return news_words


all_tokens = []
token_list = []
token_list2 = []
vocab_list = []
vocab_list2 = []
token = 0
vocab = 0
for counter, t in enumerate(text):
    a = normalize(t)
    words = get_tokens(t)
    words = get_steams(words)
    words = delete_stop_words(words)
    print(counter)
    all_tokens.extend(words)

    token = len(all_tokens)
    vocab = len(list(set(all_tokens)))

    # if counter in [500, 1000, 1500, 2000]:
    token_list.append(token)
    vocab_list.append(vocab)

    token_list2.append(math.log(token, 10))
    vocab_list2.append(math.log(vocab, 10))

print(token_list[-1])
print(vocab_list[-1])
plt.plot(token_list, vocab_list)
plt.plot(token_list2, vocab_list2)
plt.legend(["Dataset 1", "Dataset 2"])
plt.show()
