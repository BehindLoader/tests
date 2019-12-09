from decimal import Decimal

from rest_framework import generics, serializers
from rest_framework.response import Response

from transactions.models import Transaction

# from profiles.models import Profile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'operation_from', 'operation_to', 'value']
        depth = 0


class TransactionsList(generics.ListAPIView):
    queryset = Transaction.objects.all().order_by('-value')
    serializer_class = AccountSerializer


class TransactionUserList(generics.ListAPIView):
    queryset = Transaction.objects.filter(same_owner=True)

    def list(self, request):
        users = {}

        # I don't know how to optimize it :(
        for transaction in self.get_queryset():
            owner = transaction.operation_from.owner.id

            users[owner] = users.get(owner, 0)

            users[owner] += transaction.value

        response = []
        for user, value in users.items():
            response.append({
                "user": user,
                "value": value
            })

        return Response(response)
