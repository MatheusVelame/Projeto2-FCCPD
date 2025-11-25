#!/bin/bash

NETWORK_NAME="rede_microservicos4"
SERVER_A_NAME="users"
SERVER_B_NAME="consumer"

echo "========================================================="
echo "        Iniciando Microsserviços (Desafio 4)             "
echo "========================================================="

# Limpeza
echo "▶️ Removendo containers e rede antigos (se existirem)..."
docker rm -f $SERVER_A_NAME $SERVER_B_NAME 2>/dev/null
docker network rm $NETWORK_NAME 2>/dev/null

# 1. Criação da Rede Docker Customizada
echo "▶️ Criando rede Docker nomeada: $NETWORK_NAME"
docker network create $NETWORK_NAME

# 2. Construção das Imagens
echo "▶️ Construindo imagem do Microserviço A (Users)..."
docker build -t users-service-img ./microservice_A

echo "▶️ Construindo imagem do Microserviço B (Consumer)..."
docker build -t consumer-service-img ./microservice_B

# 3. Execução do Microsserviço A
echo "▶️ Iniciando Microserviço A ($SERVER_A_NAME) na porta 5000..."
docker run -d --name $SERVER_A_NAME --network $NETWORK_NAME \
    -p 5000:5000 users-service-img

# 4. Execução do Microsserviço B
echo "▶️ Iniciando Microserviço B ($SERVER_B_NAME) na porta 5001..."
docker run -d --name $SERVER_B_NAME --network $NETWORK_NAME \
    -p 8001:5001 consumer-service-img

echo "--------------------------------------------------------"
echo "✅ SETUP COMPLETO."
echo "   Microserviço A: http://localhost:5000/users"
echo "   Microserviço B (Consumer): http://localhost:8001"
echo ""
echo "▶️ Para testar, acesse o Microserviço B (Consumer) no seu navegador ou use curl:"
echo "   curl http://localhost:8001"
echo "--------------------------------------------------------"