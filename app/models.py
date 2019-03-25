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
Models for Product Service

All of the models are stored in this module

Models
------
Product - A Product used in the e-commerce Store

Attributes:
-----------
name (string) - the name of the product
category (string) - the category the product belongs to (i.e., apparel, shoe)
available (boolean) - True for products that are available for purchase

"""
import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Product(db.Model):
    """
    Class that represents a Product

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
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def save(self):
        """
        Saves a Product to the data store
        """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Removes a Product from the data store """
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a Product into a dictionary """
        return {"id": self.id,
                "name": self.name,
                "category": self.category,
                "available": self.available,
                "price": self.price}

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the Product data
        """
        try:
            self.name = data['name']
            self.category = data['category']
            self.available = data['available']
            self.price = data['price']
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
        """ Returns all of the Products in the database """
        cls.logger.info('Processing all Products')
        return cls.query.all()

    @classmethod
    def find(cls, product_id):
        """ Finds a Product by it's ID """
        cls.logger.info('Processing lookup for id %s ...', product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id):
        """ Find a Product by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Product with the given name

        Args:
            name (string): the name of the Products you want to match
        """
        cls.logger.info('Processing name query for %s ...', name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """ Returns all of the Products in a category

        Args:
            category (string): the category of the Products you want to match
        """
        cls.logger.info('Processing category query for %s ...', category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """ Query that finds Products by their availability """
        """ Returns all Products by their availability

        Args:
            available (boolean): True for products that are available
        """
        cls.logger.info('Processing available query for %s ...', available)
        return cls.query.filter(cls.available == available)
