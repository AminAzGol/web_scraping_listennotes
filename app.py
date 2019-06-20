import requests
import json
import brotli
import pandas
from genre import get_genre_name
from time import time, sleep
import os
from keywords import keywords
import atexit
from requests_futures.sessions import FuturesSession

main_dataframe = None
total_count = 0
total_max = 200000
first_save_flg = True
file_name = 'listennotes_podcasts_'+str(int(time()))+'.csv'
directory = 'output'
timer = time()
curr_req_max = 100
previous_file_name = None
previous_keyword_offset = 0
keyword_index = 0

def async_req(offset, keyword):
    url = 'https://www.listennotes.com/endpoints/v1/channels/search/'
    data = {
        'earliest_end_time': '',
        'earliest_start_time': '',
        'ecount_min': 0,
        'language': 'Any language',
        'ncid': '',
        'ocid': '',
        'offset': offset,
        'q': keyword,
        'sort_by_date': 0,
        'start_time': ''
    }
    headers = {
        "Host": "www.listennotes.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5A",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.listennotes.com/",
        "X-CSRFToken": "mc9OGLVwpy2J1FISUAexYg3zEhQ7WtSipeWolgGhWBHRD4qK9ZIZSmvBsbRYmbyT",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "131",
        "Connection": "keep-alive",
        "Cookie": "__cfduid=d6883d0b7a49e331f8934827970d7263b1560788822; csrftoken=mc9OGLVwpy2J1FISUAexYg3zEhQ7WtSipeWolgGhWBHRD4qK9ZIZSmvBsbRYmbyT",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "Trailers"
    }

    return session.post(url, data, headers=headers, hooks={
        'response': response_hook,
    })


def response_hook(resp, *args, **kwargs):
    # parse the json storing the result on the response object
    try:
        dec_res = brotli.decompress(resp.content)
        content = json.loads(dec_res)
        resp.dec_result = content['results']
        global curr_req_max
        curr_req_max = content['total']
    except:
        pass

def read_previous_attempt_data():
    global main_dataframe, previous_file_name,previous_keyword_offset
    with open('pre_data.txt') as f:
        if f.readable():
            previous_keyword_offset = int( f.readline() )
            previous_file_name = f.readline()
            previous_file_name = previous_file_name.replace('\n','')
    if previous_file_name:
        main_dataframe = pandas.read_csv(previous_file_name)


def add_dataframe(docs):
    global main_dataframe, total_count
    new_docs = []
    for doc in docs:
        keys = [
            'uuid', # save uuid for checking duplicate data
            'title',
            'author',
            'episode_count',
            'earliest_pub_date',
            'earliest_pub_date_ms',
            'tags',
            'extra_urls',
            'genres',
            'email',
            'itunes_url'
        ]

        # find the tags names based on the provided genre numbers
        doc['tags'] = []
        for genre_num in doc['genres']:
            genre_name = get_genre_name(genre_num)
            doc['tags'].append(genre_name)

        doc_to_save = {key: doc[key] for key in keys}
        new_docs.append(doc_to_save)

    new_df = pandas.DataFrame(new_docs)

    if main_dataframe is None:
        main_dataframe = new_df
    else:
        main_dataframe = main_dataframe.append(new_df, ignore_index=True)

    total_count = len(main_dataframe.index)

    main_dataframe.drop_duplicates(subset="uuid", keep='first', inplace=True)

    total_count = len(main_dataframe.index)



def save():
    print("save called")
    global main_dataframe
    if not os.path.exists(directory):
        os.makedirs(directory)
    main_dataframe.to_csv(directory + '/' + file_name, header=True)

    with open('pre_data.txt', 'w+') as f:
        f.write(str(keyword_index))
        f.write('\n')
        f.write(directory + '/' + file_name)
        f.write('\n')



atexit.register(save)
session = FuturesSession()
read_previous_attempt_data()
exc_count = 0
pre_total_count=0
req_max = 20
req_list = [None] * req_max
for k in range(previous_keyword_offset, len(keywords)):
    keyword_index = k
    keyword = keywords[k]
    offset = 0
    first = async_req(offset, keyword)
    res = first.result()
    if not res.dec_result:
        continue
    add_dataframe(res.dec_result)

    while offset < curr_req_max:
        req_list[exc_count] = async_req(offset, keyword)
        exc_count += 1

        if(exc_count >= req_max):
            exc_count = 0
            empty_result = False
            tic = time()
            for request in req_list:
                res = request.result()
                if not res.dec_result:
                    empty_result = True
                    continue
                add_dataframe(res.dec_result)
            print("========================================")
            print("This loop time: " + str(time() - tic))
            print("count: " + str(total_count))
            print("new: " + str(total_count - pre_total_count))
            pre_total_count = total_count
            print('Total time: ' + str(time() - timer))

            if empty_result:
                break

        offset += 10

    if total_count >= total_max:
        break