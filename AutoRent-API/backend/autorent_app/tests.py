from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Avaliacao, Cliente, Reserva, Veiculo


class HealthEndpointTests(TestCase):
    def test_home_endpoint_returns_project_status(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_health_endpoint_returns_ok(self):
        response = self.client.get(reverse("health_check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})


class ReservaModelTests(TestCase):
    def setUp(self):
        self.veiculo = Veiculo.objects.create(
            marca="Toyota",
            modelo="Corolla",
            ano=2024,
            preco_diaria=Decimal("100.00"),
        )
        self.cliente = Cliente.objects.create(
            nome="Maria Silva",
            email="maria@example.com",
            cnh="12345678901",
            telefone="85999990000",
        )

    def test_calcula_preco_total_por_quantidade_de_dias(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date(2026, 6, 8),
            data_fim=date(2026, 6, 11),
        )

        self.assertEqual(reserva.preco_total, Decimal("300.00"))

    def test_aplica_acrescimo_para_reserva_iniciada_no_fim_de_semana(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date(2026, 6, 12),
            data_fim=date(2026, 6, 14),
        )

        self.assertEqual(reserva.preco_total, Decimal("230.00"))

    def test_impede_data_final_menor_ou_igual_data_inicial(self):
        with self.assertRaisesMessage(
            ValidationError,
            "A data final deve ser maior que a inicial.",
        ):
            Reserva.objects.create(
                veiculo=self.veiculo,
                cliente=self.cliente,
                data_inicio=date(2026, 6, 10),
                data_fim=date(2026, 6, 10),
            )

    def test_impede_reserva_com_periodo_conflitante(self):
        Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date(2026, 6, 8),
            data_fim=date(2026, 6, 11),
        )

        with self.assertRaisesMessage(
            ValidationError,
            "Veículo já reservado neste período.",
        ):
            Reserva.objects.create(
                veiculo=self.veiculo,
                cliente=self.cliente,
                data_inicio=date(2026, 6, 10),
                data_fim=date(2026, 6, 12),
            )

    def test_soft_delete_remove_registro_do_manager_padrao(self):
        reserva = Reserva.objects.create(
            veiculo=self.veiculo,
            cliente=self.cliente,
            data_inicio=date(2026, 6, 8),
            data_fim=date(2026, 6, 11),
        )

        reserva.delete()

        self.assertEqual(Reserva.objects.count(), 0)
        self.assertEqual(Reserva.all_objects.count(), 1)


class AvaliacaoModelTests(TestCase):
    def test_impede_nota_fora_do_intervalo_de_um_a_cinco(self):
        veiculo = Veiculo.objects.create(
            marca="Honda",
            modelo="Civic",
            ano=2023,
            preco_diaria=Decimal("120.00"),
        )
        cliente = Cliente.objects.create(
            nome="Joao Souza",
            email="joao@example.com",
            cnh="98765432100",
            telefone="85988880000",
        )

        with self.assertRaisesMessage(
            ValidationError,
            "A nota deve estar entre 1 e 5.",
        ):
            Avaliacao.objects.create(
                cliente=cliente,
                veiculo=veiculo,
                nota=6,
                comentario="Nota invalida",
            )
