from django.db import models
import uuid


class Store(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "address", "province")
