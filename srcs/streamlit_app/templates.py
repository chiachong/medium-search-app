import urllib.parse


def info_add_json() -> str:
    """ """
    return """
        <div>
            JSON file containing information like:<br>
            {<br>
                &emsp;&emsp;'$STORY_URL': {<br>
                    &emsp;&emsp;&emsp;&emsp;'author': '$AUTHOR_NAME',<br>
                    &emsp;&emsp;&emsp;&emsp;'length': '$INT min read',<br>
                    &emsp;&emsp;&emsp;&emsp;'title': '$STORY_TITLE',<br>
                    &emsp;&emsp;&emsp;&emsp;'tags': ['$tag-1', '$tag-2',...],<br>
                    &emsp;&emsp;&emsp;&emsp;'content': [<br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;'$PARAGRAPH_1',<br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;'$PARAGRAPH_2',<br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;...<br>
                    &emsp;&emsp;&emsp;&emsp;]<br>
                &emsp;&emsp;},<br>
                &emsp;&emsp;...<br>
            }
        </div>

    """


def info_add_story() -> str:
    """ """
    return """
        <div style="margin-bottom:1em;">
            There are 2 ways of adding story into the search engine 
            which are using URL or JSON file.
            <ul>
                <li>
                    URL - either medium story URL or medium list URL.
                </li>
                <li>
                    JSON - content of one or more medium stories. 
                    Example file can be found at 
                    <a href="https://github.com/chiachong/scrape_medium/blob/main/data/my_lists.json">here</a>.
                </li>
            </ul>
        </div>
    """


def info_add_url() -> str:
    """ """
    return """
        <div>
            <ul>
                <li>
                    Story url - the url to a medium story. Only one story would 
                    be added into the search engine at a time.
                </li>
                <li>
                    List url - the url to a <b>public</b> medium list. There 
                    could be multiple stories being added into the search 
                    engine depends on how many stories in that medium list. 
                    <span style="color:grey;">
                    (typically looks like https://medium.com/@USERNAME/list/LISTNAME-HASH)
                    </span>
                </li>
            </ul>
        </div>
    """


def load_css() -> str:
    """ Return all css styles. """
    common_tag_css = """
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: .15rem .40rem;
                position: relative;
                text-decoration: none;
                font-size: 95%;
                border-radius: 5px;
                margin-right: .5rem;
                margin-top: .4rem;
                margin-bottom: .5rem;
    """
    return f"""
        <style>
            #tags {{
                {common_tag_css}
                color: rgb(88, 88, 88);
                border-width: 0px;
                background-color: rgb(240, 242, 246);
            }}
            #tags:hover {{
                color: black;
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
            #active-tag {{
                {common_tag_css}
                color: rgb(246, 51, 102);
                border-width: 1px;
                border-style: solid;
                border-color: rgb(246, 51, 102);
            }}
            #active-tag:hover {{
                color: black;
                border-color: black;
                background-color: rgb(240, 242, 246);
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            }}
        </style>
    """


def no_result_html() -> str:
    """ """
    return """
        <div style="color:grey;font-size:95%;margin-top:0.5em;">
            No results were found.
        </div><br>
    """


def number_of_results(total_hits: int, duration: float) -> str:
    """ HTML scripts to display number of results and time taken. """
    return f"""
        <div style="color:grey;font-size:95%;">
            {total_hits} results ({duration:.2f} seconds)
        </div><br>
    """


def pagination(total_pages: int, search: str, current_page: int,
               tags: str) -> str:
    """ Create and return html for pagination. """
    # search words and tags
    search_params = f'?search={search}'
    if tags is not None:
        search_params += f'&tags={tags}'

    # avoid invalid page number (<=0)
    if (current_page - 5) > 0:
        start_from = current_page - 5
    else:
        start_from = 1

    page_hrefs = []
    if current_page != 1:
        page_hrefs.append(f'<a href="{search_params}&page={1}">&lt&ltFirst</a>')
        page_hrefs.append(f'<a href="{search_params}&page={current_page - 1}">&ltPrevious</a>')

    for i in range(start_from, min(total_pages + 1, start_from + 10)):
        if i == current_page:
            page_hrefs.append(f'{current_page}')
        else:
            page_hrefs.append(f'<a href="{search_params}&page={i}">{i}</a>')

    if current_page != total_pages:
        page_hrefs.append(f'<a href="{search_params}&page={current_page + 1}">Next&gt</a>')

    return '<div>' + '&emsp;'.join(page_hrefs) + '</div>'


def search_result(i: int, url: str, title: str, highlights: str,
                  author: str, length: str, **kwargs) -> str:
    """ HTML scripts to display search results. """
    return f"""
        <div style="font-size:120%;">
            {i + 1}.
            <a href="{url}">
                {title}
            </a>
        </div>
        <div style="font-size:95%;">
            <div style="color:grey;font-size:95%;">
                {url[:90] + '...' if len(url) > 100 else url}
            </div>
            <div style="float:left;font-style:italic;">
                {author} ·&nbsp;
            </div>
            <div style="color:grey;float:left;">
                {length} ...
            </div>
            {highlights}
        </div>
    """


def tag_boxes(search: str, tags: list, active_tag: str) -> str:
    """ HTML scripts to render tag boxes. """
    html = ''
    search = urllib.parse.quote(search)
    for tag in tags:
        if tag != active_tag:
            html += f"""
            <a id="tags" href="?search={search}&tags={tag}">
                {tag.replace('-', ' ')}
            </a>
            """
        else:
            html += f"""
            <a id="active-tag" href="?search={search}">
                {tag.replace('-', ' ')}
            </a>
            """

    html += '<br><br>'
    return html
