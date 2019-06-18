from pprint import pprint
from requests_futures.sessions import FuturesSession

session = FuturesSession()

def response_hook(resp, *args, **kwargs):
    # parse the json storing the result on the response object
    data = resp.json()
    print(data)
r = [None] * 10
for i in range(0,10):
    r[i] = session.get('http://httpbin.org/get', hooks={
        'response': response_hook,
    })
# do some other stuff, send some more requests while this one works
for m in r:
    m.result(timeout=2)
# print('response status {0}'.format(r[0].status_code))
# data will have been attached to the response object in the background
# pprint(r[0].data)