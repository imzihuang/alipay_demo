#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

STATIC_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'static')
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'templates')

default_settings = {
    'base_url': '/',
    'static_path': STATIC_PATH,
    'templates_path': TEMPLATES_PATH,
    'product_prefix': '/alipay',
    'api_version': 'v1.0',
    'api_key': '',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete'],
    'exclude_namespaces': [],
    'app_id': '2018011001743278',
    'alipay_url': 'https://openapi.alipaydev.com/gateway.do',
    'rsb_path': 'pem'
}

models = []