import os
import random
import requests

from requests import RequestException

from .utils import decode_url
from .processing import HTMLProcessing


class InvalidStatus(Exception):
    """Invalid status exception"""
    pass


class Article:

    def __init__(self,
                 url: str,
                 title: str = None,
                 description: str = None,
                 content: str = None):
        self.__url = url
        self.__title = title
        self.__description = description
        self.__content = content


class RequestArticle:
    REQUEST_TIMEOUT = (2, 5)
    AVAILABLE_STATUSES = [200]

    def __init__(self):
        self.__user_agents = RequestArticle.__load_client_headers()

    def request(self, url: str) -> Article:
        try:
            url = decode_url(url)
            client_headers = {'User-Agent': random.choice(self.__user_agents)}
            response = requests.get(url,
                                    headers=client_headers,
                                    verify=True,
                                    timeout=RequestArticle.REQUEST_TIMEOUT,
                                    allow_redirects=True)
            url_ = response.url
            status = response.status_code
            headers = response.headers

            if status in RequestArticle.AVAILABLE_STATUSES:
                html = HTMLProcessing(response.text)
                title = html.get_title()

                if 'html' in headers.get('Content-Type', ''):
                    description = html.get_description()
                    content = html.get_content()
                    return Article(url_, title, description, content)
                else:
                    return Article(url_, title)

            else:
                raise InvalidStatus(f'Get a {status} status on request {url}')

        except RequestException:
            pass

    @staticmethod
    def __load_client_headers():
        with open(os.path.join(os.environ['ASSETS'], 'user_agent_list.txt'), 'r') as f:
            user_agents = [line.rstrip('\n') for line in f]
        return user_agents
