from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    name = models.CharField(
        max_length=100,
    )
    classification = models.CharField(
        max_length=100,
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
