from django.db import models

class LogicalDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_deleted=True)

    def hard_delete(self):
        return super().delete()

    def active(self):
        return self.filter(is_deleted=False)

class LogicalDeleteManager(models.Manager):
    def get_queryset(self):
        return LogicalDeleteQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
