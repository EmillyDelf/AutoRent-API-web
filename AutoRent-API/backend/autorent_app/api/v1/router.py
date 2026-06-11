from rest_framework.routers import DefaultRouter

from .viewsets import (VeiculoViewSet,ClienteViewSet,ReservaViewSet,PagamentoViewSet,AvaliacaoViewSet)

router = DefaultRouter()

router.register(
    "veiculos",
    VeiculoViewSet
)

router.register(
    "clientes",
    ClienteViewSet
)

router.register(
    "reservas",
    ReservaViewSet
)

router.register(
    "pagamentos",
    PagamentoViewSet
)

router.register(
    "avaliacoes",
    AvaliacaoViewSet
)

urlpatterns = router.urls