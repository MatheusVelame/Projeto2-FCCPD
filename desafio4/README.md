# 🌐 Desafio 4: Microsserviços Independentes

## 🎯 Objetivo

O objetivo deste desafio é criar dois microsserviços distintos e independentes que se comunicam diretamente via **requisições HTTP**, demonstrando o fluxo de dados em uma arquitetura de microsserviços.

---

## 💡 Arquitetura, Fluxo e Decisões Técnicas

A solução consiste em dois microsserviços isolados, cada um executado em seu próprio container Docker e conectados por uma rede customizada.

| Componente | Nome do Container | Função | Endpoint Exposto |
|----------|-------------------|--------|-------------------|
| **Microserviço A (Users)** | `users` | Fornece dados de usuários estáticos em JSON. | Interno: `http://users:5000/users` |
| **Microserviço B (Consumer)** | `consumer` | Consome o MS A, processa os dados e exibe informações combinadas. | Externo: `http://localhost:8001` |

### 🔁 Comunicação e Fluxo de Dados

1. **Rede Customizada:**  
   A rede **`rede_microservicos4`** permite que os serviços se comuniquem usando nomes DNS (ex.: `users`).

2. **Requisição HTTP:**  
   O MS B acessa internamente:  
   `http://users:5000/users`

3. **Processamento:**  
   O MS B recebe o JSON, calcula os "dias de criação" de cada usuário e devolve uma resposta formatada, como:  
   *"Usuário Alice Silva está Ativo. Conta criada há X dias."*

### 🔒 Isolamento dos Serviços

Cada microsserviço contém:

- Seu próprio diretório  
- Um `Dockerfile`  
- Um arquivo `requirements.txt`  
- Um arquivo `.py` contendo apenas sua lógica

Garantindo total desacoplamento entre eles.

---

## 📂 Estrutura de Arquivos

```
desafio4/
├── microservice_A/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── users_service.py          # Microsserviço A (fornece dados)
│
├── microservice_B/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── consumer_service.py       # Microsserviço B (consome e exibe dados combinados)
│
└── run_desafio4.sh               # Script de automação para build e execução
```

---

### ⚙️ Instruções de Execução Passo a Passo

#### Pré-requisitos
Certifique-se de que o **Docker Engine** está instalado e em execução.

---

### Opção A: Linux / macOS (Usando Script Bash)

O script `run_desafio4.sh` automatiza todo o processo de inicialização.

1.  Navegue até o diretório do desafio:
    ```bash
    cd desafio4
    ```

2.  Dê permissão e execute o script de inicialização:
    ```bash
    chmod +x run_desafio4.sh
    ./run_desafio4.sh
    ```

---

### Opção B: Windows / PowerShell (Comandos Manuais)

Para usuários de Windows, siga os comandos manualmente no terminal:

1.  **Limpeza e Criação da Rede:**
    Remova containers e rede antigos e crie a rede customizada:
    ```bash
    # Limpa containers e rede
    docker rm -f users consumer
    docker network rm rede_microservicos4
    # Cria a rede customizada
    docker network create rede_microservicos4
    ```

2.  **Construção das Imagens:**
    ```bash
    docker build -t users-service-img ./microservice_A
    docker build -t consumer-service-img ./microservice_B
    ```

3.  **Execução dos Containers:**
    Inicie o MS A (`users`) e, em seguida, o MS B (`consumer`), conectados à rede:
    ```bash
    # Inicia Microserviço A (Users)
    docker run -d --name users --network rede_microservicos4 -p 5000:5000 users-service-img
    # Inicia Microserviço B (Consumer)
    docker run -d --name consumer --network rede_microservicos4 -p 8001:5001 consumer-service-img
    ```

---

#### 3. Demonstração e Comprovação

Acesse o **Microserviço B (Consumer)**, que acionará automaticamente a comunicação com o MS A:

1.  **Acessar o Microserviço B:**
    ```bash
    curl http://localhost:8001
    # ou acesse http://localhost:8001 no navegador
    ```
    **Comprovação:** A saída deve exibir a lista de usuários formatada e processada pelo MS B, confirmando a comunicação bem-sucedida.

2.  **Verificar Logs do MS A:**
    Confirme que o MS A recebeu a requisição do MS B:
    ```bash
    docker logs users
    ```

#### 4. Limpeza

Para interromper e remover todos os recursos criados:

```bash
docker rm -f users consumer
docker network rm rede_microservicos4