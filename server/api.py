# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify, request
from geopy.distance import vincenty
from operator import itemgetter
from cache import cache
import  time, csv


api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


def setup_cache():
    read_products()
    read_shops()
    read_taggings()
    read_tags()
    match_tags_per_shop()


@cache.cached(key_prefix='read_tags')
def read_tags():
    tags = {}
    with open(data_path('tags.csv'),'rb') as tagFile:
        reader = csv.reader(tagFile)
        next(reader, None)
        for row in reader:
            tags[row[1]] = row[0]
    print("finished calling read_tags")
    return tags

@cache.cached(key_prefix='read_shops')
def read_shops():
    shops=[]
    with open(data_path('shops.csv'), 'rb') as shopsFile:
        reader = csv.reader(shopsFile)
        next(reader , None)
        for row in reader:
            shops.append([row[0],row[2],row[3]])
    print("finished calling read_shops")
    return shops

@cache.cached(key_prefix='read_taggings')
def read_taggings():
    taggings = []
    with open(data_path('taggings.csv'),'rb') as taggingsFile:
        reader =  csv.reader(taggingsFile)
        next(reader, None)
        for row in reader:
            taggings.append([row[1],row[2]])
    print("finished calling read_taggings")
    return taggings


@cache.cached(key_prefix='read_products')
def read_products():
    products = []
    with open(data_path('products.csv'),'rb') as productsFile:
        reader = csv.reader(productsFile)
        next(reader, None)
        for row in reader:
            products.append([row[1],row[2],row[3]])
    print("finished calling read_products")
    return sorted(products,key=itemgetter(2), reverse=True)

@cache.cached(key_prefix='match_tags_per_shop')
def match_tags_per_shop():
    shops = read_shops()
    taggings = read_taggings()

    tagsPerShop = {}

    for shop in shops:
        tagsPerShop[shop[0]]=[]
        for tagging in taggings:
            if(shop[0] == tagging[0]):
                tagsPerShop[shop[0]].append(tagging[1])
    print("finished calling match_tags_per_shop")
    return tagsPerShop

def find_shops_in_radius(radius, userCoords):
    allShops = read_shops()
    shopsInRadius = []
    for shop in allShops:
        if(vincenty(userCoords, (float(shop[1]),float(shop[2]))).meters < radius):
            shopsInRadius.append([shop[0],shop[1],shop[2]])
    print("the number of shops in radius is:")
    print(len(shopsInRadius))
    return shopsInRadius


def keep_shops_with_tag(shopsInRadius, tags):
    allTags = read_tags()
    allTaggings = read_taggings()
    tagIds = []
    validShops = []
    tagsPerShop = match_tags_per_shop()
    for tag in tags:
        tagId = allTags.get(tag)
        if(tagId):
            tagIds.append(tagId)

    print("tag IDs number is")
    print(len(tagIds))
    if(not tagIds):
        return []

    for shop in shopsInRadius:
        if(any(i in tagIds for i in tagsPerShop[shop[0]])):
            validShops.append([shop[0],shop[1],shop[2]])


    print('the valid shops number is ')
    print(len(validShops))

    return validShops


def get_valid_shops(radius, userCoords, tags):
    if(tags):
        t11=time.clock()
        shopsInRadius = find_shops_in_radius(radius, userCoords)
        t12=time.clock()
        print('time for find_shops_in_radius', t12-t11)
        temp = keep_shops_with_tag(shopsInRadius,tags)
        t13=time.clock()
        print('time for keep_shops_with_tag', t13-t12)
        return temp
    else:
        return find_shops_in_radius(radius, userCoords)

def get_products(validShops, count):
    allProducts = read_products()
    products = []

    if(not validShops):
        return []


    for product in allProducts:
        for shop in validShops:
            if(product[0] == shop[0]):
                products.append({"title": product[1], "popularity": product[2], "shop": {"lat": shop[1], "lng": shop[2]}})

        if(len(products)>=count):
            break


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
    t0=time.clock()
    #Search parameters
    userCoords = (request.args.get('lat'),request.args.get('lng'))
    radius = request.args.get('radius')
    count = request.args.get('count')
    tags = request.args.getlist('tags[]')


    try:
         userCoords, radius, count = process_parameters(userCoords,radius,count,tags)
    except ValueError:
        return form_response(None, "Query parameters are malformed, please try again!")

    t1 =time.clock()
    #Get the shops in radius, with the correct tags
    validShops = get_valid_shops(radius, userCoords, tags)
    t2=time.clock()
    print('valid shops time ellapsed: ', t2-t1)
    #Get the count most popular products sold across these shops
    products = get_products(validShops,count)
    t3=time.clock()

    print('getProducts time ellapsed: ', t3-t2)


    t4=time.clock()
    print('final time ellapsed: ', t4-t0)

    return form_response(products, None)
