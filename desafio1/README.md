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

## ⚙️ Instruções de Execução Passo a Passo

O script `run.sh` automatiza toda a execução.

### 1. Pré-requisitos

- Docker Engine instalado.

### 2. Execução

```bash
cd desafio1
chmod +x run.sh
./run.sh
```
