from django.db import models

from .mixins import ModelDiffMixin


class BaseModel(ModelDiffMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'modified_at'
        ordering = ('-modified_at', '-created_at',)
        abstract = True