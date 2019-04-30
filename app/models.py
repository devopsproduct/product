# Copyright 2016, 2017 John Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Models for products Service
All of the models are stored in this module
Models
------
product - A product used in the e-commerce Store

Attributes:
-----------
name (string) - the name of the product
category (string) - the category the product belongs to (i.e., apparel, shoe)
available (boolean) - True for products that are available for purchase
price (float) - the price of the product
"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    # Used for an data validation errors when deserializing
    pass


class Products(db.Model):
    """
    Class that represents a product

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """
    logger = logging.getLogger(__name__)
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63))
    category = db.Column(db.String(63))
    available = db.Column(db.Boolean())
    price = db.Column(db.Float(precision=2))


    def __repr__(self):
        return '<product %r>' % (self.name)

    def save(self):
        """
        Saves a product to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a product from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a products into a dictionary """
        return {"id": self.id,
                "name": self.name,
                "category": self.category,
                "available": self.available,
                "price": str(self.price)
                }

    def deserialize(self, data):
        """
        Deserializes a product from a dictionary

        Args:
            data (dict): A dictionary containing the product data
        """
        try:
            self.name = data['name']
            self.category = data['category']
            self.available = data['available']
            self.price = round(float(data['price']),2)
        except KeyError as error:
            raise DataValidationError('Invalid product: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid product: body of request contained' \
                                      'bad or no data')
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the products in the database """
        cls.logger.info('Processing all products')
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """ Finds a product by it's ID """
        cls.logger.info('Processing lookup for id %s ...', product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id):
        """ Find a product by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all products with the given name

        Args:
            name (string): the name of the products you want to match
        """
        cls.logger.info('Processing name query for %s ...', name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """ Returns all of the products in a category

        Args:
            category (string): the category of the products you want to match
        """
        cls.logger.info('Processing category query for %s ...', category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """ Query that finds products by their availability """
        """ Returns all products by their availability

        Args:
            available (boolean): True for products that are available
        """
        cls.logger.info('Processing available query for %s ...', available)
        return cls.query.filter(cls.available == available)
