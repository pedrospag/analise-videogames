-- Execute este arquivo no banco analise_videogames.
CREATE TABLE IF NOT EXISTS vendas_jogos (
    ranking INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    plataforma TEXT NOT NULL,
    ano INTEGER,
    genero TEXT NOT NULL,
    publicadora TEXT NOT NULL,
    vendas_na NUMERIC(10, 2) NOT NULL,
    vendas_eu NUMERIC(10, 2) NOT NULL,
    vendas_jp NUMERIC(10, 2) NOT NULL,
    vendas_outros NUMERIC(10, 2) NOT NULL,
    vendas_global NUMERIC(10, 2) NOT NULL
);
