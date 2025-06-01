from django.test import TestCase
from django.urls import reverse
from .models import Automovel
from django.db.models import Q
import json

class AutomovelModelTestCase(TestCase):
    """Testes para o modelo Automovel."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar alguns automóveis para testes
        Automovel.objects.create(
            marca="VW",
            modelo="Gol",
            ano_fabricacao=2020,
            ano_modelo=2021,
            motorizacao=1.6,
            combustivel="F",
            cor="Branco",
            quilometragem=10000,
            numero_portas=4,
            transmissao="M",
            preco=45000.00,
            descricao="Carro de teste",
            disponivel=True
        )
        
        Automovel.objects.create(
            marca="BM",
            modelo="X5",
            ano_fabricacao=2019,
            ano_modelo=2019,
            motorizacao=2.0,
            combustivel="G",
            cor="Preto",
            quilometragem=20000,
            numero_portas=4,
            transmissao="A",
            preco=120000.00,
            descricao="Carro de luxo",
            disponivel=False
        )
    
    def test_automovel_creation(self):
        """Testa se os automóveis foram criados corretamente."""
        gol = Automovel.objects.get(modelo="Gol")
        bmw = Automovel.objects.get(modelo="X5")
        
        self.assertEqual(gol.marca, "VW")
        self.assertEqual(gol.ano_fabricacao, 2020)
        self.assertEqual(gol.combustivel, "F")
        self.assertTrue(gol.disponivel)
        
        self.assertEqual(bmw.marca, "BM")
        self.assertEqual(bmw.preco, 120000.00)
        self.assertFalse(bmw.disponivel)
    
    def test_str_representation(self):
        """Testa a representação string do modelo."""
        gol = Automovel.objects.get(modelo="Gol")
        self.assertEqual(str(gol), "Volkswagen Gol 2020")
    
    def test_get_marca_display(self):
        """Testa se o método get_marca_display retorna o nome correto da marca."""
        gol = Automovel.objects.get(modelo="Gol")
        bmw = Automovel.objects.get(modelo="X5")
        
        self.assertEqual(gol.get_marca_display(), "Volkswagen")
        self.assertEqual(bmw.get_marca_display(), "BMW")
    
    def test_get_combustivel_display(self):
        """Testa se o método get_combustivel_display retorna o tipo correto de combustível."""
        gol = Automovel.objects.get(modelo="Gol")
        bmw = Automovel.objects.get(modelo="X5")
        
        self.assertEqual(gol.get_combustivel_display(), "Flex")
        self.assertEqual(bmw.get_combustivel_display(), "Gasolina")


class ViewsTestCase(TestCase):
    """Testes para as views da aplicação."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Criar alguns automóveis para testes
        Automovel.objects.create(
            marca="VW",
            modelo="Gol",
            ano_fabricacao=2020,
            ano_modelo=2021,
            motorizacao=1.6,
            combustivel="F",
            cor="Branco",
            quilometragem=10000,
            numero_portas=4,
            transmissao="M",
            preco=45000.00,
            descricao="Carro de teste",
            disponivel=True
        )
        
        Automovel.objects.create(
            marca="BM",
            modelo="X5",
            ano_fabricacao=2019,
            ano_modelo=2019,
            motorizacao=2.0,
            combustivel="G",
            cor="Preto",
            quilometragem=20000,
            numero_portas=4,
            transmissao="A",
            preco=120000.00,
            descricao="Carro de luxo",
            disponivel=False
        )
    
    def test_index_view(self):
        """Testa se a view index carrega corretamente."""
        response = self.client.get(reverse('automoveis:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'automoveis/index.html')
        self.assertContains(response, "Sistema de Consulta de Automóveis")
        self.assertContains(response, "Consulta Rápida")
        
        # Verifica se o contexto contém as informações necessárias
        self.assertIn('total_automoveis', response.context)
        self.assertIn('marcas', response.context)
        self.assertIn('combustiveis', response.context)
        
        # Verifica se o total de automóveis está correto
        self.assertEqual(response.context['total_automoveis'], 2)
    
    def test_api_automoveis_view(self):
        """Testa se a API de automóveis retorna os dados corretamente."""
        response = self.client.get(reverse('automoveis:api_automoveis'))
        self.assertEqual(response.status_code, 200)
        
        # Converte a resposta JSON em uma lista de dicionários
        data = json.loads(response.content)
        
        # Verifica se a resposta contém os automóveis esperados
        self.assertEqual(len(data), 2)
        
        # Verifica os dados do primeiro automóvel
        self.assertEqual(data[0]['marca'], "Volkswagen")
        self.assertEqual(data[0]['modelo'], "Gol")
        self.assertEqual(data[0]['ano_fabricacao'], 2020)
        self.assertEqual(data[0]['preco'], 45000.0)
        self.assertTrue(data[0]['disponivel'])
    
    def test_busca_rapida_view(self):
        """Testa a funcionalidade de busca rápida."""
        # Teste com filtro de marca
        response = self.client.post(
            reverse('automoveis:busca_rapida'),
            {'marca': 'VW'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['marca'], "Volkswagen")
        
        # Teste com filtro de disponibilidade
        response = self.client.post(
            reverse('automoveis:busca_rapida'),
            {'disponivel': 'on'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)
        self.assertTrue(data[0]['disponivel'])
        
        # Teste com ordenação por preço (crescente)
        response = self.client.post(
            reverse('automoveis:busca_rapida'),
            {'ordenacao': 'preco_asc'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['preco'], 45000.0)
        self.assertEqual(data[1]['preco'], 120000.0)
        
        # Teste com ordenação por preço (decrescente)
        response = self.client.post(
            reverse('automoveis:busca_rapida'),
            {'ordenacao': 'preco_desc'}
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]['preco'], 120000.0)
        self.assertEqual(data[1]['preco'], 45000.0)
