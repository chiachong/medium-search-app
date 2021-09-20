# medium-search-app
A simple search engine to search medium stories built with streamlit and elasticsearch. 
The demo of this app is available on [Heroku](https://medium-search-app.herokuapp.com/).

## Prepare Environments
The codes were tested and ran on Ubuntu 18.04 using python 3.7. 
Create and set up a python environment by running the following command in the terminal
```
# create python venv and install libraries in the requirements.txt
source ./create_env
```

## Docker
Since this app depends on the elasticsearch container, it is preferable to use docker compose. 
Before getting started, let's build the docker container of this app
```
docker build -t medium-search-app .
```
Then use docker compose:
```
source env/bin/activate
docker-compose up
# the webapp should be available in localhost:8501
```
