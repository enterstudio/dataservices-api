# -*- coding: utf-8 -*-

import unittest
from mock import Mock
from cartodb_services.tomtom import TomTomGeocoder
from cartodb_services.tools.exceptions import ServiceException
from credentials import tomtom_api_key

INVALID_APIKEY = 'invalid_apikey'
VALID_ADDRESS = u'Mantería 3, Valladolid'.encode('utf-8')


class TomTomGeocoderTestCase(unittest.TestCase):
    def setUp(self):
        self.geocoder = TomTomGeocoder(apikey=tomtom_api_key(), logger=Mock())

    def test_invalid_token(self):
        invalid_geocoder = TomTomGeocoder(apikey=INVALID_APIKEY, logger=Mock())
        with self.assertRaises(ServiceException):
            invalid_geocoder.geocode(VALID_ADDRESS)

    def test_valid_request(self):
        place = self.geocoder.geocode(VALID_ADDRESS)

        assert place

    def test_valid_request_namedplace(self):
        place = self.geocoder.geocode(searchtext='Barcelona')

        assert place

    def test_valid_request_namedplace2(self):
        place = self.geocoder.geocode(searchtext='New York', country='us')

        assert place

    def test_odd_characters(self):
        place = self.geocoder.geocode(searchtext='Barcelona; &quot;Spain&quot;')

        assert place

    def test_empty_request(self):
        place = self.geocoder.geocode(searchtext='', country=None, city=None, state_province=None)

        assert place == []

    def test_empty_search_text_request(self):
        place = self.geocoder.geocode(searchtext='     ', country='us', city=None, state_province="")

        assert place == []

    def test_unknown_place_request(self):
        place = self.geocoder.geocode(searchtext='[unknown]', country='ch', state_province=None, city=None)

        assert place == []
