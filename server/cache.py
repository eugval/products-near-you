# -*- coding: utf-8 -*-
from flask.ext.cache import Cache
from operator import itemgetter
from flask import current_app
import  csv

cache = Cache()

def data_path(filename):
    '''Return the path to the file in the argument'''
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


def setup_cache():
    '''Read the data from the csv files and store them in cache for fast access'''
    print("Loading cache...")
    read_products()
    read_shops()
    read_tags()
    match_tags_per_shop()
    print("Finished loading cache.")


@cache.cached(key_prefix='read_tags')
def read_tags():
    '''Read and store the tag data

    Return a dictionary with tag:id entries where the tags are the keys
    and te ids are the values.
    '''
    tags = {}
    with open(data_path('tags.csv'),'rb') as tagFile:
        reader = csv.reader(tagFile)
        next(reader, None)
        for row in reader:
            tags[row[1]] = row[0]
    return tags


@cache.cached(key_prefix='read_shops')
def read_shops():
    '''Read and store the shop data

    Return a list with [id,lat,lng] entries, keeping each shop's id,
    latitude and longitude.
    '''
    shops=[]
    with open(data_path('shops.csv'), 'rb') as shopsFile:
        reader = csv.reader(shopsFile)
        next(reader , None)
        for row in reader:
            shops.append([row[0],row[2],row[3]])
    return shops


@cache.cached(key_prefix='read_products')
def read_products():
    '''Read and store the product data

    Return a list with [shop_id,title,popularity] entries keeping each product's
    shop_id, title, and popularity. It is also orderend in descending popularty.
    '''
    products = []
    with open(data_path('products.csv'),'rb') as productsFile:
        reader = csv.reader(productsFile)
        next(reader, None)
        for row in reader:
            products.append([row[1],row[2],row[3]])
    return sorted(products,key=itemgetter(2), reverse=True)


def read_taggings():
    '''Read the tagging data

    Return a list with [shop_id,tag_id] entries.
    Helper to the match_tags_per_shop function.
    '''
    taggings = []
    with open(data_path('taggings.csv'),'rb') as taggingsFile:
        reader =  csv.reader(taggingsFile)
        next(reader, None)
        for row in reader:
            taggings.append([row[1],row[2]])
    return taggings


@cache.cached(key_prefix='match_tags_per_shop')
def match_tags_per_shop():
    '''Match each store with the list of tags that it contains

    Return a dictionary with shop_id:[tag_ids] entries where the keys are the
    shop_ids and the values are lists of the tag_ids corresponding to each shop.
    '''
    shops = read_shops()
    taggings = read_taggings()

    tagsPerShop = {}

    for shop in shops:
        tagsPerShop[shop[0]]=[]
        for tagging in taggings:
            if(shop[0] == tagging[0]):
                tagsPerShop[shop[0]].append(tagging[1])
    return tagsPerShop
