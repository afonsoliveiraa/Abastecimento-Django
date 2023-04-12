from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.

class Unidade_Orcamentaria(models.Model):
    codigo = models.CharField(max_length=5)
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.codigo} - {self.descricao}'


class Veiculo(models.Model):
    placa = models.CharField(max_length=8)
    unidade = models.ForeignKey(Unidade_Orcamentaria, on_delete=models.PROTECT, related_name='unidade_veiculo')
    km = models.PositiveBigIntegerField()
    tipo = models.CharField(max_length=255)
    linha = models.CharField(max_length=255)

    def __str__(self):
        return self.placa


class Contrato(models.Model):
    numero = models.CharField(max_length=255)
    unidade = models.ForeignKey(Unidade_Orcamentaria, on_delete=models.PROTECT, related_name='unidade_contrato')
    valor_atual = models.DecimalField(max_digits=6, decimal_places=2)
    valor_original = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.numero

    def save(self, *args, **kwargs):
        if not self.pk:  # verifica se é uma nova instância de Contrato
            self.valor_atual = self.valor_original  # define valor_atual igual a valor_original
        super().save(*args, **kwargs)


class Abastecimento(models.Model):
    data = models.DateField()
    valor = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.data} - {self.valor}, {self.contrato}'


class Item_Abastecimento(models.Model):
    COMBUSTIVEL_CHOICES = (
        ('Gasolina', 'Gasolina'),
        ('Álcool', 'Álcool'),
        ('Diesel', 'Diesel')
    )
    abastecimento = models.ForeignKey(Abastecimento, on_delete=models.PROTECT, related_name='item')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='veiculo_item')
    combustivel = models.CharField(max_length=255, choices=COMBUSTIVEL_CHOICES)
    quantidade_combustivel = models.PositiveBigIntegerField()
    valor_unitario = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f'Item Abastecimento {self.veiculo}'


class Update(models.Model):
    autor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    conteudo = models.TextField()

    def __str__(self):
        return {self.conteudo}
