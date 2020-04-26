import json
from os.path import abspath, join
import sys


def search_results(words, index):
    index_words = index['words']
    index_documents = index['documents']
    documents = {}
    if type(words) != list:
        words = [words]

    for word in words:
        actual_word = index_words[word].items()
        for document, occurence in index_words[word].items():
            if document in documents:
                documents[document] = documents[document] + occurence
            else:
                documents[document] = occurence

    retval = ""
    docs_sorted = reversed(sorted(documents.items(), key=lambda item: item[1]))
    for document, _ in docs_sorted:
        # https://stackoverflow.com/questions/1285911/how-do-i-check-that-multiple-keys-are-in-a-dict-in-a-single-pass
        if all(word in index_documents[document] for word in words):
            retval += document + "\n"

    return retval

#def search_results(search_word, index):
#    retval = ""
#    if search_word not in index:
#        retval += search_word + ': A keresett szo nem talalhato vagy tul altalanos\n'
#    else:
#        retval += search_word + ':\n'
#        for document, occurence in reversed(sorted(index[search_word].items(), key=lambda item: item[1])):
#            retval += 'Fajl\t' + document + ':\t' + str(occurence) + ' elofordulas.\n'
#    return retval

dir_path = abspath("../res/indexing")

with open(join(dir_path, 'simple_indexes.json'), 'r') as i:
    index = json.load(i)

search_words = sys.argv[1:]

search_string = ""
for word in search_words:
    search_string = search_string + word + " "

print(search_string)
print(search_results(search_words, index))
