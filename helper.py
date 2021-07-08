import os

from gensim.models import KeyedVectors, FastText
from gensim import utils
import gensim.downloader as api
import fasttext.util

from config import *
from threading import Thread

async def download_pretrained_gensim_model(name : str) -> None:
    if os.path.exists(INFO["model"]["filename"]):
        # Already downloaded
        print("Found Model already as a download")
        await load_word2vec_model()
        return 

    INFO["model"]["available"] = "downloading"
    INFO["model"]["in_memory"] = False

    # Download and Save Model
    print("Downloading pretrained gensim model...")
    OBJECTS["WORD2VEC_MODEL"] = api.load(name)
    OBJECTS["WORD2VEC_MODEL"].save(INFO["model"]["filename"])
    print("Got model locally and in_memory!")

    INFO["model"]["available"] = True
    INFO["model"]["in_memory"] = True


async def download_pretrained_fasttext_model(lang : str) -> None:
    INFO["model"]["available"] = "downloading"
    INFO["model"]["in_memory"] = False

    if os.path.exists(INFO["model"]["filename"]):
        # Already a perfect model
        print("Found Model already in a valid format!")
        await load_word2vec_model()
        return 
        
    if not os.path.exists(f"cc.{lang}.300.bin"):
        # Download now
        print("Downloading pretrained fasttext model...")
        fasttext.util.download_model(lang, if_exists='ignore')
        print("Donwload complete.")
    
    OBJECTS["WORD2VEC_MODEL"] = FastText.load_fasttext_format(f"cc.{lang}.300.bin").wv
    print("Got model now in_memory!")
    
    INFO["model"]["available"] = True
    INFO["model"]["in_memory"] = True

    # Save Model in another Thread
    if not os.path.exists(INFO["model"]["filename"]):
        t = Thread(target=OBJECTS["WORD2VEC_MODEL"].save, args=(INFO["model"]["filename"],))
        t.start()

async def load_word2vec_model():
    INFO["model"]["available"] = "downloading"
    INFO["model"]["in_memory"] = False

    OBJECTS["WORD2VEC_MODEL"] = KeyedVectors.load(INFO["model"]["filename"])
    print("Got model now in_memory!")

    INFO["model"]["available"] = True
    INFO["model"]["in_memory"] = True
