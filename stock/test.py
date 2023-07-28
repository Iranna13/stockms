from datetime import datetime
from decimal import Decimal
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Supplier, Product, Category, SupplierOrder, SupplierOrderItem, ConsumerOrder, ConsumerOrderItem, Consumer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Create a PostgreSQL database for testing
engine = create_engine("postgresql+psycopg2://postgres:admin123@localhost:5432/stock_new")
Session = sessionmaker(bind=engine)

# Create the tables in the database
Base.metadata.create_all(engine)


class TestModels(unittest.TestCase):
    def setUp(self):
        # Create a new session for each test
        self.session = Session()

    def tearDown(self):
        # Rollback the session after each test
        self.session.rollback()
        self.session.close()

    def test_supplier(self):
        # Create a Supplier object
        supplier = Supplier(name='Test Supplier', contact_number='1234567890')

        # Add the supplier to the session
        self.session.add(supplier)
        self.session.commit()

        # Retrieve the supplier from the database
        retrieved_supplier = self.session.query(Supplier).get(supplier.id)

        # Assert that the retrieved supplier matches the original supplier
        self.assertEqual(retrieved_supplier.name, 'Test Supplier')
        self.assertEqual(retrieved_supplier.contact_number, '1234567890')

    def test_product(self):
        # Create a Category object
        category = Category(category_name='Test Category')
        self.session.add(category)
        self.session.commit()

        # Create a Product object
        product = Product(category_id=category.id, name='Test Product', unit_price=10.99, description='Test Description')

        # Add the product to the session
        self.session.add(product)
        self.session.commit()

        # Retrieve the product from the database
        retrieved_product = self.session.query(Product).get(product.id)

        # Assert that the retrieved product matches the original product
        self.assertEqual(retrieved_product.category_id, category.id)
        self.assertEqual(retrieved_product.name, 'Test Product')
        self.assertEqual(retrieved_product.unit_price, Decimal('10.99'))
        self.assertEqual(retrieved_product.description, 'Test Description')

    def test_category(self):
        # Create a Product object
        product = Product(name='Test Product', unit_price=10.99, description='Test Description')
        self.session.add(product)
        self.session.commit()

        # Create a Category object
        category = Category(product_id=product.id, category_name='Test Category')

        # Add the category to the session
        self.session.add(category)
        self.session.commit()

        # Retrieve the category from the database
        retrieved_category = self.session.query(Category).get(category.id)

        # Assert that the retrieved category matches the original category
        self.assertEqual(retrieved_category.product_id, product.id)
        self.assertEqual(retrieved_category.category_name, 'Test Category')

    def test_supplier_order(self):
        # Create a Supplier object
        supplier = Supplier(name='Test Supplier', contact_number='1234567890')
        self.session.add(supplier)
        self.session.commit()

        # Create a SupplierOrder object
        supplier_order = SupplierOrder(supplier_id=supplier.id, order_date=datetime.now(), total_amount=100.0)

        # Add the supplier order to the session
        self.session.add(supplier_order)
        self.session.commit()

        # Retrieve the supplier order from the database
        retrieved_supplier_order = self.session.query(SupplierOrder).get(supplier_order.id)

        # Assert that the retrieved supplier order matches the original supplier order
        self.assertEqual(retrieved_supplier_order.supplier_id, supplier.id)
        self.assertEqual(retrieved_supplier_order.order_date, supplier_order.order_date)
        self.assertEqual(retrieved_supplier_order.total_amount, 100.0)

    def test_supplier_order_item(self):
        # Create a SupplierOrder object
        supplier_order = SupplierOrder(supplier_id=1, order_date=datetime.now(), total_amount=100.0)
        self.session.add(supplier_order)
        self.session.commit()

        # Create a Product object
        product = Product(name='Test Product', unit_price=10.99, description='Test Description')
        self.session.add(product)
        self.session.commit()

        # Create a SupplierOrderItem object
        supplier_order_item = SupplierOrderItem(
            supplier_order_id=supplier_order.id,
            product_id=product.id,
            item_name='Test Item',
            quantity=5,
            unit_price=10.99,
            total_price=54.95
        )

        # Add the supplier order item to the session
        self.session.add(supplier_order_item)
        self.session.commit()

        # Retrieve the supplier order item from the database
        retrieved_supplier_order_item = self.session.query(SupplierOrderItem).get(supplier_order_item.id)

        # Assert that the retrieved supplier order item matches the original supplier order item
        self.assertEqual(retrieved_supplier_order_item.supplier_order_id, supplier_order.id)
        self.assertEqual(retrieved_supplier_order_item.product_id, product.id)
        self.assertEqual(retrieved_supplier_order_item.item_name, 'Test Item')
        self.assertEqual(retrieved_supplier_order_item.quantity, 5)
        self.assertEqual(retrieved_supplier_order_item.unit_price, 10.99)
        self.assertEqual(retrieved_supplier_order_item.total_price, 54.95)

    def test_consumer_order(self):
        # Create a Consumer object
        consumer = Consumer(name='Test Consumer', contact_number='9876543210')
        self.session.add(consumer)
        self.session.commit()

        # Create a ConsumerOrder object
        consumer_order = ConsumerOrder(consumer_id=consumer.id, order_date=datetime.now(), total_amount=200.0)

        # Add the consumer order to the session
        self.session.add(consumer_order)
        self.session.commit()

        # Retrieve the consumer order from the database
        retrieved_consumer_order = self.session.query(ConsumerOrder).get(consumer_order.id)

        # Assert that the retrieved consumer order matches the original consumer order
        self.assertEqual(retrieved_consumer_order.consumer_id, consumer.id)
        self.assertEqual(retrieved_consumer_order.order_date, consumer_order.order_date)
        self.assertEqual(retrieved_consumer_order.total_amount, 200.0)

    def test_consumer_order_item(self):
        # Create a ConsumerOrder object
        consumer_order = ConsumerOrder(consumer_id=1, order_date=datetime.now(), total_amount=200.0)
        self.session.add(consumer_order)
        self.session.commit()

        # Create a Product object
        product = Product(name='Test Product', unit_price=10.99, description='Test Description')
        self.session.add(product)
        self.session.commit()

        # Create a ConsumerOrderItem object
        consumer_order_item = ConsumerOrderItem(
            consumer_order_id=consumer_order.id,
            product_id=product.id,
            item_name='Test Item',
            quantity=10,
            unit_price=10.99,
            total_price=109.9
        )

        # Add the consumer order item to the session
        self.session.add(consumer_order_item)
        self.session.commit()

        # Retrieve the consumer order item from the database
        retrieved_consumer_order_item = self.session.query(ConsumerOrderItem).get(consumer_order_item.id)

        # Assert that the retrieved consumer order item matches the original consumer order item
        self.assertEqual(retrieved_consumer_order_item.consumer_order_id, consumer_order.id)
        self.assertEqual(retrieved_consumer_order_item.product_id, product.id)
        self.assertEqual(retrieved_consumer_order_item.item_name, 'Test Item')
        self.assertEqual(retrieved_consumer_order_item.quantity, 10)
        self.assertEqual(retrieved_consumer_order_item.unit_price, 10.99)
        self.assertEqual(retrieved_consumer_order_item.total_price, 109.9)

    def test_consumer(self):
        # Create a Consumer object
        consumer = Consumer(name='Test Consumer', contact_number='9876543210')

        # Add the consumer to the session
        self.session.add(consumer)
        self.session.commit()

        # Retrieve the consumer from the database
        retrieved_consumer = self.session.query(Consumer).get(consumer.id)

        # Assert that the retrieved consumer matches the original consumer
        self.assertEqual(retrieved_consumer.name, 'Test Consumer')
        self.assertEqual(retrieved_consumer.contact_number, '9876543210')


if __name__ == '__main__':
    unittest.main()