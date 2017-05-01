# -*- coding: utf-8 -*-
from server.api import *
import pytest
import json
import flask
from conftest import app,client,get

app = flask.Flask(__name__)

class TestApi(object):

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

    def test_search_request(app,client,get):


        response= client.get('/search?count=4&radius=1000&lat=50.0&lng=50.0&tags[]=tag1&tags[]=tag3&tags[]=notag')
        data = json.loads(response.get_data(as_text=True))
        assert data["products"] ==  [{"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}}]
        assert data["errorMessage"] == ''

        response= client.get('/search?count=4&radius=1000&lat[]=50.0&lng=50.0&tags[]=tag1&tags[]=tag3&tags[]=notag')
        data = json.loads(response.get_data(as_text=True))
        assert data["products"] ==  []
        assert data["errorMessage"]=="Query parameters are malformed, please try again!"


        response= client.get('/search')
        data = json.loads(response.get_data(as_text=True))
        assert data["products"] ==  []
        assert data["errorMessage"]=="Query parameters are malformed, please try again!"


        response= client.get('/search?count=4&radius=1000&lat=50.0&lng=50.0')
        data = json.loads(response.get_data(as_text=True))
        assert data["products"] ==  [{"title": "product2", "popularity": "2", "shop": {"lat": "50.005", "lng": "50.005"}},
                                    {"title": "product1", "popularity": "1", "shop": {"lat": "50.002", "lng": "50.002"}}]
        assert data["errorMessage"] == ""

        response= client.get('/search?count=1&radius=2000&lat=50.0&lng=50.0')
        data = json.loads(response.get_data(as_text=True))
        assert data["products"] ==  [{"title": "product3", "popularity": "3", "shop": {"lat": "50.01", "lng": "50.01"}}]
        assert data["errorMessage"] == ""
