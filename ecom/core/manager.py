from django.db import models
from django.utils.timezone import now

class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    def all_with_deleted(self):
        return super().get_queryset()
    
    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)
    
    def soft_delete(self, instance):
        instance.is_deleted = True
        instance.deleted_at = now()
        instance.save(update_fields=['is_deleted', 'deleted_at'])
    
    def hard_delete(self, instance):
        instance.delete()

    def restore(self, instance):
        instance.is_deleted = False
        instance.deleted_at = None
        instance.save(update_fields=['is_deleted', 'deleted_at'])
