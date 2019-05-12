"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice
from app.models import Products

class ProductFactory(factory.Factory):
    """ Creates fake products that you don't have to use """
    class Meta:
        model = Products
    id = factory.Sequence(lambda n: n)
    name = factory.Faker('first_name')
    category = FuzzyChoice(choices=['Television', 'T-Shirt', 'Table', 'Helicopter'])
    available = FuzzyChoice(choices=[True, False])
    price = FuzzyChoice(choices=[34.12, 0.99, 12, 18.1231, 3000, 3000.12])

if __name__ == '__main__':
    for _ in range(10):
        product = ProductFactory()
        print(product.serialize())
