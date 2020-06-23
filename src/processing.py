import re

from typing import Union
from bs4 import BeautifulSoup


def preprocess_text(text: str) -> str:
    """Basic text pre-processing."""
    text = re.sub(r'(^[\n]+)', '', text)        # Remove \n at the beginning
    text = re.sub(r'([\n]+$)', '', text)        # Remove \n at the end
    text = re.sub(r'([\n]{2,})', '', text)      # Remove all double \n
    text = re.sub('r([\t])', '', text)          # Remove \t
    text = re.sub(r'([ ]{2,})', ' ', text)      # Remove extra spaces
    return text


def shorter_text(text: str, word_limit: int) -> str:
    """Makes a text shorter than word_limit."""
    text_split = text.split()
    if len(text_split) > word_limit:
        return ' '.join(text_split[:word_limit]) + '...'
    else:
        return text


class HTMLProcessing:

    def __init__(self, html: str):
        self.__soup = BeautifulSoup(html, 'html.parser')

    def get_title(self) -> Union[str, None]:
        """Extracts the title of a website."""
        title = None

        if self.__soup.find('h1') is not None:
            title = self.__soup.find('h1').text
        elif self.__soup.title is not None:
            title = self.__soup.title.text

        if title is not None:
            title = preprocess_text(title)

        return title

    def get_description(self) -> Union[str, None]:
        """Extracts the description of the article from meta tags."""
        tmp = self.__soup.findAll('meta', attrs={"name": re.compile(r"description", re.IGNORECASE)})
        tmp += self.__soup.findAll('meta', attrs={"name": re.compile(r"description", re.IGNORECASE)})

        for desc in tmp:
            if desc.get('content') is not None:
                return preprocess_text(desc['content'])

        return None

    def get_content(self) -> Union[str, None]:
        """Extracts paragraphs from the content of the article."""
        content = list()
        paragraphs = self.__soup.findAll('p')
        if paragraphs is not None:
            for p in paragraphs:
                content.append(preprocess_text(p.text))
            content = '\n'.join(content)
            return content

        return None
