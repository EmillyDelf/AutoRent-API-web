from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import (MinValueValidator, MaxValueValidator, RegexValidator,)

# --
# VALIDAÇÕES
# --

cpf_validator = RegexValidator(
    regex=r"^\d{11}$",
    message="CPF deve conter exatamente 11 números."
)

cep_validator = RegexValidator(
    regex=r"^\d{5}-?\d{3}$",
    message="CEP inválido. Exemplo: 56780-000"
)

placa_validator = RegexValidator(
    regex=r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$",
    message="Placa inválida. Exemplo: ABC1234 ou ABC1D23"
)

# --
# Manager para Soft Delete
# --

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            deleted_at__isnull=True
        )

# --
# Modelo base utilizado por todas as entidades
# --

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

# --
# Veículos disponíveis
# --
class Veiculo(BaseModel):

    STATUS_VEICULO = (
        ("DISPONIVEL", "Disponível"),
        ("ALUGADO", "Alugado"),
        ("MANUTENCAO", "Manutenção"),
    )

    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    ano = models.PositiveIntegerField()

    placa = models.CharField(
        max_length=10,
        unique=True,
        validators=[placa_validator]
    )

    preco_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_VEICULO,
        default="DISPONIVEL"
    )

    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"
        ordering = ["marca", "modelo"]

    def __str__(self):
        return f"{self.marca} {self.modelo}"

# --
# Clientes
# --

class Cliente(BaseModel):

    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[cpf_validator]
    )

    cnh = models.CharField(
        max_length=20,
        unique=True
    )

    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255)

    cep = models.CharField(
        max_length=9,
        validators=[cep_validator]
    )

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome

# --
# Reservas
# --

class Reserva(BaseModel):

    STATUS_RESERVA = (
        ("PENDENTE", "Pendente"),
        ("CONFIRMADA", "Confirmada"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.PROTECT,
        related_name="reservas"
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="reservas"
    )

    data_inicio = models.DateField()
    data_fim = models.DateField()

    preco_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_RESERVA,
        default="PENDENTE"
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):

        if self.data_fim <= self.data_inicio:
            raise ValidationError(
                "A data final deve ser maior que a data inicial."
            )

        conflito = (
            Reserva.objects.filter(
                veiculo=self.veiculo,
                data_inicio__lt=self.data_fim,
                data_fim__gt=self.data_inicio,
            )
            .exclude(pk=self.pk)
            .exclude(status="CANCELADA")
        )

        if conflito.exists():
            raise ValidationError(
                "Veículo já reservado neste período."
            )

    def save(self, *args, **kwargs):

        self.full_clean()

        dias = (
            self.data_fim - self.data_inicio
        ).days

        valor_base = (
            self.veiculo.preco_diaria * dias
        )

        if self.data_inicio.weekday() in [4, 5, 6]:
            valor_base *= Decimal("1.15")

        self.preco_total = valor_base

        super().save(*args, **kwargs)

        if self.status == "CONFIRMADA":
            self.veiculo.status = "ALUGADO"

        elif self.status in ["FINALIZADA", "CANCELADA"]:
            self.veiculo.status = "DISPONIVEL"

        self.veiculo.save()

    def __str__(self):
        return f"{self.cliente.nome} - {self.veiculo.modelo}"

# --
# Pagamentos
# --
class Pagamento(BaseModel):

    METODO_PAGAMENTO = (
        ("PIX", "PIX"),
        ("CARTAO_CREDITO", "Cartão de Crédito"),
        ("CARTAO_DEBITO", "Cartão de Débito"),
        ("DINHEIRO", "Dinheiro"),
    )

    STATUS_PAGAMENTO = (
        ("PENDENTE", "Pendente"),
        ("PAGO", "Pago"),
        ("CANCELADO", "Cancelado"),
    )

    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name="pagamento"
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    metodo = models.CharField(
        max_length=20,
        choices=METODO_PAGAMENTO
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_PAGAMENTO,
        default="PENDENTE"
    )

    data_pagamento = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        if self.valor is None:
            self.valor = self.reserva.preco_total

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pagamento #{self.id}"

# --
# Avaliações
# --
class Avaliacao(BaseModel):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="avaliacoes"
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name="avaliacoes"
    )

    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)
        ]
    )

    comentario = models.TextField()

    def __str__(self):
        return f"{self.cliente.nome} - {self.nota}"