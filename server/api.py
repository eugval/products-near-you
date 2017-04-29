# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from geopy.distance import vincenty

import csv,#,time


api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)

def find_shops_in_radius(radius, userCoords, shopsPath):
    shopsInRadius = []
    with open(shopsPath, 'rb') as shopsFile:
        reader = csv.reader(shopsFile)
        next(reader , None)
        for row in reader:
            if(vincenty(userCoords, (float(row[2]),float(row[3]))).meters < radius):
                shopsInRadius.append([row[0],row[2],row[3]])
    print("the number of shops in radius is:")
    print(len(shopsInRadius))
    return shopsInRadius


def keep_shops_with_tag(shopsInRadius, tags, taggingsPath, tagsPath):
    tagIds = []
    validShops = []
    with open(tagsPath,'rb') as tagFile:
        reader = csv.reader(tagFile)
        next(reader, None)
        for row in reader:
            if row[1] in tags:
                tagIds.append(row[0])

    print("tag IDs number is")
    print(len(tagIds))
    if(not tagIds):
        return []

    with open(taggingsPath,'rb') as taggingsFile:
        reader =  csv.reader(taggingsFile)
        next(reader, None)
        for row in reader:
            for shop in shopsInRadius:
                if(row[1] == shop[0]  and row[2] in tagIds):
                    validShops.append([shop[0],shop[1],shop[2]])

    return validShops


def get_valid_shops(radius, userCoords, tags, shopsPath, taggingsPath, tagsPath):
    if(tags):
        shopsInRadius = find_shops_in_radius(radius, userCoords, shopsPath)
        return keep_shops_with_tag(shopsInRadius,tags, taggingsPath, tagsPath)
    else:
        return find_shops_in_radius(radius, userCoords, shopsPath)

def get_products(validShops, count, productsPath):
    products = [];

    if(not validShops):
        return []

    with open(productsPath,'rb') as productsFile:
        reader = csv.reader(productsFile)
        next(reader, None)
        for row in reader:
            for shop in validShops:
                if(row[1] == shop[0]):
                    products.append({"title": row[2], "popularity": row[3], "shop": {"lat": shop[1], "lng": shop[2]}})

    sorted(products, key=lambda prod: prod['popularity'])
    print("the full product array length is")
    print(len(products))
    return products[0:count]


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
    print(tags)

    try:
         userCoords, radius, count = process_parameters(userCoords,radius,count,tags)
    except ValueError:
        return form_response(None, "Query parameters are malformed, please try again!")

    #Get the shops in radius, with the correct tags
    validShops = get_valid_shops(radius, userCoords, tags, SHOPS_PATH, TAGGINGS_PATH, TAGS_PATH)

    #Get the count most popular products sold across these shops
    products = get_products(validShops,count, PRODUCTS_PATH)

    return form_response(products, None)
