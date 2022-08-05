# <p align="center">Informations Retrieval Project (Search Engine)</p>

# Table of Contents
- [Introduction](https://github.com/mohammadtavakoli78/Informations-Retrieval#introduction)
- [First_Phase](https://github.com/mohammadtavakoli78/Informations-Retrieval#-First_Phase)
- [Second_Phase](https://github.com/mohammadtavakoli78/Informations-Retrieval#-Second_Phase)
- [Third_Phase](https://github.com/mohammadtavakoli78/Informations-Retrieval#-Third_Phase)
- [Technologies](https://github.com/mohammadtavakoli78/Informations-Retrieval#technologies)

## Introduction
In this project i implement a search engine using various algorithms like: ```tf-idf```, ```Word Embedding```, ```Inverted Index``` and also in phase three i use ```KNN``` and ```K-means``` for clustering and classifying that leads to boost speed of retrieving documents.<br>
I used two different dataset, The first one has more than 7k news and the second one has more than 50k news that i use the first one for building inverted index and i use the second dataset which has five diverse categories(```sport```, ```politics```, ```economy```, ```health``` and ```culture```) that use this dataset for labeling the news in first dataset.

## 💻 First_Phase
In this phase, i made an inverted index after ```preprocessing``` the documents. Preprocessing includes ```normalizing``` the document, ```tokenizing```, ```stemming```, ```removing stop words```. After these steps, the tokens were prepared to crate the ```inverted index```. Inverted index has the information of each term is appeard in what document and its positions in a certain one. Now it was time to answer the queries of the user. This approach was based on the order of words in the queries. If this order is found in a document, It is considered as a candidate answer preprocessing step.<br>

Sample of output:
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/image/1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/image/2.PNG)<br>

## 💻 Second_Phase
In the second phase, we have got to use ```tf-idf approach```. Our documents we represented in the vector it means for each word in the document, we calculated the weight of that word (except stoping words ...) when we face to a user query, we build the query vector and caculate the ```Cosin similarity``` to find the most similar document to that query. The result was shown in the ranking sort from the most similar to the least one.

Sample of output:
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/image/3.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/image/4.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/5/1-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/5/2-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/5/3-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%202/5/4-1.PNG)<br>

## 💻 Third_Phase
In the last phase, the number of documents became multiple. since the perform of Cosin similarity of query to each document would take a significant time, so we have to change our approach while handling query and we were using ```KNN``` and ```K-means``` algorithms to find the most like documents to queries. the number of documents were about 50K.<br>

Sample of output:
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/1-1-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/1-2-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/1-3-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/2-1-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/2-2-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/2-3-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/2-4-1.PNG)<br>
![](https://github.com/mohammadtavakoli78/Informations-Retrieval/blob/master/Phase%203/Images/2-5-1.PNG)<br>

## Technologies
Project is created with:
* Python version: 3.7

