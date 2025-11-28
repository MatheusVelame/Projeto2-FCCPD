# 🛡️ Desafio 5: Microsserviços com API Gateway

## 🎯 Objetivo

O objetivo deste desafio é implementar uma arquitetura completa de microsserviços, utilizando um **API Gateway** como ponto único de entrada para centralizar e rotear o acesso a dois serviços de *backend* independentes.

---

## 💡 Arquitetura, Fluxo e Decisões Técnicas

A solução é baseada na orquestração de três serviços utilizando **Docker Compose**: dois microsserviços de dados e um API Gateway responsável por rotear as solicitações.

### 🔧 Componentes da Arquitetura

| Serviço | Função | Tecnologia | Porta Interna |
|--------|--------|------------|----------------|
| **Users Service (`users-service`)** | Fornece dados de usuários. | Flask (Python) | `5001` |
| **Orders Service (`orders-service`)** | Fornece dados de pedidos. | Flask (Python) | `5002` |
| **API Gateway (`gateway`)** | Ponto único de entrada. Roteia requisições para ambos os serviços. | Flask (Python) + `requests` | `5000` |

---

## 🔁 Funcionamento do API Gateway

O arquivo **`gateway_app.py`** funciona como um *reverse proxy*, expondo endpoints externos e encaminhando-os internamente:

- **GET `/users`** → Encaminha para:  
  `http://users-service:5001/api/v1/users`

- **GET `/orders`** → Encaminha para:  
  `http://orders-service:5002/api/v1/orders`

Ele também:
- Retorna erros caso um serviço esteja indisponível.
- Centraliza logs de roteamento.
- Evita que os microsserviços exponham portas externas diretamente.

---

## 🐳 Orquestração com Docker Compose

O arquivo `docker-compose.yml` garante:

1. **Build de cada serviço** através de seu próprio `Dockerfile`.
2. **Isolamento e rede interna** chamada `microservice-net`.
3. **Roteamento pelo Gateway** usando nomes de container.
4. **Porta única de entrada**: somente o serviço `gateway` mapeia para o host:
   ```
   8000 -> 5000
   ```
5. **depends_on** assegura a ordem de inicialização.

---

## 📂 Estrutura de Arquivos

```
desafio5/
├── docker-compose.yml
│
├── gateway/
│   ├── Dockerfile
│   ├── gateway_app.py          # Implementa o proxy/roteamento
│   └── requirements.txt
│
├── orders_service/
│   ├── Dockerfile
│   ├── orders_api.py           # Microsserviço 2 (Pedidos)
│   └── requirements.txt
│
└── users_service/
    ├── Dockerfile
    ├── users_api.py            # Microsserviço 1 (Usuários)
    └── requirements.txt
```

---

## ⚙️ Instruções de Execução Passo a Passo

### 1. Pré-requisitos

- Docker instalado  
- Docker Compose disponível

---

### 2. Execução

1. Entre no diretório:
   ```bash
   cd desafio5
   ```

2. Limpeza Total:
   ```bash
   docker-compose down -v
   ```

3. Suba toda a arquitetura:
   ```bash
   docker-compose up --build -d
   ```

O Compose irá:
- Criar a rede `microservice-net`
- Construir as imagens
- Iniciar os microsserviços
- Expor apenas o Gateway

---

## 🧪 Teste e Validação

O acesso é sempre feito pela porta **8000** → Gateway.

### 1. Testar o Microsserviço de Usuários
```bash
curl http://localhost:8000/users
```
**Resultado esperado:** JSON com a lista de usuários.

---

### 2. Testar o Microsserviço de Pedidos
```bash
curl http://localhost:8000/orders
```
**Resultado esperado:** JSON com a lista de pedidos.

---

### 3. Verificar Logs do Gateway
```bash
docker-compose logs -f gateway
```

Os logs devem mostrar:

```
Gateway: Roteando para /users
Gateway: Roteando para /orders
```

Isso comprova o funcionamento do roteamento.

---

## 🧹 Limpeza

Para remover containers, rede e imagens construídas:

```bash
docker-compose down
```

---
