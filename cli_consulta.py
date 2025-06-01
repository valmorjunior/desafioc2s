#!/usr/bin/env python
"""
Interface de linha de comando para consulta de automóveis.
Uma alternativa mais direta ao agente virtual.
"""
import argparse
import json
from cliente_mcp import MCPClient

def main():
    parser = argparse.ArgumentParser(description='Consulta de automóveis via MCP')
    parser.add_argument('--marca', help='Marca do automóvel (VW, FI, FO, GM, etc)')
    parser.add_argument('--modelo', help='Modelo do automóvel')
    parser.add_argument('--ano-min', type=int, help='Ano mínimo de fabricação')
    parser.add_argument('--ano-max', type=int, help='Ano máximo de fabricação')
    parser.add_argument('--combustivel', help='Tipo de combustível (G, A, D, F, E, H)')
    parser.add_argument('--preco-min', type=float, help='Preço mínimo')
    parser.add_argument('--preco-max', type=float, help='Preço máximo')
    parser.add_argument('--disponivel', action='store_true', help='Apenas automóveis disponíveis')
    parser.add_argument('--formato', choices=['texto', 'json'], default='texto', 
                        help='Formato de saída (texto ou json)')
    
    args = parser.parse_args()
    
    # Constrói o dicionário de filtros a partir dos argumentos
    filtros = {}
    if args.marca:
        filtros['marca'] = args.marca
    if args.modelo:
        filtros['modelo'] = args.modelo
    if args.ano_min:
        filtros['ano_min'] = args.ano_min
    if args.ano_max:
        filtros['ano_max'] = args.ano_max
    if args.combustivel:
        filtros['combustivel'] = args.combustivel
    if args.preco_min:
        filtros['preco_min'] = args.preco_min
    if args.preco_max:
        filtros['preco_max'] = args.preco_max
    if args.disponivel:
        filtros['disponivel'] = True
    
    # Se não houver filtros, exibe ajuda
    if not filtros:
        parser.print_help()
        print("\nExemplo de uso:")
        print("  python cli_consulta.py --marca VW --ano-min 2015 --disponivel")
        return
    
    # Realiza a consulta
    cliente = MCPClient()
    try:
        resultados = cliente.enviar_consulta(filtros)
        
        if 'error' in resultados:
            print(f"Erro: {resultados['error']}")
            return
        
        # Exibe os resultados no formato solicitado
        if args.formato == 'json':
            print(json.dumps(resultados, indent=2, ensure_ascii=False))
        else:
            if not resultados:
                print("Nenhum automóvel encontrado com os filtros especificados.")
                return
            
            print(f"\nEncontrados {len(resultados)} automóveis:\n")
            for i, auto in enumerate(resultados, 1):
                fields = auto['fields']
                print(f"{i}. {fields.get('marca')} {fields.get('modelo')} ({fields.get('ano_fabricacao')})")
                print(f"   Cor: {fields.get('cor')}")
                print(f"   Motor: {fields.get('motorizacao')} | Combustível: {fields.get('combustivel')}")
                print(f"   Km: {fields.get('quilometragem'):,}")
                print(f"   Preço: R$ {fields.get('preco'):,.2f}")
                print(f"   Disponível: {'Sim' if fields.get('disponivel') else 'Não'}")
                print()
    
    except Exception as e:
        print(f"Erro ao conectar ao servidor MCP: {e}")
        print("Certifique-se de que o servidor MCP está em execução (python servidor_mcp.py)")

if __name__ == '__main__':
    main()
