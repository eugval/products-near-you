# -*- coding: utf-8 -*-
from server.search_helpers import *

class TestSearchHelpers(object):
    def test_find_shops_in_radius(self):
        userCoords = (50.0,50.0)

        radius100 = 100
        shopsInR100 = find_shops_in_radius(radius100,userCoords)
        expectedShopsInR100 = []
        assert shopsInR100 == expectedShopsInR100

        radius500 = 500
        shopsInR500 = find_shops_in_radius(radius500,userCoords)
        expectedShopsInR500 = [["shop_1","50.002",'50.002']]
        assert shopsInR500 == expectedShopsInR500

        radius1000 = 1000
        shopsInR1000 = find_shops_in_radius(radius1000,userCoords)
        expectedShopsInR1000 = [["shop_1","50.002",'50.002'],
                                ["shop_2","50.005",'50.005']]
        assert shopsInR1000 == expectedShopsInR1000

        radius2000 = 2000
        shopsInR2000 = find_shops_in_radius(radius2000, userCoords)
        expectedShopsInR2000 = [["shop_1","50.002",'50.002'],
                                ["shop_2","50.005",'50.005'],
                                ["shop_3","50.01",'50.01']]
        assert shopsInR2000 == expectedShopsInR2000


    def test_keep_shops_with_tags(self):
        shopsInRadius = [["shop_1","50.002",'50.002'],
                        ["shop_2","50.005",'50.005'],
                        ["shop_3","50.01",'50.01']]

        wrongTags = ["wt1", "wt2", "wt3"]
        shopsWrongTags = keep_shops_with_tag(shopsInRadius, wrongTags)
        expectedShopsWrongTags = []
        assert shopsWrongTags == expectedShopsWrongTags

        tags = ["tag2","wt1","tag3"]
        validShops = keep_shops_with_tag(shopsInRadius, tags)
        expectedValidShops = [["shop_2","50.005",'50.005'],
                             ["shop_3","50.01",'50.01']]
        assert validShops == expectedValidShops


    def test_get_valid_shops(self):
        userCoords = (50.0,50.0)
        radius = 1000

        noTags = []
        noTagShops = get_valid_shops(radius, userCoords, noTags)
        expectedNoTagShops = [["shop_1","50.002",'50.002'],
                             ["shop_2","50.005",'50.005']]
        assert noTagShops == expectedNoTagShops

        tags = ["tag2","wt1","tag3"]
        tagShops = get_valid_shops(radius, userCoords, tags)
        expectedTagShops = [["shop_2","50.005",'50.005']]
        assert tagShops == expectedTagShops


    def test_get_products(self):
        shops1 = [["shop_1","50.002",'50.002'],
                 ["shop_2","50.005",'50.005'],
                 ["shop_3","50.01",'50.01']]
        count1 = 2
        products1 = get_products(shops1, count1)
        expectedProducts1 = [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}},
                           {"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}}]

        shops2 = []
        count2 = 10
        products2 = get_products(shops2, count2)
        expectedProducts2 = []

        shops3 = shops1
        count3 = 0
        products3 = get_products(shops3, count3)
        expectedProducts3 = []

        shops4 = [["shop_1","50.002",'50.002'],
                 ["shop_2","50.005",'50.005'],
                 ["shop_3","50.01",'50.01']]
        count4 = count2
        products4 = get_products(shops4, count4)
        expectedProducts4 =  [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}},
                           {"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}},
                           {"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}},
                           ]
