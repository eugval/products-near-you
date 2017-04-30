# -*- coding: utf-8 -*-
from server.api import *
import pytest
import json
import flask
from conftest import client, get

app = flask.Flask(__name__)

class TestApiUnits(object):

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


    def test_is_list_of_strings(self):
        lst1 = ['testing', 1, 'testing2', 3]
        res1 = is_list_of_strings(lst1)
        assert res1 == False

        lst2 = ['testing', 'testing1', 'testing2', 'testing3']
        res2 =  is_list_of_strings(lst2)
        assert res2 == True


    def test_process_parameters(self):
        userCoords1 = ("should raise a ValueError")
        radius1 = "100"
        count1 = "10"
        tags1 = ["tag1"]
        with pytest.raises(ValueError):
            process_parameters(userCoords1, radius1, count1, tags1)


        userCoords2 = ("50.0","50.0")
        radius2 = "100"
        count2 = "10"
        tags2 = ["tag1"]
        newUserCoords2, newRadius2, newCount2 = process_parameters(userCoords2, radius2, count2, tags2)
        assert isinstance(newUserCoords2, tuple)
        assert isinstance(newUserCoords2[0], float)
        assert isinstance(newUserCoords2[1], float)
        assert isinstance(newRadius2, float)
        assert isinstance(newCount2, int)
        assert isinstance(tags2, list)
        assert isinstance(tags2[0], basestring)


        userCoords3 = ("50.0","50.0")
        radius3 = "100"
        count3 = "10"
        tags3 = ["tag1",3]
        with pytest.raises(ValueError):
            process_parameters(userCoords3, radius3, count3, tags3)


    def test_form_response(self):
        with app.test_request_context('/search'):
            products1 = None
            error1 = "Test error message"
            response1 = form_response(products1, error1)
        response1Json = json.loads(response1.get_data(as_text=True))
        assert response1Json["errorMessage"] == error1
        assert response1Json["products"] == []

        with app.test_request_context('/search'):
            products2 = [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}},
                         {"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}},
                         {"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}},
                         ]
            error2 = None
            response2 = form_response(products2, error2)

        response2Json = json.loads(response2.get_data(as_text=True))

        assert response2Json["errorMessage"] == ''
        assert response2Json["products"] == [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}},
                                            {"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}},
                                            {"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}},
                                            ]

'''

class TestRequests(object):
    def test_search_request(self):
        #testClient = client(app, 'http://localhost:5000/search?count=4&radius=1000&lat=50.0&lng=50.0&tags[]=tag1&tags[]=tag3&tags[]=notag')
        #rv = get(testClient)

        rv = self.app.get('http://localhost:5000/search?count=4&radius=1000&lat=50.0&lng=50.0&tags[]=tag1&tags[]=tag3&tags[]=notag')

        print(rv)
        print(rv.data)
        assert rv.data ==1
'''
