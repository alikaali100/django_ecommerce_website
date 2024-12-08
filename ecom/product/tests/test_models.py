from django.test import TestCase
from product.models import Category, Product, ProductFeature, Discount
from django.utils.timezone import now, timedelta

class CategoryModelTest(TestCase):
    def setUp(self):
        self.parent_category = Category.objects.create(name="Electronics", description="Electronic items")
        self.sub_category = Category.objects.create(name="Laptops", description="Laptops and accessories", parent=self.parent_category)

    def test_category_creation(self):
        self.assertEqual(self.parent_category.name, "Electronics")
        self.assertEqual(self.sub_category.parent, self.parent_category)

    def test_category_str(self):
        self.assertEqual(str(self.parent_category), "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Electronic items")
        self.product = Product.objects.create(
            name="Laptop",
            description="High performance laptop",
            price=1500,
            stock=10,
            brand="BrandX",
            model="X100",
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Laptop")
        self.assertEqual(self.product.price, 1500)
        self.assertEqual(self.product.category, self.category)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Laptop")

class ProductFeatureModelTest(TestCase):
    def setUp(self):
        self.feature = ProductFeature.objects.create(key="RAM", value="16GB", display_order=1)

    def test_product_feature_creation(self):
        self.assertEqual(self.feature.key, "RAM")
        self.assertEqual(self.feature.value, "16GB")

    def test_product_feature_str(self):
        self.assertEqual(str(self.feature), "RAM: 16GB")

class DiscountModelTest(TestCase):
    def setUp(self):
        self.discount = Discount.objects.create(
            type="PG",
            amount=10,
            max_amount=100,
            start_date=now(),
            end_date=now() + timedelta(days=7)
        )

    def test_discount_creation(self):
        self.assertEqual(self.discount.type, "PG")
        self.assertEqual(self.discount.amount, 10)
        self.assertTrue(self.discount.start_date < self.discount.end_date)

    def test_discount_str(self):
        self.assertEqual(str(self.discount), "PG - 10")
