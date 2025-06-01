import os
import django
from faker import Faker
from random import randint, choice, uniform
import decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_automoveis.settings')
django.setup()

from automoveis.models import Automovel

fake = Faker('pt_BR')

def criar_automoveis(numero=100):
    marcas = [m[0] for m in Automovel.MARCA_CHOICES]
    combustiveis = [c[0] for c in Automovel.COMBUSTIVEL_CHOICES]
    transmissoes = [t[0] for t in Automovel.TRANSMISSAO_CHOICES]
    cores = ['Preto', 'Branco', 'Prata', 'Vermelho', 'Azul', 'Verde', 'Cinza', 'Amarelo', 'Laranja']
    
    for _ in range(numero):
        ano_fab = randint(2000, 2023)
        ano_mod = ano_fab if randint(0, 1) else ano_fab + 1
        motor = decimal.Decimal(randint(10, 30)/10)
        preco = decimal.Decimal(round(uniform(20000, 150000), 2))
        
        Automovel.objects.create(
            marca=choice(marcas),
            modelo=fake.word().capitalize(),
            ano_fabricacao=ano_fab,
            ano_modelo=ano_mod,
            motorizacao=motor,
            combustivel=choice(combustiveis),
            cor=choice(cores),
            quilometragem=randint(0, 200000),
            numero_portas=choice([2, 4]),
            transmissao=choice(transmissoes),
            preco=preco,
            descricao=fake.text(max_nb_chars=200),
            disponivel=choice([True, False])
        )

if __name__ == '__main__':
    print("Criando automóveis...")
    criar_automoveis(100)
    print("100 automóveis criados com sucesso!")
