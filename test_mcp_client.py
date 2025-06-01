#!/usr/bin/env python
"""
Script para testar a comunicação cliente-servidor via MCP.
Este script envia uma consulta simples ao servidor MCP e exibe os resultados.
"""
import json
from cliente_mcp import MCPClient

def main():
    print("=== Teste de Comunicação MCP ===")
    
    # Cria um cliente MCP
    cliente = MCPClient()
    
    # Define filtros de exemplo
    filtros = {
        'marca': 'VW',
        'ano_min': 2015,
        'disponivel': True
    }
    
    print(f"Enviando consulta com filtros: {filtros}")
    
    # Envia a consulta ao servidor
    try:
        resultados = cliente.enviar_consulta(filtros)
        
        if 'error' in resultados:
            print(f"Erro na consulta: {resultados['error']}")
        else:
            print(f"Recebidos {len(resultados)} resultados:")
            
            for i, automovel in enumerate(resultados[:5], 1):  # Mostra apenas os 5 primeiros
                fields = automovel.get('fields', {})
                print(f"{i}. {fields.get('marca')} {fields.get('modelo')} ({fields.get('ano_fabricacao')})")
                print(f"   Preço: R$ {fields.get('preco', 0):,.2f}")
                print(f"   Km: {fields.get('quilometragem', 0):,}")
                print()
                
            if len(resultados) > 5:
                print(f"... e mais {len(resultados) - 5} automóveis.")
    
    except Exception as e:
        print(f"Erro ao conectar ao servidor MCP: {e}")
        print("Certifique-se de que o servidor MCP está em execução (python servidor_mcp.py)")

if __name__ == "__main__":
    main()
