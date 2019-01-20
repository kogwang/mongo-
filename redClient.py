import redis

class Redis():
    def __init__(self):
        self.red = redis.Redis(host='localhost')