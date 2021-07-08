# WordVec API
This repo contains my docker image of an API which converts words to vectors. For that, it depends on gensim and facebook's fasttext implementation of word2vec. To run the API by your own:

- `[1] docker pull christopher2002/wordvec-api:latest` 
- `[2] docker run -d --name api-container -p 8000:8000 christopher2002/wordvec-api:latest -gensim_model glove-wiki-gigaword-50` 

You have to enter a pretrained model name (Currently the glove gigaword model is selected with a vector/embedding size of 50). An overview for gensim's pretrained models is [here](https://fasttext.cc/docs/en/crawl-vectors.html) available. To get a fasttext model, change `-gensim_model ...` to `-fasttext_model lang`. Replace lang with one of the country codes [here](https://fasttext.cc/docs/en/crawl-vectors.html) listed. German is de; English is en and so on...


<br/>



## API Methods
Vectors will always be base64 encoded and have to be decoded and then parsed. Another documentation and testing platform is running at `http://127.0.0.1:8000/docs` (SwaggerUI).
- [GET] Get Vector of one Word: `curl --location --request GET 'http://127.0.0.1:8000/vector?w=hello'`
- [POST] Get Vector of multiple Words: `curl --location --request POST 'http://127.0.0.1:8000/vector' --header 'Content-Type: application/json' --data-raw '[ "hello", "world" ]'`
- [GET] Most Similar with one word: `curl --location --request GET 'http://127.0.0.1:8000/most-similar?w=hello'`
- [POST] Most Similar with muliple words: `curl --location --request POST 'http://127.0.0.1:8000/most-similar'--header 'Content-Type: application/json'--data-raw '[ "hello", "world" ]'`
- [GET] Similarity between two words: `curl --location --request GET 'http://127.0.0.1:8000/similarity?w1=hello&w2=world'`


<br/>

## Custom Model
If you want to deploy your own model, you can simple pull this github repo and then copy your Word2Vec-Model (Keyed-Vectors Format) inside this folder. Finally rebuild the docker image and run the docker run command with the model-name:
- Clone Repo: `[1] git clone https://github.com/Christopher-06/wordvec-api.git`
- Change Directory: `[2] cd wordvec-api`
- Copy now your model inside this folder
- Build Docker Image: `[3] docker build -t wordvec-api:latest .`
- Run Container: `[4] docker run -d --name api-container -p 8000:8000 wordvec-api:latest -model_filepath [YOUR MODEL NAME]`