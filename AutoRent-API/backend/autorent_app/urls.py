from django.urls import path

from .views import (
    home,
    health_check
)

urlpatterns = [

    # Página principal temporária
    path(
        "",
        home,
        name="home"
    ),

    # Verificação de saúde da aplicação
    path(
        "health/",
        health_check,
        name="health_check"
    ),
]