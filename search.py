from whoosh import index
from whoosh.qparser import QueryParser

ix = index.open_dir("indexdir")

qp = QueryParser("content", schema=ix.schema)
raw_query = input("Enter query: ")
q = qp.parse(raw_query)

with ix.searcher() as searcher:
    results = searcher.search(q)
    for result in results:
        print(result)