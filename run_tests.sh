#!/bin/bash
# Script para executar todos os testes unitários do projeto

echo "=== Executando testes unitários do Sistema de Consulta de Automóveis ==="
echo

# Verifica se está rodando em ambiente Docker
if [ -f /.dockerenv ]; then
    echo "Detectado ambiente Docker"
    PYTHON_CMD="python"
    DJANGO_TEST_CMD="python manage.py test automoveis"
else
    echo "Executando em ambiente local"
    PYTHON_CMD="python"
    DJANGO_TEST_CMD="python projeto_automoveis/manage.py test automoveis"
    
    # Configura variáveis de ambiente para testes locais
    export PYTHONPATH=$PWD
    export DJANGO_SETTINGS_MODULE=projeto_automoveis.settings
fi

echo
echo "1. Executando testes do Django (modelos e views)..."
$DJANGO_TEST_CMD

echo
echo "2. Executando testes do cliente MCP..."
$PYTHON_CMD -m unittest tests.test_mcp_components

echo
echo "3. Executando testes do agente virtual..."
$PYTHON_CMD -m unittest tests.test_agente_virtual

echo
echo "=== Testes concluídos ==="
