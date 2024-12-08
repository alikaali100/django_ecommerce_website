from django.db import models
from django.utils.timezone import now
from .manager import BaseManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False,blank=True,null=True)
    deleted_at = models.DateTimeField(auto_now=True)
    objects = BaseManager() 
    class Meta:
        abstract = True

