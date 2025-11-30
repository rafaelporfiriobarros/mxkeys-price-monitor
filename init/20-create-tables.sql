\connect precos;

CREATE TABLE IF NOT EXISTS precos (
    id SERIAL PRIMARY KEY,
    produto VARCHAR(255) NOT NULL,
    site VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    preco NUMERIC(10,2),
    data_coleta TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_preco_produto_data
ON precos (produto, data_coleta DESC);
