from setup import *
from utils import *
import os
from elasticsearch import Elasticsearch, helpers
import configparser

def index_local_documents(es, ROOT, INDEX, debug=False):        
    cnt = 0
    for path, directories, files in os.walk(ROOT):
        for file in files:
            fp = os.path.join(path, file)
            extension = os.path.splitext(fp)[1].lower()
            if extension in TEXT_EXTENSIONS:
                body = extract_info_local(fp)
                if body is not None:
                    res = es.index(index=INDEX, body=body, id=fp)
                    cnt+=1
                    if debug:
                        print("-"*80)
                        print(str(cnt) + " FILE INDEXED")
                        print(fp)
                        print(res['result'])

test_path = r"C:/Users/avyuk/Downloads"
test_index = "test-index"
es = start_es()
index_local_documents(es, test_path, test_index, debug=True)

