-- Cria uma tabela de persistência
CREATE TABLE registros_teste (
    id SERIAL PRIMARY KEY,
    mensagem VARCHAR(255) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insere um registro inicial
INSERT INTO registros_teste (mensagem) VALUES ('Dado original persistido com sucesso.');