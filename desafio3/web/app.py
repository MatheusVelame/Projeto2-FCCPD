import time
import os
import redis
import psycopg2
from flask import Flask

# -----------------------------------------------------
# Configuração de Conexão
# -----------------------------------------------------

cache = redis.Redis(host='cache', port=6379) 
conn = None
cursor = None

def init_db():
    global conn, cursor
    MAX_RETRIES = 10
    RETRY_DELAY = 2  

    for attempt in range(MAX_RETRIES):
        try:
            # 1. Tenta conectar ao DB usando variáveis de ambiente do docker-compose
            conn = psycopg2.connect(
                host='db',
                database=os.environ.get('POSTGRES_DB'),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD')
            )
            cursor = conn.cursor()
            
            # 2. Cria a tabela de log se não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS access_log (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP,
                    hit_count INT
                );
            """)
            conn.commit()
            print("Conexão e inicialização do DB bem-sucedidas!")
            return 
        
        except psycopg2.OperationalError as e:
            
            print(f"Tentativa {attempt + 1}/{MAX_RETRIES}: Conexão ao DB falhou. Erro: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                print("Máximo de tentativas de conexão atingido. O DB pode não estar pronto.")
                conn = None
                cursor = None
                return


init_db()

app = Flask(__name__)

# -----------------------------------------------------
# Funções de Lógica da Aplicação
# -----------------------------------------------------

def get_hit_count():
    retries = 5
    while True:
        try:
            # Tenta incrementar o contador no Redis
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                # Se falhar após 5 tentativas, lança exceção
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    try:
        count = get_hit_count()
        
        db_status = "Falhou"
        # Verifica se a conexão global 'conn' existe antes de tentar logar
        if conn and cursor:
            try:
                cursor.execute("INSERT INTO access_log (timestamp, hit_count) VALUES (NOW(), %s)", (count,))
                conn.commit()
                db_status = "OK"
            except Exception as e:
                db_status = f"Erro ao inserir: {e}"
        else:
             db_status = "Não Conectado"
        
        return f'<h1>Contador de Acessos (CACHE): {count}</h1>' \
               f'<p>Status da Conexão:</p>' \
               f'<ul><li>Cache (Redis): OK</li><li>DB (PostgreSQL): {db_status}</li></ul>'

    except Exception as e:
        return f"Erro Crítico: Serviço indisponível. Detalhe: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)