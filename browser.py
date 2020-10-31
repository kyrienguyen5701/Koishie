import webbrowser
import json
import pandas as pd
import random

path = 'data/util_data.json'
file = open(path, 'r')
data = json.load(file)
web_store = pd.DataFrame(data['web store'])
web_store.set_index('title', inplace=True)

def browse(title):
    if title in web_store.index:
        webbrowser.open('{}'.format(web_store.loc[title]['url']))

class Website():
    def __init__(self, title, url, purpose):
        self.title = title
        self.url = url
        self.purpose = purpose

    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'purpose': self.purpose
        }

def invalid_url(url):
    available_domains = ('com', 'gov', 'org', 'net', 'edu', 'jp', 'vn','us', 'ai')
    domain = url.split('.')[-1]
    if domain not in available_domains:
        return True
    return False

def add_web(title, url, purpose):
    # preprocess the title:
    if not title[0].isupper():
        title = title[0].upper() + title[1:]
    # check if the website is already available
    if not (web_store.index == title).any():
        web = Website(title, url, purpose)
        data['web store'].append(web.to_dict())
        json.dump(data, open(path, 'w'), indent=4)

def admin():
    print('Enter the following information to add a website:')
    title = input('Name: ')
    url = input('URL: ')
    while invalid_url(url):
        url = input('Invalid URL. Please try again: ')
    purpose = input('Purpose: ')
    add_web(title, url, purpose)

if __name__ == '__main__':
    admin()