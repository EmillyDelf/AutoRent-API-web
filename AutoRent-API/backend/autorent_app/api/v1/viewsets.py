from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.viewsets import ModelViewSet

from ...models import (
    Veiculo,
    Cliente,
    Reserva,
    Pagamento,
    Avaliacao
)

from .serializers import (
    VeiculoSerializer,
    ClienteSerializer,
    ReservaSerializer,
    PagamentoSerializer,
    AvaliacaoSerializer
)

# --
# VEiCULOS
# Cache aplicado apenas na listagem.
# --

@method_decorator(
    cache_page(60 * 5),
    name="list"
)
class VeiculoViewSet(ModelViewSet):

    queryset = Veiculo.objects.all()

    serializer_class = VeiculoSerializer

    search_fields = [
        "marca",
        "modelo",
        "placa"
    ]

    filterset_fields = [
        "status",
        "marca",
        "ano"
    ]

    ordering_fields = [
        "marca",
        "modelo",
        "ano",
        "preco_diaria"
    ]

    ordering = [
        "marca"
    ]

# --
# CLIENTES
# --
class ClienteViewSet(ModelViewSet):

    queryset = Cliente.objects.all()

    serializer_class = ClienteSerializer

    search_fields = [
        "nome",
        "cpf",
        "email",
        "cnh"
    ]

    ordering_fields = [
        "nome",
        "created_at"
    ]

    ordering = [
        "nome"
    ]

# --
# RESERVAS
# --
class ReservaViewSet(ModelViewSet):

    queryset = Reserva.objects.all()

    serializer_class = ReservaSerializer

    search_fields = [
        "cliente__nome",
        "veiculo__marca",
        "veiculo__modelo",
        "veiculo__placa"
    ]

    filterset_fields = [
        "status",
        "cliente",
        "veiculo"
    ]

    ordering_fields = [
        "data_inicio",
        "data_fim",
        "preco_total",
        "created_at"
    ]

    ordering = [
        "-created_at"
    ]


# --
# PAGAMENTOS
# --
class PagamentoViewSet(ModelViewSet):

    queryset = Pagamento.objects.all()

    serializer_class = PagamentoSerializer

    search_fields = [
        "reserva__cliente__nome",
        "reserva__veiculo__modelo",
        "reserva__veiculo__placa"
    ]

    filterset_fields = [
        "status",
        "metodo"
    ]

    ordering_fields = [
        "valor",
        "data_pagamento",
        "created_at"
    ]

    ordering = [
        "-created_at"
    ]


# --
# AVALIAÇÕES
# --

class AvaliacaoViewSet(ModelViewSet):

    queryset = Avaliacao.objects.all()

    serializer_class = AvaliacaoSerializer

    search_fields = [
        "cliente__nome",
        "veiculo__marca",
        "veiculo__modelo",
        "veiculo__placa"
    ]

    filterset_fields = [
        "nota",
        "veiculo"
    ]

    ordering_fields = [
        "nota",
        "created_at"
    ]

    ordering = [
        "-created_at"
    ]