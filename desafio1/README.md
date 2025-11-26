# 🌐 Desafio 1: Containers em Rede

## 🎯 Objetivo

O objetivo deste desafio é criar e demonstrar a comunicação funcional entre dois containers Docker distintos que operam dentro de uma **rede Docker customizada e nomeada**.

## 💡 Arquitetura e Decisões Técnicas

A solução implementa o padrão básico de comunicação **Cliente-Servidor**, isolando as funções em dois containers independentes, mas conectados.

| Componente | Função | Implementação | Decisão Técnica |
| --- | --- | --- | --- |
| **Servidor (`servidor`)** | Container que expõe um serviço HTTP na porta `8080`. | Aplicação **Flask** em Python. | Imagem `python:3.9-slim` pela leveza e execução direta do servidor Flask. |
| **Cliente (`cliente`)** | Container que realiza requisições HTTP periódicas. | Script Shell (`client.sh`) com `curl` em *loop*. | Imagem `alpine/curl:latest` para ser extremamente leve e incluir apenas o utilitário `curl`. |

### Comunicação em Rede

1. **Criação da Rede:** É utilizada uma rede customizada do tipo *bridge* chamada **`rede_desafio1`**.  
2. **Resolução de Nomes (DNS):** Ambos os containers são conectados à `rede_desafio1`. O cliente acessa o servidor usando o nome do container (`http://servidor:8080`), provando que a resolução de nomes interna do Docker está funcionando.

## 📂 Estrutura de Arquivos

```bash
desafio1/
├── Dockerfile.client        # Imagem do container cliente (curl)
├── Dockerfile.server        # Imagem do servidor Flask
├── client.sh                # Loop de requisições curl
├── requirements.txt         # Dependências do Flask
├── run.sh                   # Script principal de build e execução
└── server.py                # Servidor Flask na porta 8080
```

### ⚙️ Instruções de Execução Passo a Passo

#### Pré-requisitos
Certifique-se de ter o **Docker Engine** instalado e em execução.

---

### Opção A: Linux / macOS (Usando Script Bash)

O script `run.sh` automatiza todas as etapas de inicialização e limpeza.

1.  Navegue até o diretório do desafio:
    ```bash
    cd desafio1
    ```

2.  Dê permissão e execute o script de inicialização:
    ```bash
    chmod +x run.sh
    ./run.sh
    ```

---

### Opção B: Windows / PowerShell (Comandos Manuais)

Para usuários de Windows, siga os comandos manualmente no terminal (PowerShell ou CMD):

1.  **Limpeza e Criação da Rede:**
    Remova containers e rede antigos (se existirem) e crie a rede customizada:
    ```bash
    # Limpa containers antigos
    docker rm -f servidor cliente
    # Limpa rede antiga
    docker network rm rede_desafio1
    # Cria a rede customizada (Requisito)
    docker network create rede_desafio1
    ```

2.  **Construção das Imagens:**
    ```bash
    docker build -t server-image -f Dockerfile.server .
    docker build -t client-image -f Dockerfile.client .
    ```

3.  **Execução dos Containers:**
    Inicie o servidor (mapeando a porta 8080) e o cliente (conectados à rede):
    ```bash
    docker run -d --name servidor --network rede_desafio1 -p 8080:8080 server-image
    docker run -d --name cliente --network rede_desafio1 client-image
    ```

---

#### Demonstração e Comprovação (Logs)

Para demonstrar a comunicação e a troca de mensagens, observe os logs dos containers:

| Ação | Comando | Propósito |
| :--- | :--- | :--- |
| **Verificar o lado Cliente** | `docker logs -f cliente` | Mostrará o resultado de cada requisição `curl` a cada 5 segundos, comprovando a comunicação funcional. |
| **Verificar o lado Servidor** | `docker logs -f servidor` | Mostrará os logs HTTP do Flask, indicando o recebimento periódico das requisições do container `cliente`. |

#### Limpeza

Para interromper e remover todos os recursos criados:

```bash
docker rm -f servidor cliente
docker network rm rede_desafio1