import webbrowser

def web_info(url, purpose):
    return {
        'url': url,
        'purpose': purpose
    }

def web_store():
    return {
        'facebook': web_info('facebook.com', 'social media'),
        'twitter': web_info('twitter.com', 'social media'),
        'instagram': web_info('instagram.com', 'social media'),
        'discord': web_info('discord.com', 'social media'),
        'slack': web_info('slack.com', 'social media'),
        'linkedIn': web_info('linkedin.com', 'social_media'),
        'coursera': web_info('coursera.org', 'study'),
        'hackerrank': web_info('hackerrank.com', 'study'),
        'codeforces': web_info('codeforces.com', 'study'),
        'google': web_info('google.com', 'search engine'),
        'bing': web_info('bing.com', 'search engine'),
        'duckDuckGo': web_info('duckduckgo.com', 'search engine'),
        'mail': web_info('mail.google.com', 'work'),
        'drive': web_info('drive.google.com', 'work'),
        'youtube': web_info('youtube.com', 'entertainment'),
        'anime': web_info('vuighe.net','entertainment'),
        'spotify': web_info('spotify.com', 'entertainment'),
        'netflix': web_info('netflix.com', 'entertainment'),
        'doujin': web_info('dynasty-scans.com', 'entertainment')
    }

def browse(web):
    # print(web_store()[web]['url'])
    webbrowser.open('www.{}'.format(web_store()[web]['url']))