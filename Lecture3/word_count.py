#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 05:27:30 2021

@author: aoqu
"""
import random
import os
from collections import defaultdict
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
                    
                        word_counter[word] = 1
    return sorted(word_counter.items(), key=lambda x: x[1], reverse=True)[:n]
        

def build_markov_chain():
    global LEN
    model = defaultdict(lambda: defaultdict(int))
    with open('reviews.txt', 'r') as f:
        for index, line in enumerate(f.readlines()):
            words = line.lower().split()
            for i in range(len(words) - LEN):
                first = words[i:i+LEN]
                second = words[i+LEN]
                model[tuple(first)][second] += 1
            if index % 1000 == 0:
                print(f'Finished processing {index} reviews')
    print('Finished processing all reviews')
    
    return model

def generate_text(starting_sentence, model, max_len=30):
    global LEN
    sentence = starting_sentence.lower().split(' ')
    words = tuple(sentence[-LEN:])
    for i in range(max_len - LEN):
        if words in model:
            prob_dist = model[words]
            word = random.choices(list(prob_dist.keys()), weights=list(prob_dist.values()), k=1)[0]
            sentence.append(word)
            words = tuple([*(words[1:]), word])
        else:
            break
    return ' '.join(sentence)

def auto_complete(sentence, model):
    words = tuple(sentence.lower().split(' ')[-LEN])
    prob_dist = model[words]
    inference = sorted(prob_dist.keys(), key=lambda x: \
                       prob_dist[x], reverse=True)
    return inference[:10]
                

if __name__ == '__main__':
    top_words = get_n_top_words(20)
    for data in top_words:
        word, count = data
        print('Word: ' + word + ', Count: ' + str(count))
    LEN = 4
    markov_chain = build_markov_chain()
    print(generate_text('I am a math', markov_chain, max_len=40))
    print(generate_text('This is the hardest', markov_chain, max_len=40))
    print(generate_text('Professor Rafter is a', markov_chain, max_len=40))
    