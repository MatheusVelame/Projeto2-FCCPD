from flask import Flask, jsonify

app = Flask(__name__)

USERS = {
    "u001": {"name": "Alice Silva", "status": "Ativo", "created_at": "2023-01-15T10:00:00Z"},
    "u002": {"name": "Bruno Costa", "status": "Inativo", "created_at": "2023-03-20T14:30:00Z"}
}

@app.route('/users')
def list_users():

    return jsonify(USERS)

@app.route('/users/<user_id>')
def get_user(user_id):
    user = USERS.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)