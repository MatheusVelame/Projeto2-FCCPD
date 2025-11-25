# 🚀 Projeto 2: Docker e Arquitetura de Microsserviços

Este repositório contém a solução para o Projeto 2, que abrange uma série de desafios práticos focados na orquestração de containers com **Docker** e **Docker Compose**, e na implementação de uma arquitetura de **Microsserviços** (MS) com comunicação HTTP e API Gateway.

O projeto está dividido em cinco desafios, cada um em sua própria pasta, conforme a estrutura de entrega.

---

## 🏗️ Estrutura do Repositório

O repositório está organizado para isolar as soluções de cada desafio:

| Pasta | Descrição | Tópicos Principais |
| :--- | :--- | :--- |
| **`desafio1/`** | Containers em Rede | Criação de rede customizada e comunicação entre dois containers. |
| **`desafio2/`** | Volumes e Persistência | Uso de volumes nomeados para garantir a persistência de dados de um banco de dados (PostgreSQL). |
| **`desafio3/`** | Docker Compose Orquestrando Serviços | Orquestração de uma aplicação multicamadas (Web, DB, Cache) com dependências e rede interna. |
| **`desafio4/`** | Microsserviços Independentes | Comunicação direta via HTTP entre dois microsserviços isolados. |
| **`desafio5/`** | Microsserviços com API Gateway | Implementação de um API Gateway para centralizar o acesso a dois microsserviços (Usuários e Pedidos). |

---

## 🛠️ Tecnologias Utilizadas

* **Orquestração/Containers:** Docker, Docker Compose.
* **Serviços Web:** Python (Flask).
* **Bancos de Dados/Cache:** PostgreSQL, Redis.
* **Comunicação:** HTTP/REST (Módulos `requests` em Python e `curl` em Alpine).

---

## 🏃 Como Executar os Desafios

Para executar e testar as soluções, siga as instruções específicas dentro de cada pasta de desafio.

**Pré-requisitos:**

* Docker Engine instalado e em execução.
* Docker Compose instalado.

### Instruções Gerais

1.  **Navegue até a pasta do desafio desejado:**
    ```bash
    cd desafioX
    ```

2.  **Execute o script de inicialização:**
    Cada desafio possui um script ou um arquivo `docker-compose.yml` para simplificar a execução.

    * **Desafios 1, 2, 4:** Use o script shell fornecido (`run.sh` ou `run_test.sh`):
        ```bash
        ./run_test.sh
        # Ou:
        ./run.sh
        ```
    * **Desafios 3 e 5 (Docker Compose):** Utilize o Docker Compose:
        ```bash
        docker-compose up --build -d
        ```

3.  **Para finalizar e limpar os recursos (containers, redes):**
    * Para scripts shell (Desafios 1, 2, 4): Geralmente, os scripts já incluem limpeza automática ou você pode usar `docker rm -f <container_name>`.
    * Para Docker Compose (Desafios 3, 5):
        ```bash
        docker-compose down -v # O '-v' remove volumes nomeados se eles existirem.
        ```

---

## 📝 Documentação Específica

Para a documentação completa, detalhes da arquitetura, decisões técnicas e comprovação dos resultados, consulte o arquivo **README.md** dentro de cada pasta de desafio (`/desafio1/README.md`, `/desafio2/README.md`, etc.), conforme exigido nas orientações gerais do projeto.