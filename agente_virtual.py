import random
import json
from cliente_mcp import MCPClient
from faker import Faker

fake = Faker('pt_BR')

class AgenteVirtual:
    def __init__(self, host=None):
        # Se estiver rodando fora do Docker, use localhost
        # Se estiver rodando dentro do Docker, use mcp_server
        if host is None:
            import os
            # Verifica se está rodando em um contêiner Docker
            if os.path.exists('/.dockerenv'):
                host = 'mcp_server'
            else:
                host = 'localhost'
        
        self.cliente_mcp = MCPClient(host=host)
        self.saudacoes = [
            "Olá! Sou o AutoBot, seu assistente virtual para consulta de automóveis.",
            "Oi! Eu sou o AutoBot, especialista em carros. Como posso te ajudar hoje?",
            "Bem-vindo ao AutoBot! Estou aqui para te ajudar a encontrar o carro perfeito."
        ]
        # Mapeamento de marcas completas para abreviações no banco de dados
        self.marcas_map = {
            'bmw': 'BM',
            'fiat': 'FI',
            'ford': 'FO',
            'hyundai': 'HY',
            'honda': 'HO',
            'mercedes': 'MB',
            'mercedes-benz': 'MB',
            'volkswagen': 'VW',
            'toyota': 'TO',
            'nissan': 'NI',
            'chevrolet': 'GM',
            'gm': 'GM'
        }
        self.perguntas = {
            'marca': ["Qual marca você está interessado?", "De qual marca você gostaria de ver os carros?"],
            'modelo': ["Tem algum modelo específico em mente?", "Qual modelo você está buscando?"],
            'ano': ["Qual o ano mínimo que você deseja?", "Dos carros mais novos, a partir de que ano?"],
            'combustivel': ["Qual tipo de combustível você prefere?", "Tem preferência por gasolina, álcool, flex ou outro?"],
            'preco': ["Qual sua faixa de preço máxima?", "Até quanto você pretende gastar?"]
        }
        self.respostas_positivas = ["sim", "claro", "com certeza", "quero", "positivo", "afirmativo"]
        self.respostas_negativas = ["não", "nao", "negativo", "nada", "nunca", "nem"]
    
    def iniciar(self):
        print(random.choice(self.saudacoes))
        print("Vamos começar com algumas perguntas para entender melhor o que você busca.")
        
        filtros = {}
        
        # Marca
        resposta = input(f"{random.choice(self.perguntas['marca'])} (ou digite 'listar' para ver as marcas disponíveis): ")
        if resposta.lower() == 'listar':
            print("Marcas disponíveis: Volkswagen, Fiat, Ford, Chevrolet, Hyundai, Toyota, Honda, Nissan, BMW, Mercedes-Benz")
            resposta = input("E então, qual marca você prefere? ")
        if resposta:
            filtros['marca'] = self.mapear_marca(resposta)
        
        # Modelo
        resposta = input(f"{random.choice(self.perguntas['modelo'])} ")
        if resposta:
            filtros['modelo'] = resposta
        
        # Ano
        resposta = input(f"{random.choice(self.perguntas['ano'])} (deixe em branco se não importa): ")
        if resposta:
            filtros['ano_min'] = int(resposta)
        
        # Combustível
        resposta = input(f"{random.choice(self.perguntas['combustivel'])} (Gasolina, Álcool, Diesel, Flex, Elétrico, Híbrido): ")
        if resposta:
            filtros['combustivel'] = self.mapear_combustivel(resposta)
        
        # Preço
        resposta = input(f"{random.choice(self.perguntas['preco'])} (em R$): ")
        if resposta:
            filtros['preco_max'] = float(resposta)
        
        # Apenas disponíveis
        resposta = input("Deseja ver apenas carros disponíveis para venda? [sim/não] ").lower()
        if resposta in self.respostas_positivas:
            filtros['disponivel'] = True
        
        print("\nÓtimo! Estou buscando os carros que combinam com o que você procura...\n")
        
        resultados = self.cliente_mcp.enviar_consulta(filtros)
        self.mostrar_resultados(resultados)
    
    def mapear_marca(self, marca):
        # Usar o mapeamento definido no __init__
        return self.marcas_map.get(marca.lower(), marca.upper()[:2])
    
    def mapear_combustivel(self, combustivel):
        combustiveis = {
            'gasolina': 'G',
            'álcool': 'A', 'alcool': 'A',
            'diesel': 'D',
            'flex': 'F',
            'elétrico': 'E', 'eletrico': 'E',
            'híbrido': 'H', 'hibrido': 'H'
        }
        return combustiveis.get(combustivel.lower(), combustivel.upper()[:1])
    
    def mostrar_resultados(self, resultados):
        if isinstance(resultados, list):
            if not resultados:
                print("Não encontrei nenhum carro com os filtros especificados.")
                return
            
            print(f"Encontrei {len(resultados)} carro(s) que combinam com sua busca:\n")
            for idx, carro in enumerate(resultados, 1):
                print(f"{idx}. {carro['fields']['marca']} {carro['fields']['modelo']} {carro['fields']['ano_fabricacao']}")
                print(f"   Cor: {carro['fields']['cor']}")
                print(f"   Km: {carro['fields']['quilometragem']:,} km")
                print(f"   Preço: R$ {float(carro['fields']['preco']):,.2f}\n")
        elif 'error' in resultados:
            print(f"Ocorreu um erro na busca: {resultados['error']}")
        else:
            print("Nenhum resultado encontrado ou formato de resposta inesperado.")

    def perguntar_nova_consulta(self):
        print("\n" + "-"*50)
        resposta = input("Deseja fazer uma nova consulta? [sim/não] ").lower()
        return resposta in self.respostas_positivas

if __name__ == '__main__':
    agente = AgenteVirtual()
    
    continuar = True
    while continuar:
        agente.iniciar()
        continuar = agente.perguntar_nova_consulta()
    
    print("\nObrigado por usar o AutoBot! Até a próxima!")
