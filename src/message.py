from .article import Article
from .processing import shorter_text


class Message:
    TITLE_LEN = 20
    DESCRIPTION_LEN = 80
    WORD_PER_MIN = 200

    def __init__(self, article: Article):
        self.__article = article
        self.url = self.__article.url

        if self.__article.title is not None:
            self.title = shorter_text(self.__article.title, Message.TITLE_LEN)
        else:
            self.title = 'No title'

        if self.__article.content is not None:
            self.read_time = self.__compute_read_time()
        else:
            self.read_time = 0

        if self.__article.description is not None:
            self.description = shorter_text(self.__article.description, Message.DESCRIPTION_LEN)
        elif self.__article.content is not None:
            self.description = shorter_text(self.__article.content, Message.DESCRIPTION_LEN)
        else:
            self.description = None

    def get_message(self) -> str:
        return self.__build_message(self.url, self.title, self.description, self.read_time)

    def __compute_read_time(self) -> int:
        tokenized_content = self.__article.content.split()
        return int(round(len(tokenized_content) / self.WORD_PER_MIN))

    @staticmethod
    def __build_message(url: str, title: str, description: str = None, read_time: int = 0) -> str:
        message = f'<b>{title}</b>'

        if read_time > 0:
            message += ' · <i>{read_time}</i> min read'

        if description is not None:
            message += f'\n{description}'

        message += f'\n\n<b>Link:</b> {url}'

        return message
