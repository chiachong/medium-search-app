import sys
import json
import urllib.parse
import streamlit as st
from elasticsearch import Elasticsearch
sys.path.append('srcs')
from streamlit_app import utils, templates

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


def main():
    st.set_page_config(page_title='Medium Search Engine')
    set_session_state()
    layout = st.sidebar.radio('', ['Search', 'Add Story'])
    st.write(templates.load_css(), unsafe_allow_html=True)
    # main layout
    if layout == 'Search':
        # load css
        st.title('Search Medium Story')
        if st.session_state.search is None:
            search = st.text_input('Enter search words:')
        else:
            search = st.text_input('Enter search words:', st.session_state.search)

        if search:
            # reset tags when receive new search words
            if search != st.session_state.search:
                st.session_state.tags = None
            # reset search word
            st.session_state.search = None
            from_i = (st.session_state.page - 1) * PAGE_SIZE
            results = utils.index_search(es, INDEX, search, st.session_state.tags,
                                         from_i, PAGE_SIZE)
            total_hits = results['aggregations']['match_count']['value']
            if total_hits > 0:
                # show number of results and time taken
                st.write(templates.number_of_results(total_hits, results['took'] / 1000),
                         unsafe_allow_html=True)
                # show popular tags
                if st.session_state.tags is not None and st.session_state.tags not in results['sorted_tags']:
                    popular_tags = [st.session_state.tags] + results['sorted_tags']
                else:
                    popular_tags = results['sorted_tags']

                popular_tags_html = templates.tag_boxes(search,
                                                        popular_tags[:10],
                                                        st.session_state.tags)
                st.write(popular_tags_html, unsafe_allow_html=True)
                # search results
                for i in range(len(results['hits']['hits'])):
                    res = utils.simplify_es_result(results['hits']['hits'][i])
                    st.write(templates.search_result(i + from_i, **res),
                             unsafe_allow_html=True)
                    # render tags
                    tags_html = templates.tag_boxes(search, res['tags'],
                                                    st.session_state.tags)
                    st.write(tags_html, unsafe_allow_html=True)

                # pagination
                if total_hits > PAGE_SIZE:
                    total_pages = (total_hits + PAGE_SIZE - 1) // PAGE_SIZE
                    pagination_html = templates.pagination(total_pages,
                                                           search,
                                                           st.session_state.page,
                                                           st.session_state.tags,)
                    st.write(pagination_html, unsafe_allow_html=True)
            else:
                # no result found
                st.write(templates.no_result_html(), unsafe_allow_html=True)

    elif layout == 'Add Story':
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
                    stories[url] = utils.get_story_from_url(url, DRIVER)
            # add stories by medium list url
            else:
                # get story urls in the given medium list
                story_urls = utils.get_story_urls_from_list(url, DRIVER)
                for i, _url in enumerate(story_urls):
                    with st.spinner(f'Getting {i + 1}/{len(story_urls)} story content...'):
                        stories[_url] = utils.get_story_from_url(_url, DRIVER)

            # index stories into elasticsearch
            utils.index_stories(es, INDEX, stories)

        if json_file is not None and add_story_json:
            data = json_file.read()
            stories = json.loads(data)
            # index stories into elasticsearch
            utils.index_stories(es, INDEX, stories)

        # result = st.selectbox('Results', list(stories.keys()))
        # with st.form('result'):
        #     story = stories[result]
        #     author = st.text_input('Author', story['author'])
        #     length = st.text_input('Length of the story', story['length'])
        #     title = st.text_input('Title', story['title'])
        #     tags = st.text_input('Tags', ', '.join(story['tags']))
        #     content = st.text_area('Content', ' '.join(story['content']))
        #     st.form_submit_button('Add', 'Check')


def set_session_state():
    """ """
    # default values
    if 'search' not in st.session_state:
        st.session_state.search = None
    if 'page' not in st.session_state:
        st.session_state.page = 1
    if 'tags' not in st.session_state:
        st.session_state.tags = None

    # get parameters in url
    para = st.experimental_get_query_params()
    if 'page' in para.keys():
        st.experimental_set_query_params()
        st.session_state.page = int(para['page'][0])
    if 'search' in para.keys():
        st.experimental_set_query_params()
        st.session_state.search = urllib.parse.unquote(para['search'][0])
    if 'tags' in para.keys():
        st.experimental_set_query_params()
        st.session_state.tags = para['tags'][0]


if __name__ == '__main__':
    main()
