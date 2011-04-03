import sys
import os
import re
import math
from helper_fns import *

##########################
# Open input files.
##########################
if len(sys.argv) < 5:
    print "Usage ./nb.py [data_folder], [training], [test], [result_file]"
    exit()

argv = sys.argv

data_folder = argv[1]
training_set_filename = argv[2]
test_set_filename = argv[3]
result_filename = argv[4]

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
    print "training: "+doc_name
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
    doc = clean(doc)
    doc_bag = doc.split(' ')

    cat_bag_count[cat] = cat_bag_count[cat] + 1

    for word in doc_bag:
        if word not in cat_bag[cat]:
            cat_bag[cat][word] = 0
            vocab.add(word)

        cat_bag[cat][word] = cat_bag[cat][word] + 1

#################################################
# Calculate the necessary probabilities for NB
#################################################

prior = {}
word_count_in_cat = {}

# Initialize conditional probabilities
p = {}
for w in vocab:
    p[w] = {}

print "Initialized vocab"


for c in categories:
    print "Computing probabilities for: " + c
    prior[c] = float(cat_bag_count[c]) / float(len(training_set))
    word_count_in_cat[c] = 0
    for v in cat_bag[cat].values():
        word_count_in_cat[c] = word_count_in_cat[c] + v

    print "Done counting words."

    for w in cat_bag[c].keys():
        p[w][c] = (cat_bag[c][w] + float(1)) / float(word_count_in_cat[c] + len(vocab))



################################################
# Classify test examples
################################################

predictions = {}
for doc_name in test_set:
    #cat = category_from_filename(doc_name)
    print "testing: "+doc_name

    try:
        doc_file = open(data_folder + "/" + doc_name, 'r')
    except:
        print "Could not open file: "+ doc_name
        print "Exiting."
        exit()

    doc = doc_file.read()
    doc = clean(doc)
    doc_bag = doc.split(' ')

    max_cat = ''
    max_cat_val = -10000000000000

    for c in categories:
        log_sum = 0  
        for w in doc_bag:
            if w not in vocab:
                continue

            try:
                log_sum = log_sum + math.log(p[w][c])
            except:
                p[w][c] = float(1) / float(word_count_in_cat[c] + len(vocab))
                log_sum = log_sum + math.log(p[w][c])
                
                
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
