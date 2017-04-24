# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify,request


api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():
    testobj={"title":"Ruben WD 60cm","popularity":0.905,"quantity":10,"name":"Barton LLC","shop":{"lat":59.33784869757904,"lng":18.061913853445546 }}
    response = jsonify({'products': [testobj]})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
    return response
