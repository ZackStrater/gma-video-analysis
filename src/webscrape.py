


from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
import re
import json
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import requests


username='goodmorningamerica'
browser = webdriver.Chrome('/home/zackstrater/Downloads/chromedriver')
browser.get(f'https://www.instagram.com/{username}/?hl=en')
Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


#Extract links from user profile page
links=[]
source = browser.page_source
data=bs(source, 'html.parser')
body = data.find('body')
script = body.find('script', text=lambda t: t.startswith('window._sharedData'))

page_json = script.string.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)

for link in data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
    links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')
#try with ['display_url'] instead of ['shortcode'] if you don't get links


result=pd.DataFrame()
for link in links:
    try:
        page = requests.get(link)
        data=bs(page.content, 'html.parser')
        body = data.find('body')
        script = body.find('script')
        raw = script.string.strip().replace('window._sharedData =', '').replace(';', '')
        json_data=json.loads(raw)
        print(json_data)
        posts =json_data['entry_data']['PostPage'][0]['graphql']
        posts= json.dumps(posts)
        posts = json.loads(posts)
        x = pd.DataFrame.from_dict(json_normalize(posts), orient='columns')
        x.columns = x.columns.str.replace('shortcode_media.', '')
        result=result.append(x)
    except:
        pass
result = result.drop_duplicates(subset = 'shortcode')
result.index = range(len(result.index))
print(result)




# # hashtags code
# hashtag='food'
# browser = webdriver.Chrome('/path/to/chromedriver')
# browser.get('https://www.instagram.com/explore/tags/'+hashtag)
# Pagelength = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


#Extract links from hashtag page
# links=[]
# source = browser.page_source
# data=bs(source, 'html.parser')
# body = data.find('body')
# script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
# page_json = script.text.split(' = ', 1)[1].rstrip(';')
# data = json.loads(page_json)
# for link in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
#     links.append('https://www.instagram.com'+'/p/'+link['node']['shortcode']+'/')