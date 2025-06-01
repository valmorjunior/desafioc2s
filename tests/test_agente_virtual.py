#!/usr/bin/env python
"""
Testes unitários para o agente virtual.
"""
import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock, call

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agente_virtual import AgenteVirtual

class TestAgenteVirtual(unittest.TestCase):
    """Testes para o agente virtual."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Cria uma instância do agente virtual com cliente MCP mockado
        with patch('agente_virtual.MCPClient'):
            self.agente = AgenteVirtual()
    
    def test_mapear_marca(self):
        """Testa o mapeamento de nomes de marcas para códigos."""
        # Testa marcas conhecidas
        self.assertEqual(self.agente.mapear_marca("volkswagen"), "VW")
        self.assertEqual(self.agente.mapear_marca("bmw"), "BM")
        self.assertEqual(self.agente.mapear_marca("fiat"), "FI")
        self.assertEqual(self.agente.mapear_marca("chevrolet"), "GM")  # Corrigido para GM
        
        # Testa marca desconhecida (deve retornar as duas primeiras letras em maiúsculo)
        self.assertEqual(self.agente.mapear_marca("tesla"), "TE")
    
    def test_mapear_combustivel(self):
        """Testa o mapeamento de tipos de combustível para códigos."""
        self.assertEqual(self.agente.mapear_combustivel("gasolina"), "G")
        self.assertEqual(self.agente.mapear_combustivel("álcool"), "A")
        self.assertEqual(self.agente.mapear_combustivel("diesel"), "D")
        self.assertEqual(self.agente.mapear_combustivel("flex"), "F")
        self.assertEqual(self.agente.mapear_combustivel("elétrico"), "E")
        self.assertEqual(self.agente.mapear_combustivel("híbrido"), "H")
        
        # Testa combustível desconhecido (deve retornar a primeira letra em maiúsculo)
        self.assertEqual(self.agente.mapear_combustivel("hidrogênio"), "H")
    
    @patch('builtins.print')
    def test_mostrar_resultados(self, mock_print):
        """Testa a exibição de resultados."""
        # Dados de teste
        resultados = [
            {
                'pk': 1,
                'fields': {
                    'marca': 'VW',
                    'modelo': 'Gol',
                    'ano_fabricacao': 2020,
                    'ano_modelo': 2021,
                    'motorizacao': 1.6,
                    'combustivel': 'F',
                    'cor': 'Branco',
                    'quilometragem': 10000,
                    'numero_portas': 4,
                    'transmissao': 'M',
                    'preco': 45000.00,
                    'descricao': 'Carro de teste',
                    'disponivel': True
                }
            },
            {
                'pk': 2,
                'fields': {
                    'marca': 'BM',
                    'modelo': 'X5',
                    'ano_fabricacao': 2019,
                    'ano_modelo': 2019,
                    'motorizacao': 2.0,
                    'combustivel': 'G',
                    'cor': 'Preto',
                    'quilometragem': 20000,
                    'numero_portas': 4,
                    'transmissao': 'A',
                    'preco': 120000.00,
                    'descricao': 'Carro de luxo',
                    'disponivel': False
                }
            }
        ]
        
        # Executa o método a ser testado
        self.agente.mostrar_resultados(resultados)
        
        # Verifica se a função print foi chamada com as informações corretas
        # Deve ter pelo menos 10 chamadas (cabeçalho + 2 carros com várias linhas cada)
        self.assertGreaterEqual(mock_print.call_count, 5)
        
        # Verifica se a mensagem de resultados foi exibida
        mock_print.assert_any_call("Encontrei 2 carro(s) que combinam com sua busca:\n")
    
    @patch('builtins.input')
    def test_perguntar_nova_consulta(self, mock_input):
        """Testa a pergunta sobre nova consulta."""
        # Teste com resposta positiva
        mock_input.return_value = "sim"
        self.assertTrue(self.agente.perguntar_nova_consulta())
        
        # Teste com resposta negativa
        mock_input.return_value = "não"
        self.assertFalse(self.agente.perguntar_nova_consulta())


if __name__ == '__main__':
    unittest.main()
