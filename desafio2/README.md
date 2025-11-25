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

## ⚙️ Instruções de Execução Passo a Passo

O script `run_test.sh` executa o teste completo em duas fases, demonstrando a persistência dos dados.

### 1. Pré-requisitos

- Docker Engine instalado e em execução.

### 2. Execução

1. Acesse o diretório:
   ```bash
   cd desafio2
   ```

2. Dê permissão e execute:
   ```bash
   chmod +x run_test.sh
   ./run_test.sh
   ```

---

## 🧪 Demonstração e Comprovação (Logs/Resultados)

O script executa duas fases:

| Fase | Ações | Comprovação |
|------|--------|--------------|
| **FASE 1: Criação e Remoção** | 1. Cria volume. 2. Inicia **Container A** (`db_persistente`). 3. Verifica dado criado pelo `init.sql`. 4. Para e remove container. | Confirma que o dado foi criado e salvo no volume. |
| **FASE 2: Persistência Comprovada** | 5. Inicia **Container B** (`db_leitor`) usando o mesmo volume. 6. Verifica o dado. | O mesmo registro aparece no novo container → PROVA de persistência. |

---

## 📌 Saída Esperada na Fase 2

O container B deve mostrar o registro original:

```
 id | mensagem                              | data_criacao
----+----------------------------------------+------------------------------
  1 | Dado original persistido com sucesso. | 2025-11-25 04:00:00.000000+00
(1 row)
```

---

## 🧹 Limpeza

Os containers são criados com `--rm`, então são removidos automaticamente.

Para remover o volume e resetar tudo:

```bash
docker volume rm dados_postgres_desafio2
```

---
