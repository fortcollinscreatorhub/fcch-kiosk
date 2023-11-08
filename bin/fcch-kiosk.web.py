#!/usr/bin/env python3

# Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
# SPDX-License-Identifier: MIT

import argparse
from flask import Flask, jsonify, request
import gunicorn.app.base
import traceback
import sys

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description='Web configuration interface for kiosk app')
parser.add_argument('--urls-file', required=True)
parser.add_argument('--control-pipe', required=True)
parser.add_argument('--web-dir', required=True)
args = parser.parse_args()

app = Flask(
    __name__,
    static_url_path='', 
    static_folder=args.web_dir,
)

def send_cmd(cmd):
    with open(args.control_pipe, 'wt') as f:
        f.write(cmd)

def catch_except(f):
    def wrapped(*args, **kwargs):
        try:
            ret = f(*args, **kwargs)
            if ret is None:
                ret = jsonify({})
            return ret
        except:
            traceback.print_exc()
            return jsonify({'error': 'API failed due to exception; check log'})
    wrapped.__name__ = f.__name__
    return wrapped

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/api/debug-on", methods=['POST'])
@catch_except
def api_debug_on():
    send_cmd('D')
    return jsonify({})

@app.route("/api/debug-off", methods=['POST'])
@catch_except
def api_debug_off():
    send_cmd('d')
    return jsonify({})

@app.route("/api/prev-url", methods=['POST'])
@catch_except
def api_prev_url():
    send_cmd('P')
    return jsonify({})

@app.route("/api/next-url", methods=['POST'])
@catch_except
def api_next_url():
    send_cmd('N')
    return jsonify({})

@app.route('/api/urls-file', methods=['GET', 'POST'])
@catch_except
def api_urls_file():
    if request.method == 'GET':
        with open(args.urls_file, 'rt') as f:
            content = f.read()
        return jsonify({"content": content})
    elif request.method == 'POST':
        content = request.data
        content = content.decode('utf8')
        with open(args.urls_file, 'wt') as f:
            f.write(content)
        send_cmd('R')
        return jsonify({})
    else:
        raise Exception('Invalid method')

class GUnicornApp(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
            if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

options = {
    'bind': '%s:%s' % ('', '80'),
    'workers': 2,
}
GUnicornApp(app, options).run()
