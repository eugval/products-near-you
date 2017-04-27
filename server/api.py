# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify,request
import csv


api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():
    print("i am here")
    print(request.args.get('count'))
    print (type(request.args.get('count')))
    print(request.args.getlist('tags[]'))
    print(request.args)
    print(request.args.get('radius'))
    print(type(request.args.get('radius')))
    print(request.args.get('lat'))
    print(request.args.get('lng'))

    testobj={"title":"Ruben WD 60cm","popularity":0.905,"shop":{"lat":59.3378757904,"lng":18.06191385546 }}
    testobj2={"title":"blaboura","popularity":0.86,"shop":{"lat":59.3378486904,"lng":18.06191853445546 }}
    testarr =[testobj,testobj2]
    response = jsonify({'products': testarr})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
    return response
