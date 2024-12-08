# from django.test import TestCase
# from product.models import Product, Category

# class ProductModelTest(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(name="Electronics")

#     def test_create_product(self):
#         product = Product.objects.create(
#             name="Smartphone",
#             description="A very smart phone.",
#             price=699.99,
#             stock=10,
#             category=self.category
#         )
#         self.assertEqual(product.name, "Smartphone")
#         self.assertEqual(product.category, self.category)
#         self.assertFalse(product.is_deleted)

#     def test_stock_reduction(self):
#         product = Product.objects.create(
#             name="Laptop",
#             description="A lightweight laptop.",
#             price=999.99,
#             stock=5,
#             category=self.category
#         )
#         product.stock -= 1
#         product.save()
#         self.assertEqual(product.stock, 4)
