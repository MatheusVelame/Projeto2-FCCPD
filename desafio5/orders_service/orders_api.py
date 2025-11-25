from flask import Flask, jsonify

app = Flask(__name__)

ORDERS = {
    "o101": {"user_id": "u001", "product": "Laptop", "status": "Entregue"},
    "o102": {"user_id": "u002", "product": "Smartphone", "status": "Pendente"},
    "o103": {"user_id": "u001", "product": "Mouse", "status": "Em Trânsito"}
}

@app.route('/api/v1/orders', methods=['GET'])
def list_orders():
    print("MS2: Requisição de pedidos recebida.")
    return jsonify(ORDERS), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)