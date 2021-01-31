import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
for key in r.scan_iter("user:*"):
    v = r.get(key)
    print(v)
    # get = r.get('foo')
    # print(get)