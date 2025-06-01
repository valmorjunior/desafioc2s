# Sistema de Consulta de Automóveis

Este projeto implementa um sistema completo para consulta de automóveis, com comunicação cliente-servidor via protocolo MCP, interface web responsiva e um agente virtual para interação no terminal.

## Estrutura do Projeto

- `projeto_automoveis/`: Projeto Django principal
  - `automoveis/`: Aplicação Django para o modelo de automóveis
    - `templates/`: Templates HTML para a interface web
    - `views.py`: Controladores para as páginas e APIs
    - `models.py`: Modelo de dados dos automóveis
- `servidor_mcp.py`: Implementação do servidor MCP para comunicação via socket
- `cliente_mcp.py`: Cliente MCP para comunicação com o servidor
- `agente_virtual.py`: Agente virtual para interação no terminal
- `executar_agente.sh`: Script para executar o agente virtual dentro ou fora do Docker
- `teste_agente.py`: Script para testar a comunicação com o servidor MCP
- `populate_automoveis.py`: Script para popular o banco de dados com dados fictícios
- `docker-compose.yml`: Configuração dos serviços Docker (web, banco de dados, servidor MCP)

## Requisitos

- Python 3.9+
- Django 3.2
- PostgreSQL (para ambiente Docker)
- Faker (para geração de dados fictícios)
- unittest (para execução de testes unitários)

## Instruções para Execução

### Usando Docker (Recomendado)

1. Construa e inicie os containers:
```bash
docker-compose up -d --build
```

2. Aplique as migrações (se necessário):
```bash
docker-compose exec web python manage.py migrate
```

3. Popule o banco de dados com dados fictícios:
```bash
docker-compose exec web python populate_automoveis.py
```

4. Acesse a interface web:
```
http://localhost:8000
```

5. Para usar o agente virtual, execute o script auxiliar:
```bash
./executar_agente.sh
```
Ou diretamente:
```bash
docker-compose exec web python agente_virtual.py
```

### Sem Docker

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente:
```bash
export DATABASE_URL=sqlite:///db.sqlite3
export PYTHONPATH=/caminho/para/o/projeto
```

3. Aplique as migrações:
```bash
python manage.py migrate
```

4. Popule o banco de dados:
```bash
python populate_automoveis.py
```

5. Em um terminal, inicie o servidor MCP:
```bash
python servidor_mcp.py
```

6. Em outro terminal, inicie o servidor web Django:
```bash
python manage.py runserver
```

7. Em um terceiro terminal, inicie o agente virtual ou use o script auxiliar:
```bash
./executar_agente.sh
```
Ou diretamente:
```bash
python agente_virtual.py
```

## Executando os Testes Unitários

O projeto inclui testes unitários para todas as partes principais do sistema:

- **Testes Django**: Testes para o modelo Automovel e para as views (index, api_automoveis, busca_rapida)
- **Testes MCP**: Testes para o cliente MCP (comunicação com o servidor)
- **Testes Agente Virtual**: Testes para o agente virtual (mapeamento de marcas, combustíveis e interação com o usuário)

Para executar todos os testes de uma vez, use o script `run_tests.sh`:

```bash
# Em ambiente local
./run_tests.sh

# Ou dentro do container Docker
docker-compose exec web bash -c "./run_tests.sh"
```

### Detalhes dos Testes

1. **Testes Django** (`automoveis/tests.py`):
   - Testes para o modelo Automovel (criação, representação string, métodos display)
   - Testes para as views (index, api_automoveis, busca_rapida)
   - Testes para os filtros e ordenação da busca rápida

2. **Testes MCP** (`tests/test_mcp_components.py`):
   - Testes para o cliente MCP (envio de consultas, tratamento de respostas)
   - Utiliza mocks para simular a comunicação com o servidor

3. **Testes Agente Virtual** (`tests/test_agente_virtual.py`):
   - Testes para mapeamento de marcas (ex: "volkswagen" -> "VW", "chevrolet" -> "GM")
   - Testes para mapeamento de combustíveis (ex: "flex" -> "F")
   - Testes para exibição de resultados e interação com o usuário

## Funcionalidades Principais

### 1. Agente Virtual (Terminal)

- Interface conversacional para busca de automóveis via terminal
- Coleta interativa de filtros (marca, modelo, ano, combustível, etc.)
- Mapeamento automático de nomes de marcas completos para códigos do banco de dados
- Exibição formatada dos resultados com preços em formato monetário
- Opção para realizar múltiplas consultas em uma única sessão
- Detecção automática do ambiente (Docker ou local) para conexão com o servidor MCP

### 2. Interface Web

- Página inicial com estatísticas do sistema
- Formulário de busca rápida com os seguintes recursos:
  - Filtro por marca (dropdown com todas as marcas disponíveis)
  - Filtro por modelo (busca parcial por texto)
  - Filtro por tipo de combustível
  - Filtro por disponibilidade
  - Ordenação por preço (crescente/decrescente)
  - Ordenação por quilometragem (crescente/decrescente)
  - Ordenação por ano (mais novo/mais antigo)
- Exibição de resultados em tempo real via AJAX
- Design responsivo com Bootstrap
- Elementos visuais destacados para preço e quilometragem
- Indicadores coloridos de disponibilidade (verde para disponível, vermelho para indisponível)

### 3. Servidor MCP

- Comunicação via sockets TCP
- Processamento de filtros em formato JSON
- Construção dinâmica de consultas ao banco de dados
- Serialização de resultados para JSON
- Compatibilidade com ambiente Docker (bind em 0.0.0.0)

## Fluxo do Sistema

### Fluxo do Agente Virtual

1. O usuário interage com o Agente Virtual no terminal
2. O Agente coleta os parâmetros de busca de forma conversacional
3. O Agente envia os filtros para o Servidor MCP via socket
4. O Servidor MCP consulta o banco de dados Django
5. O Servidor retorna os resultados para o Agente
6. O Agente exibe os resultados de forma amigável para o usuário
7. O Agente pergunta se o usuário deseja realizar uma nova consulta

### Fluxo da Interface Web

1. O usuário acessa a página inicial do sistema
2. Preenche o formulário de busca rápida com os filtros desejados
3. Ao submeter o formulário, uma requisição AJAX é enviada ao servidor
4. O servidor processa os filtros e retorna os resultados em formato JSON
5. O JavaScript atualiza a interface com os resultados formatados
6. O usuário pode refinar a busca ou ordenar os resultados conforme necessário

## Modelagem de Dados

O sistema utiliza um modelo `Automovel` com os seguintes campos:
- Marca (com opções pré-definidas)
- Modelo
- Ano de fabricação e modelo
- Motorização
- Combustível (Gasolina, Álcool, Diesel, Flex, Elétrico, Híbrido)
- Cor
- Quilometragem
- Número de portas
- Transmissão (Automática, Manual, Semi-automática)
- Preço
- Descrição
- Disponibilidade
