from django.contrib import admin
from .models import (Veiculo, Cliente, Reserva, Pagamento, Avaliacao,)

# VEÍCULOS: Exibe os veículos cadastrados.  / Permite: busca / filtros / ordenação
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "marca",
        "modelo",
        "ano",
        "preco_diaria",
        "status",
        "created_at",
    )

    search_fields = (
        "marca",
        "modelo",
    )

    list_filter = (
        "status",
        "ano",
    )

    ordering = (
        "marca",
    )

# CLIENTES
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nome",
        "email",
        "cnh",
        "telefone",
    )

    search_fields = (
        "nome",
        "email",
        "cnh",
    )

    ordering = (
        "nome",
    )

# RESERVAS
# Aqui é possível visualizar: cliente, veículo, período, valor total e status
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cliente",
        "veiculo",
        "data_inicio",
        "data_fim",
        "preco_total",
        "status",
    )

    list_filter = (
        "status",
    )

    search_fields = (
        "cliente__nome",
        "veiculo__modelo",
        "veiculo__marca",
    )

    ordering = (
        "-created_at",
    )

# PAGAMENTOS
@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "reserva",
        "valor",
        "metodo",
        "status",
        "data_pagamento",
    )

    list_filter = (
        "status",
        "metodo",
    )

    search_fields = (
        "reserva__cliente__nome",
        "reserva__veiculo__modelo",
    )

# AVALIAÇÕES
# Atendendo ao requisito do projetu: avaliações dos usuários
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "cliente",
        "veiculo",
        "nota",
    )

    list_filter = (
        "nota",
    )

    search_fields = (
        "cliente__nome",
        "veiculo__modelo",
    )