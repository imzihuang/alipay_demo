#!/usr/bin/python
# -*- coding: utf-8 -*-

from tornado import httpserver
from tornado.web import URLSpec, StaticFileHandler, Application
from tornado.options import define, options
from tornado.ioloop import IOLoop
from setproctitle import setproctitle
import views
import api
from settings import *


def view_handlers():
    prefix = default_settings.get('product_prefix', '/alipay')
    if prefix[-1] != '/':
        prefix += '/'

    return [
        URLSpec('/', views.DefaultHandler, default_settings),
        URLSpec(prefix + r'home.html$', views.HomeHandler, default_settings),
        (prefix + r'(.*\.(css|png|gif|jpg|js|ttf|woff|woff2))', StaticFileHandler, {'path': default_settings.get('static_path')}),
    ]

def api_handlers():
    prefix = default_settings.get('product_prefix', '/alipay')
    if prefix[-1] != '/':
        prefix += '/'
    return [
        (prefix + r'alipay_url', api.AlipayUrlHandler),
        (prefix + r'alipay_pay', api.AlipayHandler),
        (prefix + r'alipay_test', api.AlipayCallbackHandler),
    ]

class My_Application(Application):
    def __init__(self, handlers=None, default_host="", **settings):
        super(My_Application, self).__init__(view_handlers() + api_handlers() + handlers, default_host, **settings)

def make_app():
    settings = {
        'cookie_secret': "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    }
    return My_Application([], **settings)

define("port", default=8080, help="run on the given port", type=int)
setproctitle('product:web')

if __name__ == "__main__":
    options.logging = 'info'
    app = make_app()
    server = httpserver.HTTPServer(app, xheaders=True)
    server.bind(options.port)
    server.start(0)
    IOLoop.instance().start()
