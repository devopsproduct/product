# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Products API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
from flask_api import status    # HTTP Status Codes
#from mock import MagicMock, patch
from app.models import Products, DataValidationError, db
from .product_factory import ProductFactory
import app.service as service

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProductsServer(unittest.TestCase):
    """ Product Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        service.app.debug = False
        service.initialize_logging(logging.INFO)
        # Set up the test database
        service.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        service.init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = service.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_productss(self, count):
        """ Factory method to create products in bulk """
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            resp = self.app.post('/products',
                                 json=test_product.serialize(),
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test product')
            new_product = resp.get_json()
            test_product.id = new_product['id']
            products.append(test_product)
        return products

    def test_index(self):
        """ Test the Home Page """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Product Demo REST API Service')

    def test_get_product_list(self):
        """ Get a list of Products """
        self._create_products(5)
        resp = self.app.get('/products')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_product(self):
        """ Get a single Product """
        # get the id of a product
        test_product = self._create_products(1)[0]
        resp = self.app.get('/products/{}'.format(test_product.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], test_product.name)

    def test_get_product_not_found(self):
        """ Get a Product thats not found """
        resp = self.app.get('/products/0')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        """ Create a new Product """
        test_product = ProductFactory()
        resp = self.app.post('/products',
                             json=test_product.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_product = resp.get_json()
        self.assertEqual(new_product['name'], test_product.name, "Names do not match")
        self.assertEqual(new_product['category'], test_product.category, "Categories do not match")
        self.assertEqual(new_product['available'], test_product.available, "Availability does not match")
        # Check that the location header was correct
        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_product = resp.get_json()
        self.assertEqual(new_product['name'], test_product.name, "Names do not match")
        self.assertEqual(new_product['category'], test_product.category, "Categories do not match")
        self.assertEqual(new_product['available'], test_product.available, "Availability does not match")

    def test_update_product(self):
        """ Update an existing product """
        # create a product to update
        test_product = ProductFactory()
        resp = self.app.post('/products',
                             json=test_product.serialize(),
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the product
        new_product = resp.get_json()
        new_product['category'] = 'unknown'
        resp = self.app.put('/products/{}'.format(new_product['id']),
                            json=new_product,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_product = resp.get_json()
        self.assertEqual(updated_product['category'], 'unknown')

    def test_delete_product(self):
        """ Delete a Product """
        test_product = self._create_products(1)[0]
        resp = self.app.delete('/products/{}'.format(test_product.id),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/products/{}'.format(test_product.id),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_product_list_by_category(self):
        """ Query Proucts by Category """
        products = self._create_products(10)
        test_category = products[0].category
        category_products = [product for product in products if product.category == test_category]
        resp = self.app.get('/products',
                            query_string='category={}'.format(test_category))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(category_products))
        # check the data just to be sure
        for product in data:
            self.assertEqual(product['category'], test_category)

    # @patch('app.service.product.find_by_name')
    # def test_bad_request(self, bad_request_mock):
    #     """ Test a Bad Request error from Find By Name """
    #     bad_request_mock.side_effect = DataValidationError()
    #     resp = self.app.get('/products', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # @patch('app.service.product.find_by_name')
    # def test_mock_search_data(self, product_find_mock):
    #     """ Test showing how to mock data """
    #     product_find_mock.return_value = [MagicMock(serialize=lambda: {'name': 'fido'})]
    #     resp = self.app.get('/products', query_string='name=fido')
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()