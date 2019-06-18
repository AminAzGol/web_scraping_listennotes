import grequests

urls = [
    'http://www.heroku.com',
    'http://python-tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://fakedomain/',
    'http://kennethreitz.com'
]


def exception_handler(request, exception):
        print ("Request failed")

reqs = [
    grequests.get('http://httpbin.org/delay/1', timeout=0.001, ),
    grequests.get('http://fakedomain/'),
    grequests.get('http://httpbin.org/status/500')
]
rs = (grequests.get(u) for u in urls)
# grequests.map(rs)
grequests.map(reqs ,exception_handler=exception_handler)