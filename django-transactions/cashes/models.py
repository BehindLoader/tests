from django.contrib.auth.models import User
from django.db import models


class Cash(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    value = models.DecimalField(
        max_digits=32,
        decimal_places=3,
    )

    def __str__(self):
        return 'Cash #{0}'.format(self.id)
