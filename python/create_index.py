import json
import re
from os.path import isfile, join, basename, abspath
from pathlib import Path


dir_path = abspath("../res/indexing")
# https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory, https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
all_files = {f.name:f.absolute() for f in Path(dir_path).rglob('*.*') if isfile(f.absolute()) and not re.match('.*json$', f.name)}

no_index = []
f_no_index = all_files.pop('stopwords.txt')
with open(f_no_index) as f:
    for word in f:
        no_index.append(word.strip())

# example: {
# 'words': {	'john': {'document1': 3, 'document2': 5},
# 		        'doe' : {'document1': 1, 'document3': 2}},
# 'documents': {'document1': {'foo':2, 'bar':1 },
# 		        'document2':{'asd': 1, 'bsd': 5}}
# }
# index is NOT case sensitive

index = {'words':{}, 'documents':{}}
# https://stackoverflow.com/questions/16922214/reading-a-text-file-and-splitting-it-into-single-words-in-python
for _, document_path in all_files.items():
    with open(document_path, "r") as d:
        # get document name
        document = basename(document_path)
        for line in d:
            for word in line.split():
                # check if word needs to be indexed
                if word in no_index:
                    continue
                # check if word already in words index, if so increment counter, if not then add to the index
                if word in index['words']:
                    word_index = index['words'][word]
                    # check if word already indexed in the current document
                    if document in word_index:
                        word_index[document] = word_index[document] + 1
                    else:
                        word_index[document] = 1
                else:
                    index['words'][word] = {document: 1}
                # check if document already in document index, if so increment counter, if not then add to the index
                if document in index['documents']:
                    document_index = index['documents'][document]
                    # check if word already indexed in the current document
                    if word in document_index:
                        document_index[word] = document_index[word] + 1
                    else:
                        document_index[word] = 1
                else:
                    index['documents'][document] = {word: 1}

# index created, save
json = json.dumps(index)
f = open(join(dir_path, "simple_indexes.json"),"w")
f.write(json)
f.close()