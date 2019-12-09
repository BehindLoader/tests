from django.db import models

from cashes.models import Cash


class Transaction(models.Model):
    operation_from = models.ForeignKey(
        Cash,
        on_delete=models.CASCADE,
        related_name='operation_from',
    )
    operation_to = models.ForeignKey(
        Cash,
        on_delete=models.CASCADE,
        related_name='operation_to',
    )
    value = models.DecimalField(
        max_digits=32,
        decimal_places=3,
    )

    same_owner = models.BooleanField(
        verbose_name='Transaction is between one profile cashes',
        default=False,
    )

    def __str__(self):
        return 'Transaction #{0} from "{1}" to "{2}"'.format(
            self.id,
            self.operation_from.id,
            self.operation_to.id,
        )
