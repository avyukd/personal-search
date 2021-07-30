#create basic fastapi api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from setup import start_es
app = FastAPI()

#add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = None

@app.on_event("startup")
async def startup():
    es = start_es()

@app.get("/test/search")
def test_search(query: str):
    if es is not None:
        res = es.search(index="test-index", body=query)
        search_results = []
        for hit in res['hits']['hits']:
            fp = hit['_id']
            fn = hit['_source']['filename']
            origin = hit['_source']['origin']
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