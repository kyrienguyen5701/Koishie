import webbrowser
import json

file = open('data/data.json', 'r')
data = json.load(file)
web_store = data['web store']

def browse(web):
    webbrowser.open('www.{}'.format(web_store[web]['url']))

class Website():
    def __init__(self, url, purpose):
        self.url = url
        self.purpose = purpose

    def to_dict(self):
        return {
            'url': self.url,
            'purpose': self.purpose
        }

def invalid_url(url):
    available_domains = ('com', 'gov', 'org', 'net', 'edu', 'jp')
    domain = url.split('.')[-1]
    if domain not in available_domains:
        return True
    return False

def add_web(name, url, purpose):
    if name not in web_store.keys():
        web = Website(url, purpose)
        web_store[name] = web.to_dict()
    json.dump(data, open('data.json', 'w'), indent=4)


def admin():
    print('Enter the following information to add a website:')
    name = input('Name: ')
    url = input('URL: ')
    while invalid_url(url):
        url = input('Invalid URL. Please try again: ')
    purpose = input('Purpose: ')
    add_web(name, url, purpose)

if __name__ == '__main__':
    admin()