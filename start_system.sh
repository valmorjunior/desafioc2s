#!/bin/bash

# Script para iniciar todos os componentes do sistema de consulta de automóveis
echo "=== Iniciando Sistema de Consulta de Automóveis ==="

# Verifica se o ambiente virtual está ativado
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Aviso: É recomendado ativar um ambiente virtual Python antes de executar este script."
    read -p "Deseja continuar mesmo assim? (s/n): " resposta
    if [[ "$resposta" != "s" ]]; then
        echo "Operação cancelada."
        exit 1
    fi
fi

# Verifica se as dependências estão instaladas
echo "Verificando dependências..."
pip install -r requirements.txt

# Aplica migrações do Django
echo "Aplicando migrações do banco de dados..."
python manage.py migrate

# Verifica se há automóveis no banco de dados
echo "Verificando dados..."
TOTAL_AUTOS=$(python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_automoveis.settings'); django.setup(); from automoveis.models import Automovel; print(Automovel.objects.count())")

if [[ "$TOTAL_AUTOS" -eq "0" ]]; then
    echo "Banco de dados vazio. Deseja popular com dados fictícios? (s/n): "
    read resposta
    if [[ "$resposta" == "s" ]]; then
        echo "Populando banco de dados..."
        python populate_automoveis.py
    fi
else
    echo "Banco de dados já contém $TOTAL_AUTOS automóveis."
fi

# Inicia o servidor MCP em background
echo "Iniciando servidor MCP em background..."
python servidor_mcp.py > servidor_mcp.log 2>&1 &
MCP_PID=$!
echo "Servidor MCP iniciado (PID: $MCP_PID)"

# Inicia o servidor Django
echo "Iniciando servidor Django..."
python manage.py runserver &
DJANGO_PID=$!
echo "Servidor Django iniciado (PID: $DJANGO_PID)"

echo ""
echo "=== Sistema iniciado com sucesso! ==="
echo "- Servidor Django: http://localhost:8000"
echo "- Servidor MCP: localhost:9999"
echo ""
echo "Para interagir com o sistema, execute em outro terminal:"
echo "python agente_virtual.py"
echo ""
echo "Para parar o sistema, pressione Ctrl+C"

# Função para encerrar processos ao sair
function cleanup {
    echo ""
    echo "Encerrando servidores..."
    kill $MCP_PID 2>/dev/null
    kill $DJANGO_PID 2>/dev/null
    echo "Sistema encerrado."
}

# Registra a função de limpeza para ser executada ao sair
trap cleanup EXIT

# Aguarda o usuário pressionar Ctrl+C
wait
