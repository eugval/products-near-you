# -*- coding: utf-8 -*-
import  time
from server.cache import *


class TestCache(object):

    def test_read_tags(self):
        t0 = time.clock()
        tags = read_tags()
        t1 = time.clock()

        tagsExpected = {"tag1":"tag_1", "tag2":"tag_2", "tag3":"tag_3"}

        assert t1-t0< 0.0001
        assert tags ==tagsExpected


    def test_read_shops(self):
        t0 = time.clock()
        shops = read_shops()
        t1 = time.clock()

        shopsExpected = [
        ["shop_1","50.002","50.002"],
        ["shop_2","50.005","50.005"],
        ["shop_3","50.01","50.01"]]


        assert t1-t0< 0.0001
        assert shops == shopsExpected


    def test_read_taggings(self):
        t0 = time.clock()
        taggings = read_taggings()
        t1 = time.clock()

        taggingsExpected = [
        ["shop_1","tag_1"],
        ["shop_2","tag_2"],
        ["shop_3","tag_3"]]

        assert t1-t0< 0.0001
        assert taggings ==  taggingsExpected

    def test_read_products(self):
        t0 = time.clock()
        products = read_products()
        t1 = time.clock()

        productsExpected = [
        ["shop_3","product3","3"],
        ["shop_2","product2","2"],
        ["shop_1","product1","1"]]

        assert t1-t0< 0.0001
        assert products == productsExpected


    def test_match_tags_per_shop(self):
        t0 = time.clock()
        tps = match_tags_per_shop()
        t1 = time.clock()

        tpsExpected = {
        "shop_1":["tag_1"],
        "shop_2":["tag_2"],
        "shop_3":["tag_3"]
        }

        assert t1-t0< 0.0001
        assert tps == tpsExpected
