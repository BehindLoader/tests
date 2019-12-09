from decimal import Decimal

from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from cashes.models import Cash
from transactions.models import Transaction


class NotEnoughMoney(Exception):
    pass


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def send_money(request):
    operation_from = request.data.get('from')
    operation_to = request.data.get('to')
    value = request.data.get('value')

    if not (operation_from and operation_to and value):
        return Response(
            {
                'error': 'required arguments are missing',
            },
            HTTP_400_BAD_REQUEST,
        )

    # validate cash account owner
    try:
        cash_from = Cash.objects.select_for_update().get(id=operation_from)
        cash_to = Cash.objects.select_for_update().get(id=operation_to)
    except Cash.DoesNotExist:
        return Response(
            {
                'error': 'matching cash does not exist'
            },
            HTTP_400_BAD_REQUEST,
        )

    if cash_from.owner != request.user:
        return Response(
            {
                'error': '"from" cash account is not yours'
            },
            HTTP_400_BAD_REQUEST,
        )

    # send money
    try:
        with transaction.atomic():
            sid = transaction.savepoint()

            transfer_value = Decimal(value)

            if cash_from.value < transfer_value:
                transaction.savepoint_rollback(sid)
                raise NotEnoughMoney()
            else:
                cash_from.value -= transfer_value
                cash_to.value += transfer_value

                cash_from.save()
                cash_to.save()

                same_owner = cash_from.owner == cash_to.owner

                Transaction.objects.create(
                    operation_from=cash_from,
                    operation_to=cash_to,
                    value=transfer_value,
                    same_owner=same_owner,
                )

                transaction.savepoint_commit(sid)
    except NotEnoughMoney:
        return Response(
            {
                'error': 'not enough money on cash#{0}'.format(
                    cash_from.id
                ),
            },
            HTTP_400_BAD_REQUEST,
        )

    return Response(
        {
            'status': 'ok',
        },
        HTTP_200_OK,
    )
