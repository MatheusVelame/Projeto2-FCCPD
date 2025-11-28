# 🚀 Desafio 3: Docker Compose Orquestrando Serviços

## 🎯 Objetivo

O objetivo deste desafio é utilizar o **Docker Compose** para orquestrar múltiplos serviços dependentes, simulando uma arquitetura de aplicação em três camadas (Web, Cache e Banco de Dados).

---

## 💡 Arquitetura e Decisões Técnicas

A solução consiste em três serviços conectados por uma rede interna gerenciada pelo Docker Compose, atendendo ao requisito de orquestrar múltiplos serviços dependentes.

### 🔧 Visão Geral da Arquitetura

1. **`web` (Frontend/Aplicação)**  
   - **Função:** Conta e exibe o número de acessos e registra essa contagem no banco.  
   - **Tecnologia:** Aplicação **Flask** construída via `Dockerfile`.  
   - **Comunicação:** Conecta com `cache` (Redis) e `db` (Postgres).

2. **`cache` (Cache de Acesso)**  
   - **Função:** Armazena o contador de *hits* (acessos).  
   - **Tecnologia:** Imagem oficial do **Redis** (`redis:latest`).

3. **`db` (Banco de Dados)**  
   - **Função:** Persistência dos logs de acesso.  
   - **Tecnologia:** Imagem oficial do **PostgreSQL** (`postgres:16-alpine`).

### 🧩 Orquestração via `docker-compose.yml`

- **`depends_on`:** O serviço `web` depende de `db` e `cache`, garantindo sua inicialização primeiro.  
- **Rede Interna:** Automática, nomeada **`rede-desafio3`**, permitindo comunicação por nome de serviço.  
- **Persistência:** O banco usa o volume nomeado **`db-data`**.  
- **Variáveis de Ambiente:** Credenciais do banco configuradas no `db` e replicadas no `web`.

---

## 📂 Estrutura de Arquivos

```
desafio3/
├── docker-compose.yml        # Orquestração dos serviços
└── web/
    ├── Dockerfile
    ├── app.py                # Aplicação Flask com lógica de cache e banco
    └── requirements.txt
```

---

## ⚙️ Instruções de Execução Passo a Passo

### 1. Pré-requisitos

- Docker instalado  
- Docker Compose disponível

### 2. Execução

1. Acesse o diretório:
   ```bash
   cd desafio3
   ```

2. Limpeza Total:
   ```bash
   docker-compose down -v
   ```

3. Suba os serviços em modo *detached*:
   ```bash
   docker-compose up --build -d
   ```
   O Compose inicia primeiro `db` e `cache`, depois o serviço `web`.

---

## 🧪 Teste e Validação da Comunicação

### 1. Acessar a Aplicação Web

A aplicação está mapeada na porta **80**:

```bash
curl http://localhost
# ou acesse http://localhost no navegador
```

Cada acesso deve:

- Incrementar o contador usando **Redis**
- Exibir o número de *hits*
- Registrar o log no **PostgreSQL**

### 2. Verificar Logs do Serviço Web

```bash
docker-compose logs -f web
```

Os logs devem mostrar:

- Conexão bem-sucedida com Redis  
- Conexão bem-sucedida com o PostgreSQL  
- Inserção de registros a cada acesso

---

## 🧹 Limpeza

Para remover containers, rede e volume:

```bash
docker-compose down -v
```

---
