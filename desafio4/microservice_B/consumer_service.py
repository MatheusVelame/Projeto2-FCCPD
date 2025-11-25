from flask import Flask, jsonify, render_template_string
import requests
import os
from datetime import datetime

app = Flask(__name__)

USERS_SERVICE_URL = "http://users:5000/users"

def fetch_and_process_users():
    try:
        # 1. Faz a requisição HTTP para o Serviço A
        response = requests.get(USERS_SERVICE_URL, timeout=5)
        response.raise_for_status()
        
        users_data = response.json()
        processed_users = []
        
        # 2. Processa e combina os dados
        for user_id, user_info in users_data.items():
            created_at = datetime.strptime(user_info["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            time_ago = (datetime.utcnow() - created_at).days
            
            processed_users.append({
                "id": user_id,
                "summary": f"Usuário **{user_info['name']}** está **{user_info['status']}**",
                "detail": f"Conta criada há {time_ago} dias ({created_at.strftime('%Y-%m-%d')})."
            })
            
        return processed_users, "OK"
        
    except requests.exceptions.RequestException as e:
        return [], f"Erro ao consumir o Microserviço A: {e}"

@app.route('/')
def combined_view():
    users, status = fetch_and_process_users()
    
    html_output = f"<h1>Status da Conexão com Microserviço A: {status}</h1>"
    
    if users:
        html_output += "<h2>Detalhes dos Usuários (Dados Combinados):</h2><ul>"
        for user in users:
            html_output += f"<li>**{user['summary']}**. {user['detail']}</li>"
        html_output += "</ul>"
    
    return render_template_string(html_output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)