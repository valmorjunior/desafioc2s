#!/usr/bin/env python
import json
from cliente_mcp import MCPClient

def teste_consulta():
    """Testa uma consulta específica ao servidor MCP."""
    print("Testando consulta ao servidor MCP...")
    
    # Criar filtros com os mesmos parâmetros da consulta do usuário
    filtros = {
        'marca': 'BM',           # BMW
        'modelo': 'Labore',      # Modelo contendo "Labore"
        'combustivel': 'F',      # Flex
        'preco_max': 100000.0,   # Preço máximo de R$ 100.000
        'disponivel': True       # Apenas carros disponíveis
    }
    
    try:
        # Criar cliente MCP e enviar consulta
        cliente = MCPClient()
        print(f"Enviando consulta com filtros: {json.dumps(filtros, indent=2)}")
        resultados = cliente.enviar_consulta(filtros)
        
        # Exibir resultados
        if isinstance(resultados, list):
            if not resultados:
                print("Não foram encontrados carros com os filtros especificados.")
            else:
                print(f"Encontrados {len(resultados)} carro(s):")
                for idx, carro in enumerate(resultados, 1):
                    print(f"{idx}. {carro['fields']['marca']} {carro['fields']['modelo']} {carro['fields']['ano_fabricacao']}")
                    print(f"   Combustível: {carro['fields']['combustivel']}")
                    print(f"   Preço: R$ {float(carro['fields']['preco']):,.2f}")
                    print(f"   Disponível: {'Sim' if carro['fields']['disponivel'] else 'Não'}\n")
        else:
            print(f"Erro ou formato inesperado na resposta: {resultados}")
    
    except Exception as e:
        print(f"Erro na consulta: {e}")

if __name__ == "__main__":
    teste_consulta()
