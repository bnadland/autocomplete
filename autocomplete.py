#!./env/bin/python

from redis import StrictRedis
from tornado import autoreload
from tornado.httpclient import HTTPClient, HTTPError
from tornado.options import define, options
from tornado.web import Application, RedirectHandler, RequestHandler, StaticFileHandler
from tornado.ioloop import IOLoop

# options
define("port", default=5000)
# commands
define("setup", default=False)

class CompletionHandler(RequestHandler):
    def initialize(self, r):
        self.r = r

    def get(self):
        term = self.get_argument("term")
        self.write({"data": [str(x) for x in r.smembers("ac:{}".format(term))]})

def add_to_autocompleter(r, user):
    user = user.strip()
    for i in range(len(user)):
        r.sadd("ac:{}".format(user[:i]), user)

if __name__ == '__main__':
    options.parse_command_line()

    r = StrictRedis(decode_responses=True)

    if options.setup or not r.keys("ac:*"):
        [r.delete(x) for x in r.keys("ac:*")]
        with open("users.txt", "r") as f:
            for user in f.readlines():
                add_to_autocompleter(r, user)
        exit(0)

    print("Starting server on port: {}".format(options.port))
    Application([
        (r"/", RedirectHandler, {"url": "/frontend/index.html"}),
        (r"/frontend/(.*)", StaticFileHandler, dict(path="frontend")),
        (r"/autocomplete/users", CompletionHandler, dict(r=r)),
    ], {
        "debug": True,
    }).listen(options.port)

    ioloop = IOLoop.instance()
    autoreload.watch("frontend/index.html")
    autoreload.start(ioloop)
    ioloop.start()
