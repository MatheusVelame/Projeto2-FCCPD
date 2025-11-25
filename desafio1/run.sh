
NETWORK_NAME="rede_desafio1"
SERVER_NAME="servidor"
CLIENT_NAME="cliente"

# 1. Limpeza de containers antigos
echo "▶️ Removendo containers e rede antigos (se existirem)..."
docker rm -f $SERVER_NAME $CLIENT_NAME 2>/dev/null
docker network rm $NETWORK_NAME 2>/dev/null

# 2. Criação da Rede Docker Customizada (Requisito: 5 pts)
echo "▶️ Criando rede Docker nomeada: $NETWORK_NAME"
docker network create $NETWORK_NAME

# 3. Construção das Imagens
echo "▶️ Construindo imagem do Servidor..."
docker build -t server-image -f Dockerfile.server .

echo "▶️ Construindo imagem do Cliente..."
docker build -t client-image -f Dockerfile.client .

# 4. Execução do Servidor (conectado à rede)
echo "▶️ Iniciando Servidor ($SERVER_NAME) na rede $NETWORK_NAME..."
# O --network-alias permite que o cliente use o nome 'servidor'
docker run -d --name $SERVER_NAME --network $NETWORK_NAME -p 8080:8080 server-image

# 5. Execução do Cliente (conectado à rede)
echo "▶️ Iniciando Cliente ($CLIENT_NAME) na rede $NETWORK_NAME (requisições periódicas)..."
docker run -d --name $CLIENT_NAME --network $NETWORK_NAME client-image

# 6. Demonstração e Logs (Requisito: Demonstração da comunicação)
echo "✅ SETUP COMPLETO. A comunicação está ocorrendo."
echo "--------------------------------------------------------"
echo "Para verificar a comunicação (logs do cliente):"
echo "docker logs -f $CLIENT_NAME"
echo ""
echo "Para verificar as requisições recebidas (logs do servidor):"
echo "docker logs -f $SERVER_NAME"
echo "--------------------------------------------------------"