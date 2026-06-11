from rest_framework import serializers

from ...models import (
    Veiculo,
    Cliente,
    Reserva,
    Pagamento,
    Avaliacao
)

class VeiculoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Veiculo
        fields = "__all__"

class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cliente
        fields = "__all__"
class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = "__all__"


class PagamentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pagamento
        fields = "__all__"


class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avaliacao
        fields = "__all__"