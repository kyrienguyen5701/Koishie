import random
import json

file = open('data/util_data.json', 'r')
data = json.load(file)
hello_scripts = data['hello']
bye_scripts = data['goodbye']

def hello():
    return random.choice(hello_scripts)

def bye():
    return random.choice(bye_scripts)

def add_hello(s):
    if s not in hello_scripts:
        hello_scripts.append(s)
    json.dump(data, open('data/util_data.json', 'w'), indent=4)

def add_goodbye(s):
    if s not in bye_scripts:
        bye_scripts.append(s)
    json.dump(data, open('data/util_data.json', 'w'), indent=4)

def menu():
    print('''1. Press H to add a hello
2. Press G to add a goodbye
3. Press Enter to leave''')

def take_input():
    return input('Your input: ')

def invalid_input():
    return input('Invalid input. Please try again: ')

def admin():
    menu()
    cmd = take_input().lower()
    while cmd != '':
        if cmd not in ['h', 'g']:
            cmd = invalid_input()
        
        else:
            if cmd == 'h':
                h = input("The hello: ")
                while h == '':
                    h = invalid_input()
                add_hello(h)
            
            if cmd == 'g':
                g = input("The hello: ")
                while g == '':
                    g = invalid_input()
                add_goodbye(g)
        menu()
        cmd = take_input()

if __name__ == '__main__':
    admin()