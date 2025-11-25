from flask import Flask, jsonify

app = Flask(__name__)

USERS = {
    "u001": {"name": "Alice Silva", "email": "alice@exemplo.com"},
    "u002": {"name": "Bruno Costa", "email": "bruno@exemplo.com"}
}

@app.route('/api/v1/users', methods=['GET'])
def list_users():
    print("MS1: Requisição de usuários recebida.")
    return jsonify(USERS), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)