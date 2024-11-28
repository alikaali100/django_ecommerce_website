from django.test import TestCase
from core.models import BaseModel

class TestBaseModel(TestCase):
    def test_base_model_fields(self):
        obj = BaseModel()
        self.assertTrue(hasattr(obj, 'created_at'))
        self.assertTrue(hasattr(obj, 'updated_at'))
        self.assertTrue(hasattr(obj, 'is_deleted'))
