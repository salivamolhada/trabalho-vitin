-- Esquema relacional SQLite do sistema Solidário Tech
-- Campanha de Natal — Gerenciamento de Doações

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS doacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doador TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('brinquedo', 'alimento', 'roupa', 'dinheiro', 'cesta')),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    data_doacao TEXT NOT NULL,
    descricao TEXT,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS estoque (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT UNIQUE NOT NULL CHECK (tipo IN ('brinquedo', 'alimento', 'roupa', 'dinheiro', 'cesta')),
    quantidade_disponivel INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_disponivel >= 0),
    atualizado_em TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS distribuicoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    doacao_id INTEGER,
    item_tipo TEXT NOT NULL CHECK (item_tipo IN ('brinquedo', 'alimento', 'roupa', 'dinheiro', 'cesta')),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    beneficiario TEXT NOT NULL,
    data_entrega TEXT NOT NULL,
    responsavel TEXT NOT NULL,
    criado_em TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doacao_id) REFERENCES doacoes(id) ON DELETE SET NULL
);

-- Seed inicial das 5 categorias obrigatórias zeradas (idempotente)
INSERT OR IGNORE INTO estoque (tipo, quantidade_disponivel) VALUES ('brinquedo', 0);
INSERT OR IGNORE INTO estoque (tipo, quantidade_disponivel) VALUES ('alimento', 0);
INSERT OR IGNORE INTO estoque (tipo, quantidade_disponivel) VALUES ('roupa', 0);
INSERT OR IGNORE INTO estoque (tipo, quantidade_disponivel) VALUES ('dinheiro', 0);
INSERT OR IGNORE INTO estoque (tipo, quantidade_disponivel) VALUES ('cesta', 0);
