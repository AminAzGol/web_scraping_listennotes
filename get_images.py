import os
import requests
from requests_futures.sessions import FuturesSession
from bs4 import BeautifulSoup
import pandas
import atexit
from time import time

session = FuturesSession()


def download_file(url, local_filename ):
    local_filename += '.jpg'
    # local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        directory = 'images'
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory+'/'+local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()
    return local_filename

def hook_factory(*factory_args, **factory_kwargs):
    def response_hook(resp, *args, **kwargs):
        html = resp.content
        file_name = factory_args[0]
        soup = BeautifulSoup(html, 'lxml')

        pic_tag = soup.find("picture", {
            "class": "we-artwork ember-view product-artwork product-artwork--bottom-separator we-artwork--fullwidth"})
        try:
            img = pic_tag.source
            img_urls = img['srcset'].split(',')
            img_url = img_urls[0]
            img_url = img_url.replace(' 1x', '')
            resp.img_url = img_url
            download_file(img_url, file_name)
        except:
            resp.img_url = ''

    return response_hook

def load_pre():
    global file_name, start_index
    with open('pre_image_info.txt') as f:
        file_name = f.readline()


def save():
    global file_name, start_index, df
    new_file_name = f"listennotes_podcasts_img_url_{str(int(time()))}.json"
    with open('pre_image_info.txt', 'w+') as f:
        f.write(new_file_name)

    with open(new_file_name , 'w', encoding='utf-8') as file:
        df.to_json(file, force_ascii=False)
    print('saved')

file_name = None
atexit.register(save)
load_pre()
df = pandas.read_json(file_name)
df.to_json()
max_req = 40
sessions = [None]*max_req
rows = []
req_index = 0
tic = time()
max_time = 1
for i, row in df.iterrows():
    if 'img_url' in row and row['img_url'] is not '':
        continue
    itunes = row['itunes_url']
    ses = dict()
    ses['session'] = session.post(itunes, hooks={
        'response': hook_factory(row['uuid']),
    })
    ses['row'] = row
    ses['index'] = i
    sessions[req_index] = ses
    req_index += 1

    if req_index >= max_req:
        for s in sessions:
            res = s['session'].result()
            df.set_value(s['index'], 'img_url', res.img_url)
            print(s['index'])
        req_index = 0
        while time() - tic > max_time:
            tic = time()
print('done')

