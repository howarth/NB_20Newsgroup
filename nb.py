import sys
import os
import re
import math
from helper_fns import *

##########################
# Open input files.
##########################
if len(sys.argv) < 7:
    print "Usage ./nb.py [data_folder], [training], [test], [result_file], [num_exclude], [m]"
    exit()

argv = sys.argv

data_folder = argv[1]
training_set_filename = argv[2]
test_set_filename = argv[3]
result_filename = argv[4]
num_excluded = int(argv[5])
m = int(argv[6])

distribution = non_uniform_dist


try:
    training_set_file = open(training_set_filename, 'r')
except:
    print "Could not open training set file. Exiting."
    exit()

try:
    test_set_file = test_set_filename = open(test_set_filename, 'r')
except:
    print "Could not open test set file. Exiting."
    exit()


#######################
# Initial variables
#######################
vocab = set()
vocab_count = {}
words_seen = 0
categories = set()
cat_bag = {}
cat_bag_count = {}


training_set = [d.rstrip() for d in training_set_file.readlines()]
test_set = [d.rstrip() for d in test_set_file.readlines()]

#############################################################
# Read through documents and create a cumulative bag of words
# for each category
#############################################################
for doc_name in training_set:
    cat = category_from_filename(doc_name)

    if cat not in categories:
        categories.add(cat)
        cat_bag[cat] = {}
        cat_bag_count[cat] = 0

    try:
        doc_file = open("/".join([data_folder, doc_name]), 'r')
    except:
        print "Could not open training file: "+"/".join([data_folder, doc_name])
        print "Exiting."
        exit()

    doc = doc_file.read()
    doc_bag = clean_and_bag(doc)

    cat_bag_count[cat] = cat_bag_count[cat] + 1

    for word in doc_bag:
        words_seen = words_seen + 1
        if word not in cat_bag[cat]:
            cat_bag[cat][word] = 0
            if word not in vocab:
                vocab.add(word)
                vocab_count[word] = 0

        cat_bag[cat][word] = cat_bag[cat][word] + 1
        vocab_count[word] = vocab_count[word] + 1

#################################################
# Calculate the necessary probabilities for NB
#################################################
prior = {}
word_count_in_cat = {}

# Initialize conditional probabilities
p = {}
for w in vocab:
    p[w] = {}



for c in categories:
    prior[c] = float(cat_bag_count[c]) / float(len(training_set))
    word_count_in_cat[c] = 0
    for v in cat_bag[cat].values():
        word_count_in_cat[c] = word_count_in_cat[c] + v


    for w in cat_bag[c].keys():
        p[w][c] = distribution(cat_bag[c][w], word_count_in_cat[c], len(vocab), m, vocab_count[w], words_seen)

#print_top_20_words(cat_bag["christian"], cat_bag["politics"])
#exit()
print_log_odds("christian", "politics", p, vocab, word_count_in_cat)
exit()
################################################
# Classify test examples
################################################
 
excluded = set()
excluded = [k for k,v in sorted(vocab_count.iteritems(), key=operator.itemgetter(1))[-num_excluded:]]

vocab = vocab.difference(excluded)

predictions = {}
for doc_name in test_set:
    #cat = category_from_filename(doc_name)

    try:
        doc_file = open(data_folder + "/" + doc_name, 'r')
    except:
        print "Could not open file: "+ doc_name
        print "Exiting."
        exit()

    doc = doc_file.read()
    doc_bag = clean_and_bag(doc)

    max_cat = ''
    max_cat_val = -10000000000000

    for c in categories:
        log_sum = 0.0  
        for w in doc_bag:
            if w in excluded:
                continue


            try:
                log_sum = log_sum + math.log(p[w][c])
            except:
                if w in vocab:
                    a =  math.log(distribution(0.0, word_count_in_cat[c], len(vocab), m, vocab_count[w], words_seen))
                    log_sum = a + log_sum
                else:
                    log_sum = log_sum + math.log(distribution(0.0, word_count_in_cat[c], len(vocab), m, 0, words_seen))
                
                
            #if w not in cat_bag[c].keys():
            #    p[w][c] = float(1) / float(word_count_in_cat[c] + len(vocab))


        if log_sum > max_cat_val:
            max_cat = c
            max_cat_val = log_sum
    
    predictions[doc_name] = max_cat

try:
    result_file = open(result_filename, 'w')
except:
    print "Could not open result file. Exiting"
    exit()

for doc, cat in predictions.items():
    result_file.write(" ".join([doc,cat, "\n"]))

result_file.close()
