from setup import *

es = start_es()
while(True):
    user_input = input("Enter a search term: ")
    print("-"*80)
    query = {
        "query": {
            "query_string":{
                "query": user_input,
                "fields": ["content", "filename"]
            }
        },
        "highlight" : {
            "fields" : {
                "content" : {},
                "filename" : {}
            }
        }
    }
    res = es.search(index="test-index", body=query)
    print(res['hits']['total'])
    for hit in res['hits']['hits']:
        fn = hit['_source']['filename']
        print(fn)
        if "filename" in hit['highlight']:
            print(hit['highlight']['filename'][0])
        if "content" in hit['highlight']:
            print(hit['highlight']['content'])
