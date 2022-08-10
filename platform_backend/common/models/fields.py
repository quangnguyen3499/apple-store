from django.db import models


class PriceField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = 19
        kwargs["decimal_places"] = 4
        kwargs["default"] = 0
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_digits"]
        del kwargs["decimal_places"]
        del kwargs["default"]
        return name, path, args, kwargs
