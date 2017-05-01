# -*- coding: utf-8 -*-
from server.cache import *


class TestCache(object):
    '''Test the server.cache module functions

    Uses the test data in /tests/test_data.
    '''

    def test_read_tags(self):
        tags = read_tags()
        tagsExpected = {"tag1":"tag_1", "tag2":"tag_2", "tag3":"tag_3"}
        assert tags == tagsExpected


    def test_read_shops(self):
        shops = read_shops()
        shopsExpected = [
        ["shop_1","50.002","50.002"],
        ["shop_2","50.005","50.005"],
        ["shop_3","50.01","50.01"]]
        assert shops == shopsExpected


    def test_read_taggings(self):
        taggings = read_taggings()
        taggingsExpected = [
        ["shop_1","tag_1"],
        ["shop_2","tag_2"],
        ["shop_3","tag_3"]]
        assert taggings == taggingsExpected

    def test_read_products(self):
        products = read_products()
        productsExpected = [
        ["shop_3","product3","3"],
        ["shop_2","product2","2"],
        ["shop_1","product1","1"]]
        assert products == productsExpected


    def test_match_tags_per_shop(self):
        tps = match_tags_per_shop()
        tpsExpected = {
        "shop_1":["tag_1"],
        "shop_2":["tag_2"],
        "shop_3":["tag_3"]
        }
        assert tps == tpsExpected
