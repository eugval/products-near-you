# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from search_helpers import get_valid_shops, get_products


api = Blueprint('api', __name__)


def form_response(products, error):
    '''Return the response with the search results.'''
    if(not products):
        products = []

    if(not error):
        error = ''

    response = jsonify({'errorMessage': error, 'products': products})
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
    return response


def is_list_of_strings(lst):
    '''Return True if the argument is a list of strings, False otherwise'''
    return isinstance(lst, list) and all(isinstance(elem, basestring) for elem in lst)


def process_parameters(userCoords, radius, count, tags):
    '''Validate parameters received from the client and convert them to a more usable format'''
    userCoords = (float(userCoords[0]), float(userCoords[1]))
    radius = float(radius)
    count = int(count)
    if(not is_list_of_strings(tags)):
        raise ValueError
    return (userCoords, radius, count)


#: finds the products corresponding to search parameters
#and returns the
@api.route('/search', methods=['GET'])
def search():
    '''Entry point for product search

    Perform the search and return the results in json format to the client.
    Products found are returned under the 'products' key.
    Caught errors are passed to the client under 'errorMessage'.
    '''
    #Retrieve and process search parameters
    userCoords = (request.args.get('lat'),request.args.get('lng'))
    radius = request.args.get('radius')
    count = request.args.get('count')
    tags = request.args.getlist('tags[]')

    try:
         userCoords, radius, count = process_parameters(userCoords,radius,count,tags)
    except (ValueError, TypeError):
        return form_response(None, "Query parameters are malformed, please try again!")

    #Get the shops in radius that have the correct tags
    validShops = get_valid_shops(radius, userCoords, tags)

    #Get the 'count' most popular products sold across these shops
    products = get_products(validShops,count)

    return form_response(products, None)
