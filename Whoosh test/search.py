from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
ix = index.open_dir("indexdir")

mparser = MultifieldParser(["filename", "tags", "content"], schema=ix.schema)
mparser.add_plugin(qparser.FuzzyTermPlugin())
#qp = QueryParser("content", schema=ix.schema)
raw_query = input("Enter query: ")
q = mparser.parse(raw_query)

with ix.searcher() as searcher:
    results = searcher.search(q)
    for result in results:
        print(result['filename'])
