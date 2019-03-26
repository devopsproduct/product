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
Test cases for Pet Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.models import Pet, DataValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestProducts(unittest.TestCase):
    """ Test Cases for Pets """

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
        Pet.init_db(app)
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
        product.category = "Electrionics"
        product.save()
        self.assertEqual(product.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Products.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(product[0].category, "Electronics")

    def test_delete_a_Products(self):
        """ Delete a Pet """
        pet = Products(name="fido", category="dog", available=True)
        pet.save()
        self.assertEqual(len(Pet.all()), 1)
        # delete the pet and make sure it isn't in the database
        pet.delete()
        self.assertEqual(len(Pet.all()), 0)

    def test_serialize_a_Products(self):
        """ Test serialization of a Pet """
        pet = Products(name="fido", category="dog", available=False)
        data = pet.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('id', data)
        self.assertEqual(data['id'], None)
        self.assertIn('name', data)
        self.assertEqual(data['name'], "fido")
        self.assertIn('category', data)
        self.assertEqual(data['category'], "dog")
        self.assertIn('available', data)
        self.assertEqual(data['available'], False)

    def test_deserialize_a_Products(self):
        """ Test deserialization of a Pet """
        data = {"id": 1, "name": "kitty", "category": "cat", "available": True}
        pet = Products()
        pet.deserialize(data)
        self.assertNotEqual(pet, None)
        self.assertEqual(pet.id, None)
        self.assertEqual(pet.name, "kitty")
        self.assertEqual(pet.category, "cat")
        self.assertEqual(pet.available, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        pet = Products()
        self.assertRaises(DataValidationError, pet.deserialize, data)

    def test_find_Products(self):
        """ Find a Pet by ID """
        Products(name="fido", category="dog", available=True).save()
        kitty = Products(name="kitty", category="cat", available=False)
        kitty.save()
        pet = Pet.find(kitty.id)
        self.assertIsNot(pet, None)
        self.assertEqual(pet.id, kitty.id)
        self.assertEqual(pet.name, "kitty")
        self.assertEqual(pet.available, False)

    def test_find_by_category(self):
        """ Find Pets by Category """
        Products(name="fido", category="dog", available=True).save()
        Products(name="kitty", category="cat", available=False).save()
        pets = Pet.find_by_category("cat")
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "kitty")
        self.assertEqual(pets[0].available, False)

    def test_find_by_name(self):
        """ Find a Pet by Name """
        Products(name="fido", category="dog", available=True).save()
        Products(name="kitty", category="cat", available=False).save()
        pets = Pet.find_by_name("kitty")
        self.assertEqual(pets[0].category, "cat")
        self.assertEqual(pets[0].name, "kitty")
        self.assertEqual(pets[0].available, False)


######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
