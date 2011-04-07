import re, string, operator, math

def no_dist(occur_in_c, words_in_c, vocab_len, m, word_count, words_seen):
    return float(occur_in_c + 1) / float(words_in_c + vocab_len)
'''<
    if word in cat_bag[cat].keys():
        return float((cat_bag[cat][word] + float(1)) / float(word_count_in_cat[cat] + len(vocab)))
    return float(1) / float(word_count_in_cat[cat] + len(vocab))
'''

def uniform_dist(occur_in_c, words_in_c, vocab_len, m, word_count, words_seen):
    return float(float(occur_in_c + float(m)/vocab_len) / float(words_in_c + m))

'''
def uniform_dist(word, cat, cat_bag, word_count_in_cat, vocab, m, vocab_count, words_seen):
    if word in cat_bag[cat].keys():
        return float((cat_bag[cat][word] + float(m/len(vocab))) / float(word_count_in_cat[cat] + m))
    return (float(m)/len(vocab)) / float(word_count_in_cat[cat] + m)
'''




def non_uniform_dist(occur_in_c, words_in_c, vocab_len, m, word_count, words_seen):
    p = float(words_in_c)/float(words_in_c + m) * float(occur_in_c)/float(words_in_c)
    return p + float(m)/float(words_in_c + m) * float(word_count + 1)/float(words_seen + vocab_len)



def category_from_filename(fname):
    return re.split('[0-9]', fname)[0]

def clean_and_bag(doc):
    #doc = re.sub(r'>.*\n', '', doc) 
    doc = re.sub(r'[%s]' % re.escape(string.punctuation), '', doc)
    doc = re.sub(r'\s', ' ', doc)
    doc = re.sub(r'\s+', ' ', doc)
    doc = doc.lower()
    return doc.split(' ')

def print_top_20_words(cat1, cat2):
    print "CATEGORY 1"
    
    a = sorted(cat1.iteritems(), key=operator.itemgetter(1))
    a = a[-20:]
    a = sorted([k for k,v in a])
    print a
    
    
    print "CATEGORY 2"
    a = sorted(cat2.iteritems(), key=operator.itemgetter(1))
    a = a[-20:]
    a = sorted([k for k,v in a])
    print a

def print_log_odds(cat1, cat2, p, vocab, word_count_in_cat):
    log_odds_cat1 = {}
    log_odds_cat2 = {}

    for w in vocab:
        if cat1 not in p[w].keys():
            p[w][cat1] = float(1) / float(word_count_in_cat[cat1] + len(vocab))
        if cat2 not in p[w].keys():
            p[w][cat2] = float(1) / float(word_count_in_cat[cat2] + len(vocab))

        log_odds_cat1[w] = math.log(p[w][cat1]/p[w][cat2])
        log_odds_cat2[w] = math.log(p[w][cat2]/p[w][cat1])

    print "Category: "+cat1
    a = sorted(log_odds_cat1.iteritems(), key=operator.itemgetter(1))
    a = a[-20:]
    a = sorted([k for k,v in a])
    print a

    print "Category: "+cat2
    a = sorted(log_odds_cat2.iteritems(), key=operator.itemgetter(1))
    a = a[-20:]
    a = sorted([k for k,v in a])
    print a

