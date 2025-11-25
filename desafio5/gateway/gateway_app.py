from flask import Flask, jsonify, make_response
import requests
import os

app = Flask(__name__)

# Endereços internos (nomes de serviço do docker-compose)
USERS_SERVICE_URL = "http://users-service:5001/api/v1/users"
ORDERS_SERVICE_URL = "http://orders-service:5002/api/v1/orders"

def proxy_request(url):
    """Encaminha a requisição GET para o microsserviço."""
    try:
        response = requests.get(url, timeout=5)
        # Retorna a resposta (JSON e código de status) do microsserviço
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": f"Serviço indisponível: {url}", "detail": str(e)}, 503

@app.route('/users', methods=['GET'])
def get_users_proxy():
    # Gateway expõe /users e roteia para o users-service
    print("Gateway: Roteando para /users")
    data, status = proxy_request(USERS_SERVICE_URL)
    return make_response(jsonify(data), status)

@app.route('/orders', methods=['GET'])
def get_orders_proxy():
    # Gateway expõe /orders e roteia para o orders-service
    print("Gateway: Roteando para /orders")
    data, status = proxy_request(ORDERS_SERVICE_URL)
    return make_response(jsonify(data), status)

@app.route('/')
def home():
    return "API Gateway Ativo. Use /users ou /orders."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)