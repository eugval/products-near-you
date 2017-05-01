# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from search_helpers import get_valid_shops, get_products


api = Blueprint('api', __name__)


def form_response(products, error):
    if(not products):
        products = []

    if(not error):
        error = ''

    response = jsonify({'errorMessage': error, 'products': products})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
    return response


def is_list_of_strings(lst):
        return isinstance(lst, list) and all(isinstance(elem, basestring) for elem in lst)

def process_parameters(userCoords, radius, count, tags):
    userCoords = (float(userCoords[0]), float(userCoords[1]))
    radius = float(radius)
    count = int(count)
    if(not is_list_of_strings(tags)):
        raise ValueError
    return (userCoords, radius, count)


@api.route('/search', methods=['GET'])
def search():
    #Search parameters
    userCoords = (request.args.get('lat'),request.args.get('lng'))
    radius = request.args.get('radius')
    count = request.args.get('count')
    tags = request.args.getlist('tags[]')

    try:
         userCoords, radius, count = process_parameters(userCoords,radius,count,tags)
    except (ValueError, TypeError):
        return form_response(None, "Query parameters are malformed, please try again!")

    #Get the shops in radius, with the correct tags
    validShops = get_valid_shops(radius, userCoords, tags)

    #Get the count most popular products sold across these shops
    products = get_products(validShops,count)

    return form_response(products, None)
