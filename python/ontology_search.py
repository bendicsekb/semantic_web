import subprocess
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
        if word not in index_words:
            continue
        for document, occurence in index_words[word].items():
            if document in documents:
                documents[document] = documents[document] + occurence
            else:
                documents[document] = occurence

    retval = ""
    docs_sorted = reversed(sorted(documents.items(), key=lambda item: item[1]))
    for document, _ in docs_sorted:
        # https://stackoverflow.com/questions/1285911/how-do-i-check-that-multiple-keys-are-in-a-dict-in-a-single-pass
        if any(word in index_documents[document] for word in words):
            retval += document + "\n"

    return retval

def expand_query(word):
    # self path found in IntelliJ
    result = subprocess.run([r"C:\Program Files\Java\jdk1.8.0_251\bin\java.exe",
                             r'-Dfile.encoding=UTF-8',
                             '-classpath',
                             r"C:\Program Files\Java\jdk1.8.0_251\jre\lib\charsets.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\deploy.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\access-bridge-64.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\cldrdata.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\dnsns.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\jaccess.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\jfxrt.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\localedata.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\nashorn.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\sunec.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\sunjce_provider.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\sunmscapi.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\sunpkcs11.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\ext\zipfs.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\javaws.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\jce.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\jfr.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\jfxswt.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\jsse.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\management-agent.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\plugin.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\resources.jar;C:\Program Files\Java\jdk1.8.0_251\jre\lib\rt.jar;C:\Users\bendi\Documents\BME Mérnökinformatikus Alapképzés\6. félév\IET\HF1\semantic_web\res\query\out\production\query;C:\Users\bendi\Documents\BME Mérnökinformatikus Alapképzés\6. félév\IET\HF1\semantic_web\res\HermiT\HermiT.jar",
                             'Query_Expander', word],
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    res_s = result.stdout.decode('utf-8')
    if res_s == "\r\n":
        return word
    res_arr = [word]
    for line in res_s.strip().split("\n"):
        res_arr += line.strip().split(",")

    return res_arr

dir_path = abspath("../res/indexing")

with open(join(dir_path, 'simple_indexes.json'), 'r') as i:
    index = json.load(i)

search_words = sys.argv[1:]

search_string = ""
for word in search_words:
    search_string = search_string + word + " "

print(search_string + " az alabbi dokumentumokban")
for word in search_words:
    print("Kereso szavak: ", expand_query(word))

for word in search_words:
    expanded = expand_query(word)
    print(search_results(expanded, index))

