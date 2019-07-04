from dataclasses import dataclass
from typing import List
import requests
from html import unescape

@dataclass
class RandomQuotesGenerator:
    ID: str
    title: str
    content: str
    link: str
    custom_meta: str

    def __init__(self, d):
        self.__dict__ = d
        self.__dict__["content"] = unescape(self.__dict__["content"].replace('<p>','').replace(r'</p>', ''))

    @staticmethod
    def getRandomQuotes(cnt: int = 1):
        r = requests.get('https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]={}'.format(cnt))
        res = [RandomQuotesGenerator(x) for x in r.json()]
        return res


if __name__ == '__main__':
    r = RandomQuotesGenerator.getRandomQuotes()
    print(r)