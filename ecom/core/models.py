from django.db import models
from django.utils.timezone import now
from core.managers import LogicalDeleteManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False,blank=True,null=True)
    deleted_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

