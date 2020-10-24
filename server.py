from flask import Flask, jsonify, request, json
import time
from datetime import datetime
import pandas as pd

app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
previous_url = ''
previous_title = ''
data_path = {
    'log': 'data/browsing_log.txt',
    'history': 'data/browsing_history.csv',
    'util': 'data/util_data.json'
}
user = 'Kyrie Nguyen' #static user, for now

util_file = open(data_path['util'], 'r')
data = json.load(util_file)
df = pd.DataFrame(data['web store'])
tracking_sites = df['url']

def url_strip(url):
    if 'http://' in url or 'https://' in url or 'www.' in url:
        url = url.replace('https://', '').replace('http://', '').replace('www.', '').replace('\"', '')
    if '/' in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_info', methods=['POST'])
def send_info():
    
    # time tracking
    when = datetime.now().strftime('%Y-%m-%d')
    start = int(time.time())
    detailed_start = datetime.now().strftime('%d %B, %Y, %I:%M %p')
    
    # parsing data sent from browser
    browsing_log = open(data_path['log'], 'a')
    response_json = request.get_data()
    params = response_json.decode()
    data = params.split('&')
    title = data[0].replace('title=', '')
    url = data[1].replace('url=', '')
    parent_url = url_strip(url)
    print('Currently viewing:', parent_url)

    global url_timestamp
    global url_viewtime
    global previous_url
    global previous_title

    print('Initial db prev tab:', previous_url)
    print('Initial db timestamp:', url_timestamp)
    print('Initial db viewtime:', url_viewtime)

    # check if the url is in the tracking list and has already been browsed
    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    # calculate browsing duration and logging
    if previous_url != '':
        url_viewtime[previous_url] += start - url_timestamp[previous_url] - url_viewtime[previous_url]
        message_log = ''
        duration = {
            'hour': url_viewtime[previous_url] // 3600,
            'minute': url_viewtime[previous_url] // 60,
            'second': url_viewtime[previous_url] % 60,
        }
        message_log = 'By {}, {} has been browsing {} for an addition of'.format(detailed_start, user, previous_title, url_viewtime[previous_url])
        for k,v in duration.items():
            if v == 1:
                message_log += ' {} {}'.format(v, k)
            elif v > 1:
                message_log += ' {} {}s'.format(v, k)
        message_log += '\n'
        if url_viewtime[parent_url] == 0:
            message_log += 'At {}, {} started browsing {}\n'.format(detailed_start, user, title)
        else:
            message_log += 'At {}, {} switched to {}\n'.format(detailed_start, user, title)
        print(message_log)
        browsing_log.write(message_log)
        browsing_log.close()
    else:
        browsing_log.write('At {}, {} started browsing {}\n'.format(detailed_start, user, title))
        browsing_log.close()

    # writing to history
    if (tracking_sites == previous_url).any():
        previous_parent_title = df[df['url'] == previous_url]['title'].values[0]
        print(previous_parent_title)
        browsing_history = pd.read_csv(data_path['history'],error_bad_lines=False,parse_dates=['When'])
        browsing_history.set_index('When', inplace=True)
        if not (browsing_history.index == when).any():
            print('Bủh')
            browsing_history = browsing_history.iloc[::-1].append(pd.Series(0,name=when,index=browsing_history.columns), ignore_index=False)[::-1]
        browsing_history.loc[when, previous_parent_title] += url_viewtime[previous_url]
        browsing_history.to_csv(data_path['history'])
                
    url_timestamp[parent_url] = start
    previous_url = parent_url
    previous_title = title
    print('Final timestamps:', url_timestamp)
    print('Final viewtimes:', url_viewtime)

    return jsonify({'message': 'Success!'}), 200

@app.route('/quit_info', methods=['POST'])
def quit_info():
    response_json = request.get_data()
    
    global url_timestamp
    global url_viewtime
    global previous_url

    print('Url closed: ' + response_json.decode())
    return jsonify({'message': 'Quit success!'}), 200

app.run(host='0.0.0.0', port=5000)