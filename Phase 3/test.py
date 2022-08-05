import json
import math
import pickle
import time

import pandas as pd
import random
import numpy as np

from UtilsClass import *

f = open("dict.txt", "rb")
inverted_dict = pickle.load(f)

df = pd.read_excel('IR1_7k_news.xlsx')
text = df['content']

f = open("vectors2.txt", "rb")
weight_of_documents = pickle.load(f)

clusters = {}

new_clusters = {}
clusters_centroid_indexes = []
clusters_centroid_weights = []


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def val_of_vector(input_vector):
    temp = 0
    for input_v in input_vector:
        temp += math.pow(input_v, 2)
    temp = math.sqrt(temp)
    return temp


def init_clusters_centroids(k: int):
    documents_length = len(text)
    while len(clusters) != k:
        random_document = random.randint(0, documents_length - 1)
        if random_document not in clusters:
            clusters[random_document] = []


def assign_documents_to_clusters():
    for doc_id in range(len(weight_of_documents)):
        points = []
        if doc_id not in clusters:
            for centroid in clusters.keys():
                document_indexes = weight_of_documents[doc_id][0]
                centroid_indexes = weight_of_documents[centroid][0]
                document_weight = weight_of_documents[doc_id][1]
                centroid_weight = weight_of_documents[centroid][1]
                participation = intersection(document_indexes, centroid_indexes)
                point = 0
                if participation:
                    for p in participation:
                        point += document_weight[document_indexes.index(p)] * centroid_weight[centroid_indexes.index(p)]
                    point = point / (np.linalg.norm(document_weight) * np.linalg.norm(centroid_weight))
                    points.append(point)
        if points:
            maximum_index = np.argmax(points)
            centroid_doc_id = list(clusters)[int(maximum_index)]
            doc_list = clusters[centroid_doc_id]
            doc_list.append(doc_id)
            clusters[centroid_doc_id] = doc_list
    for counter, id in enumerate(clusters.keys()):
        doc_id_clusters = [id]
        doc_id_clusters.extend(clusters[id])
        index_cluster = []
        for doc_id in doc_id_clusters:
            index_cluster.extend(weight_of_documents[doc_id][0])
        index_cluster = list(dict.fromkeys(index_cluster))
        weight_cluster = [0] * len(index_cluster)
        for count, doc_id in enumerate(doc_id_clusters):
            for count2, index in enumerate(weight_of_documents[doc_id][0]):
                weight_cluster[index_cluster.index(index)] += weight_of_documents[doc_id][1][count2]
        weight_cluster = [x / len(weight_cluster) for x in weight_cluster]
        clusters_centroid_indexes.append(index_cluster)
        new_clusters[counter] = doc_id_clusters
        clusters_centroid_weights.append(weight_cluster)


def reassign_centroids():
    global clusters_centroid_indexes
    global clusters_centroid_weights
    global new_clusters
    cluster_keys = new_clusters.keys()
    len_documents = len(weight_of_documents)
    for doc_id in range(len_documents):
        points = []
        number_cluster = 0
        for counter, weight in enumerate(cluster_keys):
            weight = clusters_centroid_weights[counter]
            document_indexes = weight_of_documents[doc_id][0]
            centroid_indexes = clusters_centroid_indexes[counter]
            document_weight = weight_of_documents[doc_id][1]
            centroid_weight = weight
            participation = intersection(document_indexes, centroid_indexes)
            point = 0
            if doc_id in new_clusters[counter]:
                number_cluster = counter
            if participation:
                for p in participation:
                    point += document_weight[document_indexes.index(p)] * centroid_weight[centroid_indexes.index(p)]
                point = point / (np.linalg.norm(document_weight) * np.linalg.norm(centroid_weight))
                points.append(point)
        if points:
            maximum_index = np.argmax(points)
            centroid_doc_id = list(new_clusters)[int(maximum_index)]
            # number_cluster = clusters_centroid_weights[counter]
            doc_list = new_clusters[number_cluster]
            if doc_id in doc_list:
                doc_list.remove(doc_id)
            new_clusters[number_cluster] = doc_list
            doc_list = new_clusters[centroid_doc_id]
            doc_list.append(doc_id)
            new_clusters[centroid_doc_id] = doc_list
    len_new_cluster = len(new_clusters)
    clusters_centroid_indexes = []
    clusters_centroid_weights = []
    temp_clusters = {}
    for i in range(len_new_cluster):
        id = list(new_clusters)[int(i)]
        doc_id_clusters = new_clusters[id]
        index_cluster = []
        for doc_id in doc_id_clusters:
            index_cluster.extend(weight_of_documents[doc_id][0])
        index_cluster = list(dict.fromkeys(index_cluster))
        weight_cluster = [0] * len(index_cluster)
        for count, doc_id in enumerate(doc_id_clusters):
            for count2, index in enumerate(weight_of_documents[doc_id][0]):
                weight_cluster[index_cluster.index(index)] += weight_of_documents[doc_id][1][count2]
        weight_cluster = [x / len(weight_cluster) for x in weight_cluster]
        clusters_centroid_indexes.append(index_cluster)
        clusters_centroid_weights.append(weight_cluster)
        temp_clusters[i] = doc_id_clusters
    new_clusters = temp_clusters


if __name__ == "__main__":
    # init_clusters_centroids(5)
    clusters[1000] = []
    clusters[2000] = []
    clusters[3000] = []
    clusters[4000] = []
    clusters[5000] = []
    # start = time.time()
    assign_documents_to_clusters()
    # print(time.time() - start)
    for i in range(5):
        start = time.time()
        reassign_centroids()
        end = time.time()
        print(end - start)
    print()
    f = open("cluster2.txt", "wb")
    pickle.dump(new_clusters, f)
    f.close()
    f = open("clusters_centroid_weights2.txt", "wb")
    pickle.dump(clusters_centroid_weights, f)
    f.close()
    f = open("clusters_centroid_indexes2.txt", "wb")
    pickle.dump(clusters_centroid_indexes, f)
    f.close()
