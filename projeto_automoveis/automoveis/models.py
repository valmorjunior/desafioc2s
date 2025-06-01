from django.db import models

class Automovel(models.Model):
    MARCA_CHOICES = [
        ('VW', 'Volkswagen'),
        ('FI', 'Fiat'),
        ('FO', 'Ford'),
        ('GM', 'Chevrolet'),
        ('HY', 'Hyundai'),
        ('TO', 'Toyota'),
        ('HO', 'Honda'),
        ('NI', 'Nissan'),
        ('BM', 'BMW'),
        ('MB', 'Mercedes-Benz'),
    ]
    
    COMBUSTIVEL_CHOICES = [
        ('G', 'Gasolina'),
        ('A', 'Álcool'),
        ('D', 'Diesel'),
        ('F', 'Flex'),
        ('E', 'Elétrico'),
        ('H', 'Híbrido'),
    ]
    
    TRANSMISSAO_CHOICES = [
        ('A', 'Automática'),
        ('M', 'Manual'),
        ('S', 'Semi-automática'),
    ]
    
    marca = models.CharField(max_length=2, choices=MARCA_CHOICES)
    modelo = models.CharField(max_length=50)
    ano_fabricacao = models.PositiveIntegerField()
    ano_modelo = models.PositiveIntegerField()
    motorizacao = models.DecimalField(max_digits=2, decimal_places=1)
    combustivel = models.CharField(max_length=1, choices=COMBUSTIVEL_CHOICES)
    cor = models.CharField(max_length=30)
    quilometragem = models.PositiveIntegerField()
    numero_portas = models.PositiveIntegerField(choices=[(2, '2 portas'), (4, '4 portas')])
    transmissao = models.CharField(max_length=1, choices=TRANSMISSAO_CHOICES)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_marca_display()} {self.modelo} {self.ano_fabricacao}"
