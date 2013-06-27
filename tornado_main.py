#!/usr/bin/env python

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from foodies.wsgi import application as wsgi_handler 


def main():
    wsgi_app = tornado.wsgi.WSGIContainer(wsgi_handler)
    
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    
    tornado_app = tornado.web.Application([
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    ], **settings)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
