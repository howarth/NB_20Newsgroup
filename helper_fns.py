import re, string

def category_from_filename(fname):
    return re.split('[0-9]', fname)[0]

def clean(doc):
    doc = re.sub(r'[%s]' % re.escape(string.punctuation), '', doc)
    doc = re.sub(r'\s', ' ', doc)
    doc = re.sub(r'\s+', ' ', doc)
    doc = doc.lower()
    return doc

