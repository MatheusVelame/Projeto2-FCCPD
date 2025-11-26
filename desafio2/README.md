# 💾 Desafio 2: Volumes e Persistência

## 🎯 Objetivo

O objetivo deste desafio é demonstrar a **persistência de dados** em containers Docker usando **volumes nomeados**. O teste comprova que os dados armazenados por um container de banco de dados (PostgreSQL) permanecem intactos, mesmo após o container ser completamente removido e recriado.

---

## 💡 Arquitetura e Decisões Técnicas

A solução utiliza um container de banco de dados **PostgreSQL** e um volume Docker nomeado para mapear o diretório de dados do banco para fora do ciclo de vida do container.

| Componente | Função | Implementação | Decisão Técnica |
|-----------|--------|----------------|------------------|
| **Banco de Dados** | Armazenar dados para o teste de persistência. | Imagem `postgres:16-alpine`. | Escolha do PostgreSQL pela robustez e popularidade. Uso da tag `alpine` para imagens menores e rápidas. |
| **Volume Docker** | Garantir persistência dos dados. | Volume nomeado **`dados_postgres_desafio2`**. | Volumes nomeados são a forma recomendada pelo Docker para persistência. Montado em `/var/lib/postgresql/data`. |
| **Inicialização** | Criar tabela e dado inicial. | Arquivo **`init.sql`**. | Montado em `/docker-entrypoint-initdb.d/` para inicializar o banco automaticamente. |

---

## 📂 Estrutura de Arquivos

```
desafio2/
├── init.sql        # Script SQL para criar tabela e inserir dado inicial
└── run_test.sh     # Script de automação que executa o teste de persistência
```

---

### ⚙️ Instruções de Execução Passo a Passo

#### Pré-requisitos
Certifique-se de que o **Docker Engine** está instalado e em execução.

---

### Opção A: Linux / macOS (Usando Script Bash)

O script `run_test.sh` automatiza todo o teste em duas fases (criação/remoção e recriação/comprovação).

1.  Navegue até o diretório do desafio:
    ```bash
    cd desafio2
    ```

2.  Dê permissão e execute o script de teste:
    ```bash
    chmod +x run_test.sh
    ./run_test.sh
    ```
    O script exibirá automaticamente a comprovação final.

---

### Opção B: Windows / PowerShell (Teste Manual)

O teste de persistência deve ser realizado manualmente em duas fases:

#### FASE 1: Inicialização e Inserção do Dado

1.  **Crie o volume nomeado:**
    ```bash
    docker volume create dados_postgres_desafio2
    ```

2.  **Inicie o Container A (`db_persistente`):**
    Este container usa o volume e insere o dado via `init.sql`:
    ```bash
    docker run --rm -d `
        --name db_persistente `
        -e POSTGRES_USER=admin `
        -e POSTGRES_PASSWORD=secret `
        -e POSTGRES_DB=mydb `
        -v dados_postgres_desafio2:/var/lib/postgresql/data `
        -v ${PWD}/init.sql:/docker-entrypoint-initdb.d/init.sql `
        postgres:16-alpine
    # Note: O uso de ` e ${PWD} é específico do PowerShell. Use `%CD%` no CMD.
    ```
    *Aguarde 5 segundos para o banco iniciar.*

3.  **Verifique o dado inserido no Container A:**
    ```bash
    docker exec db_persistente psql -U admin -d mydb -c "SELECT * FROM registros_teste;"
    ```

4.  **Remova o Container A (Mantendo o Volume):**
    ```bash
    docker stop db_persistente
    ```

#### FASE 2: Recriação do Container e Comprovação

5.  **Inicie o Container B (`db_leitor`) usando o MESMO VOLUME:**
    Este container NÃO executa o `init.sql` porque o volume já tem dados:
    ```bash
    docker run --rm -d `
        --name db_leitor `
        -e POSTGRES_USER=admin `
        -e POSTGRES_PASSWORD=secret `
        -v dados_postgres_desafio2:/var/lib/postgresql/data `
        postgres:16-alpine
    ```
    *Aguarde 5 segundos para o novo banco iniciar.*

6.  **Verifique se o dado PERSISTIU no Container B:**
    ```bash
    docker exec db_leitor psql -U admin -d mydb -c "SELECT * FROM registros_teste;"
    ```
    **Comprovação:** A saída deve mostrar o dado inserido na Fase 1, provando que ele residiu no volume nomeado e persistiu após a remoção do container original.

---

#### Limpeza

Para remover o volume de persistência e resetar o ambiente:

```bash
# O stop/rm dos containers já é feito nos passos de teste
docker volume rm dados_postgres_desafio2