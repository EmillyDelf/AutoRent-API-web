from decimal import Decimal

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


# SOFT DELETE MANAGER
# Quando utilizar:
# Veiculo.objects.all()
# apenas registros não deletados serão retornados.
# Os deletados continuam no banco para auditoria.

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            deleted_at__isnull=True
        )

# BASE MODEL
# Todos os modelos herdam: created_at, updated_at, deleted_at

class BaseModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    objects = SoftDeleteManager()

    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Soft Delete

        Em vez de remover o registro
        do banco de dados.

        Apenas marca uma data de exclusão.
        """

        self.deleted_at = timezone.now()
        self.save()

# VEÍCULO
# Representa um carro disponível para aluguel.
# Futuramente (p4) pode ser consumido por uma aplicação React.

class Veiculo(BaseModel):

    marca = models.CharField(
        max_length=100
    )

    modelo = models.CharField(
        max_length=100
    )

    ano = models.PositiveIntegerField()

    preco_diaria = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    disponivel = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.marca} {self.modelo}"


# CLIENTE

# Não estamos utilizando o User padrão do Django nesta primeira fase.
# Futuramente pode ser integrado ao sistema de autenticação.

class Cliente(BaseModel):

    nome = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    cnh = models.CharField(
        max_length=20,
        unique=True
    )

    telefone = models.CharField(
        max_length=20
    )

    def __str__(self):
        return self.nome

# RESERVA
# Núcleo do sistema.

# Responsável por: aluguel, disponibilidade, preço dinâmico

class Reserva(BaseModel):

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

    STATUS_CHOICES = (
        ("PENDENTE", "Pendente"),
        ("CONFIRMADA", "Confirmada"),
        ("FINALIZADA", "Finalizada"),
        ("CANCELADA", "Cancelada"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDENTE"
    )

    def clean(self):

        # REGRA
        # Data final maior que inicial

        if self.data_fim <= self.data_inicio:

            raise ValidationError(
                "A data final deve ser maior que a inicial."
            )

        # REGRA 
        # Impedir dupla reserva

        conflito = Reserva.objects.filter(
            veiculo=self.veiculo,
            data_inicio__lt=self.data_fim,
            data_fim__gt=self.data_inicio
        ).exclude(
            id=self.id
        )

        if conflito.exists():

            raise ValidationError(
                "Veículo já reservado neste período."
            )

    def save(self, *args, **kwargs):

        self.clean()

        dias = (
            self.data_fim -
            self.data_inicio
        ).days

        valor_base = (
            self.veiculo.preco_diaria
            * dias
        )

        # PREÇO DINÂMICO no fds : Sextou, Sábadou, Domingou
        # +15%

        if self.data_inicio.weekday() in [4, 5, 6]:

            valor_base = (
                valor_base *
                Decimal("1.15")
            )

        self.preco_total = valor_base

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.cliente.nome}"
            f" -> "
            f"{self.veiculo.modelo}"
        )

# AVALIAÇÃO

class Avaliacao(BaseModel):

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE
    )

    nota = models.PositiveSmallIntegerField()

    comentario = models.TextField()

    def clean(self):

        if self.nota < 1 or self.nota > 5:

            raise ValidationError(
                "A nota deve estar entre 1 e 5."
            )

    def save(self, *args, **kwargs):

        self.clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.cliente.nome}"
            f" - "
            f"{self.nota}"
        )
