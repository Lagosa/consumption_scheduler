from django.db import models

class Dataset(models.Model):
    code = models.CharField(max_length=10, null=False, unique=True, primary_key=True)

    def __init__(self, code="-1", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code

    def __str__(self):
        return self.code

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        ordering = ['code']
