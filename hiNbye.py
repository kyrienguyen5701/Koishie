import random

hello_scripts = [
    'Hi. I am your beloved waifu, Koishie. How can I help you?',
    'Ohayou, Koishie desu. Need me for something?',
    'Th ... Thanks for relying on Koishie. What can I do for you?'
]

bye_scripts = [
    'Bye bye. See you tomorrow!',
    'Ehh you are leaving? Please come back already or I will miss you',
    'Th ... Thanks for spending time with me. See ... see you soon.'
]

def hello():
    return random.choice(hello_scripts)

def bye():
    return random.choice(bye_scripts)