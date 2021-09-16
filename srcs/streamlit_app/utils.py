import sys
import time
import streamlit as st
from elasticsearch import exceptions
sys.path.append('srcs')
import medium


def check_and_create_index(es, index: str):
    """ checks if index exits and loads the data accordingly """
    mappings = {
        'mappings': {
            'properties': {
                'author': {'type': 'keyword'},
                'length': {'type': 'keyword'},
                'title': {'type': 'text'},
                'tags': {'type': 'keyword'},
                'content': {'type': 'text'},
            }
        }
    }
    if not safe_check_index(es, index):
        print(f'Index {index} not found. Create a new one...')
        es.indices.create(index=index, body=mappings, ignore=400)


def safe_check_index(es, index: str, retry: int = 3):
    """ connect to ES with retry """
    if not retry:
        print('Out of retries. Bailing out...')
        sys.exit(1)
    try:
        status = es.indices.exists(index)
        return status
    except exceptions.ConnectionError as e:
        print('Unable to connect to ES. Retrying in 5 secs...')
        time.sleep(5)
        safe_check_index(es, index, retry - 1)


@st.cache(show_spinner=False)
def get_story_urls_from_list(url: str, chrome: str):
    """ """
    with st.spinner('Getting story urls from list...'):
        return medium.get_story_from_list(url, chrome=chrome)


@st.cache(show_spinner=False)
def get_story_from_url(url: str, chrome: str) -> dict:
    """ """
    retry = 0
    while retry < 5:
        try:
            story = medium.Story(url)
            story.scrape(chrome=chrome)
            return story.to_dict()
        except Exception as e:
            print(e)
            time.sleep(1)
            retry += 1

    print(f'Error getting {url}')
    return {}


def index_search(es, index: str, keywords: str, filters: str, from_i: int,
                 size: int) -> dict:
    """ """
    body = {
        'query': {
            'bool': {
                'must': [
                    {
                        'query_string': {
                            'query': keywords,
                            'fields': ['content'],
                            'default_operator': 'AND',
                        }
                    }
                ],
            }
        },
        'highlight': {
            'pre_tags': ['<b>'],
            'post_tags': ['</b>'],
            'fields': {'content': {}}
        },
        'from': from_i,
        'size': size,
        'aggs': {
            'tags': {
                'terms': {'field': 'tags'}
            },
            'match_count': {'value_count': {'field': '_id'}}
        }
    }
    if filters is not None:
        body['query']['bool']['filter'] = {
            'terms': {
                'tags': [filters]
            }
        }

    res = es.search(index=index, body=body)
    # sort popular tags
    sorted_tags = res['aggregations']['tags']['buckets']
    sorted_tags = sorted(sorted_tags, key=lambda t: t['doc_count'], reverse=True)
    res['sorted_tags'] = [t['key'] for t in sorted_tags]
    return res


def index_stories(es, index: str, stories: dict):
    """ """
    with st.spinner(f'Indexing...'):
        success = 0
        for url, story in stories.items():
            try:
                # add title into content for searching
                _story = story.copy()
                _story['content'] = f"{story['title']} {' '.join(story['content'])}"
                es.index(index=index, id=url, body=_story)
                stories[url] = {'success': True, **story}
                success += 1
            except:
                stories[url] = {'success': False, **story}

    st.subheader('Results')
    st.write(f'Total={len(stories)}, {success} succeed, {len(stories) - success} failed.')
    st.write(stories)


@st.cache(show_spinner=False)
def shorten_title(title: str, limit: int = 65) -> str:
    """ Shorten the title of a story. """
    if len(title) > limit:
        title = title[:limit] + '...'

    return title


@st.cache(show_spinner=False)
def simplify_es_result(result: dict) -> dict:
    """ """
    res = result['_source']
    res['url'] = result['_id']
    # join list of highlights into a sentence
    res['highlights'] = '...'.join(result['highlight']['content'])
    # limit the number of characters in the title
    res['title'] = shorten_title(res['title'])
    return res
