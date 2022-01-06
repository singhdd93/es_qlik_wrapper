import sys

from app import app
from flask import request, jsonify
import requests
from requests.auth import HTTPBasicAuth
import json
import os

ES_HOST = os.getenv('ES_HOST',"http://localhost:9200")
USERNAME = os.getenv('USERNAME',"username")
PASSWORD = os.getenv('PASSWORD',"password")


@app.route('/<idx>', methods=['POST'])
def index(idx=""):
    try:
        req = json.loads(request.data)
        print(request.data)
        if req is None or not "_scroll_id" in req:
            if not 'es_params' in req:
                return "Expected es_params", 400
            data = req['es_params']
            r = requests.post('{}/{}/_search?scroll=1m'.format(ES_HOST, idx), json=data, auth=(USERNAME, PASSWORD))
        else:
            data = {"scroll": "1m", "scroll_id": req["_scroll_id"]}
            r = requests.post('{}/_search/scroll'.format(ES_HOST), json=data, auth=(USERNAME, PASSWORD))
        result = r.json()

        if len(result['hits']['hits']) == 0:
            del result['_scroll_id']
        else:
            result["nextUrl"] = request.host_url + idx + "/" + result['_scroll_id']

        return jsonify(result)

    except Exception as ex:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return str(ex), 400


@app.route('/<idx>/<scroll_id>', methods=['GET', 'POST'])
def get(idx="", scroll_id=""):
    data = {"scroll": "1m", "scroll_id": scroll_id}
    r = requests.post('{}/_search/scroll'.format(ES_HOST), json=data, auth=(USERNAME, PASSWORD))
    result = r.json()
    if len(result['hits']['hits']) == 0:
        del result['_scroll_id']
    else:
        result["nextUrl"] = request.host_url + idx + "/" + result['_scroll_id']
    return jsonify(result)
