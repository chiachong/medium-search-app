import os
import sys
import urllib.parse
import streamlit as st
from elasticsearch import Elasticsearch
sys.path.append('srcs')
from streamlit_app import utils, templates
from streamlit_app.pages import add_story, search

INDEX = 'medium_data'
PAGE_SIZE = 5
DOMAIN = 'es'
# DOMAIN = '0.0.0.0'
PORT = 9200
DRIVER = '/usr/local/bin/chromedriver'
# DRIVER = 'chromedriver_linux64/chromedriver'
# docker run --rm -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.11.2
es = Elasticsearch(host=DOMAIN)
utils.check_and_create_index(es, INDEX)

os.environ['INDEX'] = INDEX
os.environ['PAGE_SIZE'] = str(PAGE_SIZE)
os.environ['DOMAIN'] = DOMAIN
os.environ['DRIVER'] = DRIVER


def set_session_state():
    """ """
    # default values
    if 'search' not in st.session_state:
        st.session_state.search = None
    if 'tags' not in st.session_state:
        st.session_state.tags = None
    if 'page' not in st.session_state:
        st.session_state.page = 1

    # get parameters in url
    para = st.experimental_get_query_params()
    if 'search' in para:
        st.experimental_set_query_params()
        st.session_state.search = urllib.parse.unquote(para['search'][0])
    if 'tags' in para:
        st.experimental_set_query_params()
        st.session_state.tags = para['tags'][0]
    if 'page' in para:
        st.experimental_set_query_params()
        st.session_state.page = int(para['page'][0])


def main():
    st.set_page_config(page_title='Medium Search Engine')
    set_session_state()
    layout = st.sidebar.radio('', ['Search', 'Add Story'])
    st.write(templates.load_css(), unsafe_allow_html=True)
    # switch between pages
    if layout == 'Search':
        search.app()
    elif layout == 'Add Story':
        add_story.app()


if __name__ == '__main__':
    main()
