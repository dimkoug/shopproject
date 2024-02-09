from django.db import models


class ActiveProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(price__gt=0,is_published=True)