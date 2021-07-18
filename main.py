import argparse
import base64

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from config import *
import helper

parser = argparse.ArgumentParser(description='Startup Arguments for word2vec-api')
parser.add_argument("-model_url", help="URL to download the word2vec model")
parser.add_argument("-model_filepath", help="Filepath to the word2vec model")
parser.add_argument("-gensim_model", help="Name of pretrained gensim model")
parser.add_argument("-fasttext_model", help="Lang of pretrained fasttext model")

app = FastAPI(
    title="Word2Vec API",
    description="Simple API Interface to get word-vectors by yours model!",
    version="0.2.6"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    args = parser.parse_args()

    if args.model_filepath:
        INFO["model"]["filename"] = args.model_filepath

    if args.model_url:
        await helper.download_word2vec_model(args.model_url)

    if args.gensim_model:
        await helper.download_pretrained_gensim_model(args.gensim_model)

    if args.fasttext_model:
        await helper.download_pretrained_fasttext_model(args.fasttext_model)


    # Load model (if not already happened)
    if OBJECTS["WORD2VEC_MODEL"] is None:
        await helper.load_word2vec_model()    
    

@app.get("/")
async def root():
    return INFO

# ***   GET METHODS   ***
@app.get("/vector")
async def get_vector(w : str):
    '''Get one Vector of one Word'''
    if OBJECTS["WORD2VEC_MODEL"] is None:
        # Model is not in_memory
        return {"status" : "failed", "msg" : "No word2vec model is loaded"}

    try:
        vector = OBJECTS["WORD2VEC_MODEL"].get_vector(w)
        return {
            "status" : "ok", 
            "vector" : base64.b64encode(vector)
            }
    except:
        return {"status" : "failed", "msg" : f"Key {w} is not present"}

@app.get("/most-similar")
async def get_most_similar(w : str):
    '''Get similar words of the input w'''
    if OBJECTS["WORD2VEC_MODEL"] is None:
        # Model is not in_memory
        return {"status" : "failed", "msg" : "No word2vec model is loaded"}

    try:
        return {
            "status" : "ok", 
            "similar" : OBJECTS["WORD2VEC_MODEL"].most_similar(w)
            }
    except:
        return {"status" : "failed", "msg" : f"Key {w} is not present"}

@app.get("/similarity")
async def get_similarity(w1 : str, w2 : str):
    '''Calculate how similar two individual words are'''
    if OBJECTS["WORD2VEC_MODEL"] is None:
        # Model is not in_memory
        return {"status" : "failed", "msg" : "No word2vec model is loaded"}

    try:
        similarity = OBJECTS["WORD2VEC_MODEL"].similarity(w1, w2)
        return {"status" : "ok", "similarity" : similarity.astype(float)}
    except:
        return {"status" : "failed", "msg" : f"Key {w1} or {w2} is not present"}


# ***   POST METHODS   ***
@app.post("/vector")
async def post_vector(words : List[str]):
    '''Get one Vector for many words'''
    if OBJECTS["WORD2VEC_MODEL"] is None:
        # Model is not in_memory
        return {"status" : "failed", "msg" : "No word2vec model is loaded"}

    vectors = {}
    for w in words:
        try:
            vectors[w] = base64.b64encode(OBJECTS["WORD2VEC_MODEL"].get_vector(w))
        except:
            continue # Not Found

    return {"status" : "ok", "vectors" : vectors}

@app.post("/most-similar")
async def post_most_similar(words : List[str]):
    '''Get similar words of the input words'''
    if OBJECTS["WORD2VEC_MODEL"] is None:
        # Model is not in_memory
        return {"status" : "failed", "msg" : "No word2vec model is loaded"}

    similars = {}
    for w in words:
        try:
            similars[w] = OBJECTS["WORD2VEC_MODEL"].most_similar(w)
        except:
            continue # Not Found
    
    return {"status" : "ok", "similar" : similars}




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)