import os
import sys
import json
import streamlit as st
from elasticsearch import Elasticsearch
sys.path.append('srcs')
from streamlit_app import utils, templates


def app():
    """ page for adding medium story """
    index = os.environ['INDEX']
    domain = os.environ['DOMAIN']
    driver = os.environ['DRIVER']
    es = Elasticsearch(host=domain)
    st.title('Add Story')
    st.write(templates.info_add_story(), unsafe_allow_html=True)
    with st.expander('By URL'):
        st.write(templates.info_add_url(), unsafe_allow_html=True)
        url = st.text_input('Enter medium story or list url:')
        url_type = st.radio('Url type:', ['story', 'list'])
        add_story_url = st.button('Add', 'submit_add_story_url')

    with st.expander('By JSON'):
        st.write('JSON file containing one or more stories with format:')
        st.write({
            '$STORY_URL': {
                'author': '$AUTHOR_NAME',
                'length': '$INT min read',
                'title': '$STORY_TITLE',
                'tags': ['$TAG-NAME', ],
                'content': ['$PARAGRAPH_TEXT', ]
            },
        })
        json_file = st.file_uploader('Upload a .json file', ['json'])
        add_story_json = st.button('Add', 'submit_add_story_json')

    if add_story_url:
        stories = {}
        # add story by medium story url
        if url_type == 'story':
            with st.spinner('Getting 1 story content...'):
                stories[url] = utils.get_story_from_url(url, driver)
        # add stories by medium list url
        else:
            # get story urls in the given medium list
            story_urls = utils.get_story_urls_from_list(url, driver)
            for i, _url in enumerate(story_urls):
                with st.spinner(f'Getting {i + 1}/{len(story_urls)} story content...'):
                    stories[_url] = utils.get_story_from_url(_url, driver)

        # index stories into elasticsearch
        utils.index_stories(es, index, stories)

    if json_file is not None and add_story_json:
        data = json_file.read()
        stories = json.loads(data)
        # index stories into elasticsearch
        utils.index_stories(es, index, stories)

    # result = st.selectbox('Results', list(stories.keys()))
    # with st.form('result'):
    #     story = stories[result]
    #     author = st.text_input('Author', story['author'])
    #     length = st.text_input('Length of the story', story['length'])
    #     title = st.text_input('Title', story['title'])
    #     tags = st.text_input('Tags', ', '.join(story['tags']))
    #     content = st.text_area('Content', ' '.join(story['content']))
    #     st.form_submit_button('Add', 'Check')
