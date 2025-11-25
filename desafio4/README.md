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

## ⚙️ Instruções de Execução Passo a Passo

O script `run_desafio4.sh` automatiza todo o processo.

### 1. Pré-requisitos

- Docker Engine instalado e rodando

### 2. Execução

1. Entre no diretório:
   ```bash
   cd desafio4
   ```

2. Dê permissão e execute o script:
   ```bash
   chmod +x run_desafio4.sh
   ./run_desafio4.sh
   ```

O script irá:

- Remover containers e redes antigas  
- Criar a rede **`rede_microservicos4`**  
- Construir as imagens dos dois microsserviços  
- Subir os containers:  
  - `users` (porta externa 5000)  
  - `consumer` (porta externa 8001)

---

## 🧪 Demonstração e Comprovação

### 1. Testar o Microserviço B (Consumer)

Acesse:

```bash
curl http://localhost:8001
# ou abra http://localhost:8001 no navegador
```

📌 **Resultado esperado:**

- Status da conexão: `OK`
- Lista de usuários formatada com dias de criação calculados

Exemplo:

```
Usuário Alice Silva está Ativo. Conta criada há 123 dias.
Usuário João Pereira está Inativo. Conta criada há 400 dias.
```

### 2. Verificar logs (opcional)

Para ver se o MS A recebeu requisições:

```bash
docker logs users
```

---

## 🧹 Limpeza

Para encerrar e remover tudo:

```bash
docker rm -f users consumer
docker network rm rede_microservicos4
```

---
