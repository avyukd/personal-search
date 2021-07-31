#create basic fastapi api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from setup import start_es
from pydantic import BaseModel
import time
from urllib.parse import urlparse

app = FastAPI()

class ExtensionDoc(BaseModel):
    selectedText: str
    url: str = None
    origin: str

#add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = None
es = start_es()

query_template = {
        "size" : 25,
        "query": {
            "query_string":{
                "query": "",
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

@app.get("/test/search")
def test_search(user_query: str):
    #fp can also be a url or a file path
    if es is not None:
        query = query_template.copy()
        query["query"]["query_string"]["query"] = user_query
        res = es.search(index="test-index", body=query)
        search_results = []
        for hit in res['hits']['hits']:
            fn = hit['_source']['filename']
            origin = hit['_source']['origin']
            if origin == "local":
                fp = hit['_id']
            elif origin == "Chrome":
                fp = hit['_source']['url']
            else:
                fp = ""
            highlights = []
            if "filename" in hit['highlight']:
                highlights += hit['highlight']['filename']
            if "content" in hit['highlight']:
                highlights += hit['highlight']['content']
            search_results.append({
                "fp": fp,
                "fn": fn,
                "origin": origin,
                "highlights": highlights
            })
        return {"search_results" : search_results, "success": True}
    else:
        return {"success": False}

#add post endpoint called test
@app.post("/test/save")
def test_post(item : ExtensionDoc):
    #filename will be url + "note"
    #separate url field will be added
    #id will be random
    content = item.selectedText
    origin = item.origin
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    date = timestamp
    url = item.url
    filename = str(urlparse(url).netloc) + " note"
    id = filename + " " + timestamp
    body = {
        "content": content,
        "origin": origin,
        "timestamp": timestamp,
        "date": date,
        "url": url,
        "filename": filename
    }

    es.index(index="test-index",id=id, body=body)

    return {"success": True}