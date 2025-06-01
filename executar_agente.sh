#!/bin/bash

# Script para executar o agente virtual
# Detecta automaticamente se está sendo executado dentro ou fora do Docker

# Verifica se o arquivo /.dockerenv existe (indica que está dentro de um contêiner Docker)
if [ -f /.dockerenv ]; then
    echo "Executando agente virtual dentro do contêiner Docker..."
    python agente_virtual.py
else
    echo "Executando agente virtual através do contêiner Docker..."
    docker-compose exec web python agente_virtual.py
fi
