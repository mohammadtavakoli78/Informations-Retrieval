import multiprocessing
from gensim.models import Word2Vec
import time
import numpy as np
import pandas as pd
import os
import pickle

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['content']

f = open("tokens.txt", "rb")
tokens_lists = pickle.load(f)

cores = multiprocessing.cpu_count()

w2v_model = Word2Vec(min_count=1,
                     window=5,
                     vector_size=300,
                     alpha=0.03,
                     workers=cores - 1,
                     sg=1)
w2v_model.build_vocab(tokens_lists)
w2v_model_vocab_size = len(w2v_model.wv)
print(w2v_model_vocab_size)

start = time.time()

w2v_model.train(tokens_lists, total_examples=w2v_model.corpus_count, epochs=20)
end = time.time()
print("{}".format(end - start))

w2v_model.save('my_model.model')
