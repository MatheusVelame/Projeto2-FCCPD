from flask import Flask
import os
import datetime

app = Flask(__name__)
PORT = 8080
HOSTNAME = os.environ.get('HOSTNAME', 'Servidor Desconhecido')

@app.route('/')
def hello_world():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"Olá do Servidor: {HOSTNAME} - Hora da Requisição: {now}\n"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)