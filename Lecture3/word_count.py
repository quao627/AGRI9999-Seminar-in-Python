#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 05:27:30 2021

@author: aoqu
"""

from nltk.corpus import stopwords 
stopwords = set(stopwords.words('english')) 

def get_n_top_words(n=10):
    word_counter = dict()
    with open('reviews.txt', 'r') as f:
        for line in f.readlines():
            words = line.split(' ')
            for word in words:
                if word not in stopwords:
                    if word in word_counter:
                        word_counter[word] += 1
                    else:
                        word_counter[word] = 1
    return sorted(word_counter.items(), key=lambda x: x[1], reverse=True)[:n]

if __name__ == '__main__':
    top_words = get_n_top_words(20)
    for data in top_words:
        word, count = data
        print('Word: ' + word + ', Count' + str(count))
    