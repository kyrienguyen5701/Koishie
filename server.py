from flask import Flask, jsonify, request
import time
from datetime import datetime
app = Flask(__name__)
url_timestamp = {}
url_viewtime = {}
previous_url = ''
history_path = 'data/browsing_history.txt'
user = 'Kyrie Nguyen' #static user, for now

def url_strip(url):
    if 'http://' in url or 'https://' in url or 'www.' in url:
        url = url.replace('https://', '').replace('http://', '').replace('www.', '').replace('\"', '')
    if '/' in url:
        url = url.split('/', 1)[0]
    return url

@app.route('/send_info', methods=['POST'])
def send_info():
    browsing_history = open(history_path, 'a')
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

    print('Initial db prev tab:', previous_url)
    print('Initial db timestamp:', url_timestamp)
    print('Initial db viewtime:', url_viewtime)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if previous_url != '':
        time_spent = int(time.time() - url_timestamp[previous_url])
        url_viewtime[previous_url] = url_viewtime[previous_url] + time_spent

    start = int(time.time())
    detailed_start = datetime.now().strftime('%d %B, %Y, %I:%M %p')
    if title != '':
        message_log = ''
        if url_viewtime[parent_url] == 0:
            message_log = 'At {}, {} started browsing {}'.format(detailed_start, user, title)
        else:
            duration = {
                'hour': url_viewtime[parent_url] // 3600,
                'minute': url_viewtime[parent_url] // 60,
                'second': url_viewtime[parent_url] % 60,
            }
            message_log = 'By {}, {} has been browsing {} for '.format(detailed_start, user, title, url_viewtime[parent_url])
            for k,v in duration.items():
                if v == 1:
                    message_log += '{} {} '.format(v, k)
                elif v > 1:
                    message_log += '{} {}s '.format(v, k)
        message_log += '\n'
        browsing_history.write(message_log)
        browsing_history.close()
            
    url_timestamp[parent_url] = start
    previous_url = parent_url
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