# -*- coding: utf-8 -*-
from server.api import *
import pytest
import json
import flask
from conftest import app,client,get

app = flask.Flask(__name__)

class TestApi(object):
    '''Test the server.api module functions

    Uses the test data in /tests/test_data.
    '''

    def test_is_list_of_strings(self):
        '''Tests for api.list_of_strings

        Case 1 : A list of strings and integers.
        Case 2 : A list of strings.
        '''
        #Case1
        lst1 = ['testing', 1, 'testing2', 3]
        res1 = is_list_of_strings(lst1)
        assert res1 == False

        #Case2
        lst2 = ['testing', 'testing1', 'testing2', 'testing3']
        res2 =  is_list_of_strings(lst2)
        assert res2 == True


    def test_process_parameters(self):
        '''Tests for api.process_parameters

        Case 1 : User Coordinates are malformed.
        Case 2 : All paramters are valid.
        Case 3 : The list of tags is malformed.
        '''
        #Case1
        userCoords1 = ("should raise a ValueError")
        radius1 = "100"
        count1 = "10"
        tags1 = ["tag1"]
        with pytest.raises(ValueError):
            process_parameters(userCoords1, radius1, count1, tags1)

        #Case2
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

        #Case3
        userCoords3 = ("50.0","50.0")
        radius3 = "100"
        count3 = "10"
        tags3 = ["tag1",3]
        with pytest.raises(ValueError):
            process_parameters(userCoords3, radius3, count3, tags3)


    def test_form_response(self):
        '''Test for api.form_response

        Case 1 : An error is present and no products are given.
        Case 2 : Products are given and no error is present.
        '''
        #Case1
        with app.test_request_context('/search'):
            products1 = None
            error1 = "Test error message"
            response1 = form_response(products1, error1)

        response1Json = json.loads(response1.get_data(as_text=True))
        assert response1Json["errorMessage"] == error1
        assert response1Json["products"] == []

        #Case2
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


    def test_search_request(app,client,get):
        '''Test for search_request

        Variable search parameters:
        Case 1 : {count:4,radius:1000,coords:(50.0,50.0),tags:[tag1,tag3,notag]}.
        Case 2 : {count:4,radius:1000,lat:50, malformed lng, tags:[tag1,tag3,notag]}.
        Case 3 : {count:4,radius:1000,coords:(50.0,50.0)}.
        Case 4 : {count:1,radius:2000,coords:(50.0,50.0)}.
        Case 5 : No search parameters.
        Case 6 : {count:4,coords:(50.0,50.0)}.
        '''
        #Case1
        response1 = client.get('/search?count=4&radius=1000&lat=50.0&lng=50.0&tags[]=tag1&tags[]=tag3&tags[]=notag')
        data1 = json.loads(response1.get_data(as_text=True))
        assert data1["products"] ==  [{"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}}]
        assert data1["errorMessage"] == ''

        #Case2
        response2 = client.get('/search?count=4&radius=1000&lat[]=50.0&lng=50.0&tags[]=tag1&tags[]=tag3&tags[]=notag')
        data2 = json.loads(response2.get_data(as_text=True))
        assert data2["products"] ==  []
        assert data2["errorMessage"]=="Query parameters are malformed, please try again!"

        #Case3
        response3 = client.get('/search?count=4&radius=1000&lat=50.0&lng=50.0')
        data3 = json.loads(response3.get_data(as_text=True))
        assert data3["products"] ==  [{"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}},
                                    {"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}}]
        assert data3["errorMessage"] == ""

        #Case4
        response4 = client.get('/search?count=1&radius=2000&lat=50.0&lng=50.0')
        data4 = json.loads(response4.get_data(as_text=True))
        assert data4["products"] ==  [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}}]
        assert data4["errorMessage"] == ""

        #Case5
        response5 = client.get('/search')
        data5 = json.loads(response5.get_data(as_text=True))
        assert data5["products"] ==  []
        assert data5["errorMessage"]=="Query parameters are malformed, please try again!"

        #Case6
        response6 = client.get('/search?count=4&lat=50.0&lng=50.0')
        data6 = json.loads(response6.get_data(as_text=True))
        assert data6["products"] ==  []
        assert data6["errorMessage"]=="Query parameters are malformed, please try again!"
