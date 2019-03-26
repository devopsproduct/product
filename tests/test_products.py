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
Test cases for Products Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.models import Products, DataValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProducts(unittest.TestCase):
    """ Test Cases for Products """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Products.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_product(self):
        """ Create a product and assert that it exists """
        product = Products(name="Television", category="Electronics", available=True)
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Television")
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.available, True)

    def test_add_a_product(self):
        """ Create a product and add it to the database """
        products = Products.all()
        self.assertEqual(products, [])
        product = Products(name="Television", category="Electronics", available=True)
        self.assertTrue(product != None)
        self.assertEqual(product.id, None)
        product.save()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(product.id, 1)
        products = Products.all()
        self.assertEqual(len(products), 1)

    def test_update_a_product(self):
        """ Update a product """
        product = Products(name="Television", category="Electronics", available=True)
        product.save()
        self.assertEqual(product.id, 1)
        # Change it an save it
        product.category = "Electronics"
        product.save()
        self.assertEqual(product.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Products.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(product[0].category, "Electronics")

    def test_delete_a_product(self):
        """ Delete a product """
        product = Products(name="Television", category="Electronics", available=True)
        product.save()
        self.assertEqual(len(Products.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Products.all()), 0)

    def test_serialize_a_product(self):
        """ Test serialization of a Product """
        product = Products(name="Television", category="Electronics", available=True)
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "Television")
        self.assertIn('category', data)
        self.assertEqual(data['category'], "Electronics")
        self.assertIn('available', data)
        self.assertEqual(data['available'], False)

    def test_deserialize_a_product(self):
        """ Test deserialization of a product """
        data = {"id": 1, "name": "T-Shirt", "category": "Clothing", "available": True}
        product = Products()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "T-Shirt")
        self.assertEqual(product.category, "Clothing")
        self.assertEqual(product.available, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        product = Products()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_products(self):
        """ Find a Product by ID """
        Products(name="Television", category="Electronics", available=True).save()
        TShirt = Products(name="T-Shirt", category="Clothing", available=False)
        TShirt.save()
        product = Products.find(TShirt.id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, TShirt.id)
        self.assertEqual(product.name, "T-Shirt")
        self.assertEqual(product.available, False)

    def test_find_by_category(self):
        """ Find Products by Category """
        Products(name="Television", category="Electronics", available=True).save()
        Products(name="T-Shirt", category="Clothing", available=False).save()
        product = Products.find_by_category("Clothing")
        self.assertEqual(product[0].category, "Clothing")
        self.assertEqual(product[0].name, "T-Shirt")
        self.assertEqual(product[0].available, False)

    def test_find_by_name(self):
        """ Find a Product by Name """
        Products(name="Television", category="Electronics", available=True).save()
        Products(name="T-Shirt", category="Clothing", available=False).save()
        product = Products.find_by_name("T-Shirt")
        self.assertEqual(product[0].category, "Clothing")
        self.assertEqual(product[0].name, "T-Shirt")
        self.assertEqual(product[0].available, False)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
