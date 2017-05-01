# -*- coding: utf-8 -*-
from geopy.distance import vincenty
from cache import read_shops, read_products, read_tags, match_tags_per_shop


def find_shops_in_radius(radius, userCoords):
    '''Find the shops within a certain radius from the user

    Arguments:
    radius -- Only shops within that distance from the user are to be considered.
    userCoords -- A pair of coordinates (lat, lng) reprenting the user position.

    Return a list with [shop_id, lat, lng] entries with all the shops in radius.

    Helper to get_valid_shops.
    '''
    allShops = read_shops()
    shopsInRadius = []
    for shop in allShops:
        if(vincenty(userCoords, (float(shop[1]),float(shop[2]))).meters < radius):
            shopsInRadius.append(shop)
    return shopsInRadius


def keep_shops_with_tag(shopsInRadius, tags):
    '''Find the shops with at least one of the tags provided

    Arguments:
    shopsInRadius -- A list of shops with [shop_id,lat,lng] entries.
    tags -- A list of tags (strings).

    Return from the 'shopsInRadius' those shops that have at least one of the tags
    listed in 'tags' in the form of a list with [shop_is, lat, lng] entries.

    Helper to get_valid_shops.
    '''
    allTags = read_tags()
    tagsPerShop = match_tags_per_shop()
    tagIds = []
    validShops = []

    for tag in tags:
        tagId = allTags.get(tag)
        if(tagId):
            tagIds.append(tagId)

    if(not tagIds):
        return []

    for shop in shopsInRadius:
        if(any(i in tagIds for i in tagsPerShop[shop[0]])):
            validShops.append(shop)

    return validShops


def get_valid_shops(radius, userCoords, tags):
    '''Find the shops that are in range from the user and have the wanted tags

    Arguments:
    radius -- Only shops within that distance from the user are to be considered.
    userCoords -- A pair of coordinates (lat, lng) reprenting the user coordinates.
    tags -- A list of tags (strings).

    Return the shops that are within 'radius' distance from a user at 'userCoords'
    only if the shop has at least one of the tags.

    Helper to api.search.
    '''
    if(tags):
        shopsInRadius = find_shops_in_radius(radius, userCoords)
        return keep_shops_with_tag(shopsInRadius,tags)
    else:
        return find_shops_in_radius(radius, userCoords)

def get_products(validShops, count):
    '''Find the 'count' most popular products sold in the shops provided

    Arguments:
    validShops -- a list with [shop_id, lat, lng] entries.
    count -- the amount of products to be returned

    Return the 'count' products with the highest popularity ordered
    in descending popularity.
    The products are returned as a list of dictionaries with
    {"title": product_title , "popularity": product_popularity,
     "shop": {"lat": shop_latitude, "lng": shop_longitude}} entries.

    Helper to api.search.
    '''
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

    return products[0:count]
