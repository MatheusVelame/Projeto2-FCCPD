SERVER_URL="http://servidor:8080" 

echo "Iniciando o cliente. Requisitando periodicamente o servidor em $SERVER_URL..."
while true; do
  echo "--- $(date) ---"
  curl -s $SERVER_URL
  sleep 5
done