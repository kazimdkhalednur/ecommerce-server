from django.db import models
from django.db.models import Q


class PublishedProductManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(Q(status="published") | Q(status="out_of_stack"))
        )
