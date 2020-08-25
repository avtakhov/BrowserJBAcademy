import sys
import os
import collections
import requests
import bs4
from colorama import Fore, Style

_INCORRECT = 'Error: Incorrect URL'


def _correct_url(url):
    return '.' in url


_text_tags = ['p', 'h', 'title', 'a']


def _request(url):
    r = requests.get('https://' + url)
    result = ''
    for i in bs4.BeautifulSoup(r.content, 'html.parser').find_all(_text_tags):
        if i.name == 'a':
            result += Fore.BLUE + i.get_text().strip() + Style.RESET_ALL
        else:
            result += i.get_text().strip()
        result += '\n'

    return result


def _short_name(url):
    return url[:url.rfind('.')]


class Browser:

    def __init__(self, keep_dir):
        self.saved = set()
        self.stack = collections.deque()
        self.keep_dir = keep_dir
        if not os.path.exists(keep_dir):
            os.mkdir(keep_dir)

    def _get_path(self, name):
        return f'{self.keep_dir}/{name}'

    def request(self, url):
        if url.startswith('https://'):
            url = url[len('https://'):]

        if url in self.saved:
            self.stack.append(url)
            with open(self._get_path(url), 'r', encoding='utf-8') as f:
                return f.read()

        if not _correct_url(url):
            return _INCORRECT

        name = _short_name(url)
        self.stack.append(name)
        answer = _request(url)
        self.saved.add(name)
        with open(self._get_path(name), 'w', encoding='utf-8') as f:
            f.write(answer)
        return answer

    def back(self):
        if len(self.stack) > 0:
            self.stack.pop()
        if len(self.stack) == 0:
            return ''
        return self.request(self.stack.pop())


def main():
    if len(sys.argv) != 2:
        print('enter directory for web pages')
        return

    browser = Browser(sys.argv[1])

    while True:
        user_request = input()
        if user_request == 'exit':
            return
        elif user_request == 'back':
            print(browser.back())
        else:
            print(browser.request(user_request))


if __name__ == '__main__':
    main()
