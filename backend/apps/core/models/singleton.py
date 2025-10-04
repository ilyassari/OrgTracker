from django.db import models
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    """
    An abstract base class for models which can have only one instance.
    """
    _instance = None

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(args, kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
