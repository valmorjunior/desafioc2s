#!/usr/bin/env python
"""
Script para testar todos os componentes do sistema de consulta de automóveis.
Este script verifica se o banco de dados, o servidor MCP e o cliente estão funcionando corretamente.
"""
import os
import sys
import socket
import time
import json
import django

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_automoveis.settings')
django.setup()

from automoveis.models import Automovel
from cliente_mcp import MCPClient

def check_database():
    """Verifica se o banco de dados está acessível e contém dados."""
    print("Verificando banco de dados...")
    try:
        count = Automovel.objects.count()
        print(f"✓ Banco de dados OK: {count} automóveis encontrados.")
        return count > 0
    except Exception as e:
        print(f"✗ Erro ao acessar o banco de dados: {e}")
        return False

def check_mcp_server(host='localhost', port=9999):
    """Verifica se o servidor MCP está em execução."""
    print(f"Verificando servidor MCP em {host}:{port}...")
    try:
        # Tenta conectar ao servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✓ Servidor MCP está em execução.")
            return True
        else:
            print("✗ Servidor MCP não está em execução.")
            return False
    except Exception as e:
        print(f"✗ Erro ao verificar servidor MCP: {e}")
        return False

def test_mcp_client():
    """Testa o cliente MCP enviando uma consulta simples."""
    print("Testando cliente MCP...")
    try:
        cliente = MCPClient()
        filtros = {'disponivel': True}
        resultados = cliente.enviar_consulta(filtros)
        
        if 'error' in resultados:
            print(f"✗ Erro na consulta MCP: {resultados['error']}")
            return False
        else:
            print(f"✓ Cliente MCP OK: {len(resultados)} resultados recebidos.")
            return True
    except Exception as e:
        print(f"✗ Erro ao testar cliente MCP: {e}")
        return False

def main():
    print("=== Teste do Sistema de Consulta de Automóveis ===\n")
    
    # Verifica todos os componentes
    db_ok = check_database()
    server_ok = check_mcp_server()
    
    # Só testa o cliente se o servidor estiver rodando
    client_ok = test_mcp_client() if server_ok else False
    
    print("\n=== Resultado do Teste ===")
    print(f"Banco de dados: {'✓' if db_ok else '✗'}")
    print(f"Servidor MCP: {'✓' if server_ok else '✗'}")
    print(f"Cliente MCP: {'✓' if client_ok else '✗'}")
    
    # Sugere ações com base nos resultados
    print("\n=== Próximos Passos ===")
    if not db_ok:
        print("- Execute 'python populate_automoveis.py' para popular o banco de dados.")
    
    if not server_ok:
        print("- Execute 'python servidor_mcp.py' para iniciar o servidor MCP.")
    
    if db_ok and server_ok and client_ok:
        print("Todos os componentes estão funcionando corretamente!")
        print("- Execute 'python agente_virtual.py' para interagir com o sistema.")
        print("- Ou use 'python cli_consulta.py --help' para consultas via linha de comando.")
    
    return all([db_ok, server_ok, client_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
