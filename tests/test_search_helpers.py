# -*- coding: utf-8 -*-
from server.search_helpers import *

class TestSearchHelpers(object):
    '''Test the server.search_helper module functions

    Uses the test data in /tests/test_data.
    '''

    def test_find_shops_in_radius(self):
        '''Test for find_shops_in_radius

        Case 1 : radius = 100.
        Case 2 : radius = 500.
        Case 3 : radius = 1000.
        Case 4 : radius = 2000.
        '''
        userCoords = (50.0,50.0)

        #Case1
        radius100 = 100
        shopsInR100 = find_shops_in_radius(radius100,userCoords)
        expectedShopsInR100 = []
        assert shopsInR100 == expectedShopsInR100

        #Case2
        radius500 = 500
        shopsInR500 = find_shops_in_radius(radius500,userCoords)
        expectedShopsInR500 = [["shop_1","50.002",'50.002']]
        assert shopsInR500 == expectedShopsInR500

        #Case3
        radius1000 = 1000
        shopsInR1000 = find_shops_in_radius(radius1000,userCoords)
        expectedShopsInR1000 = [["shop_1","50.002",'50.002'],
                                ["shop_2","50.005",'50.005']]
        assert shopsInR1000 == expectedShopsInR1000

        #Case4
        radius2000 = 2000
        shopsInR2000 = find_shops_in_radius(radius2000, userCoords)
        expectedShopsInR2000 = [["shop_1","50.002",'50.002'],
                                ["shop_2","50.005",'50.005'],
                                ["shop_3","50.01",'50.01']]
        assert shopsInR2000 == expectedShopsInR2000


    def test_keep_shops_with_tags(self):
        '''Test for keep_shops_with_tag

        All the shops are passed in shopsInRadius.
        Case 1 : Only false tags.
        Case 2 : tag2 and tag3 are validShops.
        '''
        shopsInRadius = [["shop_1","50.002",'50.002'],
                        ["shop_2","50.005",'50.005'],
                        ["shop_3","50.01",'50.01']]

        #Case1
        wrongTags = ["wt1", "wt2", "wt3"]
        shopsWrongTags = keep_shops_with_tag(shopsInRadius, wrongTags)
        expectedShopsWrongTags = []
        assert shopsWrongTags == expectedShopsWrongTags

        #Case2
        tags = ["tag2","wt1","tag3"]
        validShops = keep_shops_with_tag(shopsInRadius, tags)
        expectedValidShops = [["shop_2","50.005",'50.005'],
                             ["shop_3","50.01",'50.01']]
        assert validShops == expectedValidShops


    def test_get_valid_shops(self):
        '''Test for get_valid_shops

        userCoords = 1000
        radius = (50.0,50.0)
        Case 1 : no tags are provided.
        Case 2 : tag2 and tag3 are valid.
        '''
        userCoords = (50.0,50.0)
        radius = 1000

        #Case1
        noTags = []
        noTagShops = get_valid_shops(radius, userCoords, noTags)
        expectedNoTagShops = [["shop_1","50.002",'50.002'],
                             ["shop_2","50.005",'50.005']]
        assert noTagShops == expectedNoTagShops

        #Case2
        tags = ["tag2","wt1","tag3"]
        tagShops = get_valid_shops(radius, userCoords, tags)
        expectedTagShops = [["shop_2","50.005",'50.005']]
        assert tagShops == expectedTagShops


    def test_get_products(self):
        '''Test for get_products

        Case 1 : All shops are input, only 2 are kept.
        Case 2 : No shops are input.
        Case 3 : All shops are input, none is kept.
        Case 4 : All shops are input, all are kept.
        '''
        #Case1
        shops1 = [["shop_1","50.002",'50.002'],
                 ["shop_2","50.005",'50.005'],
                 ["shop_3","50.01",'50.01']]
        count1 = 2
        products1 = get_products(shops1, count1)
        expectedProducts1 = [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}},
                           {"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}}]

        #Case2
        shops2 = []
        count2 = 10
        products2 = get_products(shops2, count2)
        expectedProducts2 = []

        #Case3
        shops3 = shops1
        count3 = 0
        products3 = get_products(shops3, count3)
        expectedProducts3 = []

        #Case4
        shops4 = [["shop_1","50.002",'50.002'],
                 ["shop_2","50.005",'50.005'],
                 ["shop_3","50.01",'50.01']]
        count4 = count2
        products4 = get_products(shops4, count4)
        expectedProducts4 =  [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}},
                           {"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}},
                           {"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}},
                           ]
