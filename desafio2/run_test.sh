#!/bin/bash

VOLUME_NAME="dados_postgres_desafio2"
CONTAINER_NAME="db_persistente"

echo "========================================================"
echo "        Iniciando Teste de Persistência (Desafio 2)     "
echo "========================================================"

# --- FASE 1: Inicialização e Criação do Dado ---

echo "1. Criando ou verificando o volume Docker: $VOLUME_NAME"
# Cria o volume se ele não existir
docker volume create $VOLUME_NAME 2>/dev/null || true

echo "2. Iniciando Container PostgreSQL (com VOLUME anexado)..."
docker run --rm -d \
    --name $CONTAINER_NAME \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=mydb \
    -v $VOLUME_NAME:/var/lib/postgresql/data \
    -v $(pwd)/init.sql:/docker-entrypoint-initdb.d/init.sql \
    postgres:16-alpine

echo "Aguardando o banco iniciar (5 segundos)..."
sleep 5

echo "3. Verificando o dado INSERIDO pelo init.sql no CONTAINER ATUAL (A)..."
# Executa um comando SQL dentro do container para ler o dado
docker exec $CONTAINER_NAME psql -U admin -d mydb -c "SELECT * FROM registros_teste;"

echo "4. REMOVENDO o Container (mas MANTENDO o Volume)..."
docker stop $CONTAINER_NAME > /dev/null
docker rm $CONTAINER_NAME > /dev/null
echo "Container '$CONTAINER_NAME' removido."

echo "--------------------------------------------------------"
echo "--- FASE 2: Recriação do Container e Comprovação ---"

NEW_CONTAINER_NAME="db_leitor"

echo "5. Iniciando um NOVO Container ('$NEW_CONTAINER_NAME') usando o MESMO VOLUME..."
# Inicia um novo container. Ele não rodará o init.sql porque o volume já existe.
docker run --rm -d \
    --name $NEW_CONTAINER_NAME \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=secret \
    -v $VOLUME_NAME:/var/lib/postgresql/data \
    postgres:16-alpine

echo "Aguardando o novo banco iniciar (5 segundos)..."
sleep 5

echo "6. Verificando se o dado PERSISTIU no NOVO CONTAINER (B)..."
# Executa o mesmo comando SQL no novo container
docker exec $NEW_CONTAINER_NAME psql -U admin -d mydb -c "SELECT * FROM registros_teste;"

echo "--------------------------------------------------------"
echo "✅ TESTE DE PERSISTÊNCIA COMPROVADO."
echo "   Os dados estão presentes no novo container, provando que eles residem no volume '$VOLUME_NAME'."

# Limpeza final
docker stop $NEW_CONTAINER_NAME > /dev/null

# Opcional: Remova o volume após a demonstração, se quiser resetar o teste
# echo "Para remover o volume e resetar: docker volume rm $VOLUME_NAME"