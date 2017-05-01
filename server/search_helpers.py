# -*- coding: utf-8 -*-
from geopy.distance import vincenty
from cache import read_shops, read_products, read_tags, read_taggings, match_tags_per_shop


def find_shops_in_radius(radius, userCoords):
    allShops = read_shops()
    shopsInRadius = []
    for shop in allShops:
        if(vincenty(userCoords, (float(shop[1]),float(shop[2]))).meters < radius):
            shopsInRadius.append(shop)
    return shopsInRadius


def keep_shops_with_tag(shopsInRadius, tags):
    allTags = read_tags()
    allTaggings = read_taggings()
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
    if(tags):
        shopsInRadius = find_shops_in_radius(radius, userCoords)
        return keep_shops_with_tag(shopsInRadius,tags)
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

    return products[0:count]
