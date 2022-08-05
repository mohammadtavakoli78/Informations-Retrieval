from hazm import *
from parsivar import Normalizer, Tokenizer, FindStems

my_normalizer = Normalizer(date_normalizing_needed=True)
my_tokenizer = Tokenizer()
my_stemmer = FindStems()


class Utils:
    @staticmethod
    def normalize(input_text):
        output_text = my_normalizer.normalize(input_text)
        return output_text

    @staticmethod
    def get_tokens(input_text):
        words = my_tokenizer.tokenize_words(my_normalizer.normalize(input_text))
        return words

    @staticmethod
    def get_steams(input_words):
        words = []
        for word in input_words:
            words.append(my_stemmer.convert_to_stem(word))
        return words

    @staticmethod
    def delete_stop_words(input_words):
        news_words = []
        stop_words = stopwords_list()
        for word in input_words:
            if word not in stop_words:
                news_words.append(word)

        return news_words
