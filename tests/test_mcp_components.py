#!/usr/bin/env python
"""
Testes unitários simplificados para o cliente MCP.
"""
import unittest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cliente_mcp import MCPClient

class TestMCPClient(unittest.TestCase):
    """Testes básicos para o cliente MCP."""
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.client = MCPClient(host='localhost', port=9999)
    
    @patch('cliente_mcp.MCPClient.enviar_consulta')
    def test_enviar_consulta_mock(self, mock_enviar):
        """Testa o envio de consulta usando um mock direto."""
        # Configura o mock para retornar um resultado predefinido
        mock_resultado = [
            {"fields": {"marca": "VW", "modelo": "Gol", "preco": 45000.0}}
        ]
        mock_enviar.return_value = mock_resultado
        
        # Filtros de teste
        filtros = {
            'marca': 'VW',
            'disponivel': True
        }
        
        # Cria uma nova instância para evitar conflitos com o patch
        client = MCPClient()
        resultado = client.enviar_consulta(filtros)
        
        # Verifica se o mock foi chamado com os filtros corretos
        mock_enviar.assert_called_once_with(filtros)
        
        # Verifica se o resultado é o esperado
        self.assertEqual(resultado, mock_resultado)


if __name__ == '__main__':
    unittest.main()
