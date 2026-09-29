from pathlib import Path
from getpass import getpass

import pandas as pd
import psycopg

# lê o arquivo original
caminho = Path(__file__).resolve().parent / 'vgsales.csv'
dados = pd.read_csv(caminho)

# trata os anos e as publicadoras ausentes
dados["Year"] = dados["Year"].astype("Int64")
dados["Publisher"] = dados["Publisher"].fillna("Não informado")

registros = []

# converte cada linha em uma tupla de valores
for linha in dados.itertuples(index=False):
    ano = None if pd.isna(linha.Year) else int(linha.Year)

    registros.append((
        int(linha.Rank),
        linha.Name,
        linha.Platform,
        ano,
        linha.Genre,
        linha.Publisher,
        float(linha.NA_Sales),
        float(linha.EU_Sales),
        float(linha.JP_Sales),
        float(linha.Other_Sales),
        float(linha.Global_Sales)
    ))

sql = """
    INSERT INTO vendas_jogos (
        ranking, nome, plataforma, ano, genero, publicadora,
        vendas_na, vendas_eu, vendas_jp, vendas_outros, vendas_global
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

senha = getpass("Senha do PostgreSQL: ")
importou = False

# usa os mesmos dados do teste de conexão
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="analise_videogames",
    user="postgres",
    password=senha
) as conexao:
    with conexao.cursor() as cursor:
        # evita repetir a carga ao executar o script novamente
        cursor.execute("SELECT COUNT(*) FROM vendas_jogos;")
        quantidade = cursor.fetchone()[0]

        if quantidade > 0:
            print("A tabela já contém dados. Importação não realizada.")
        else:
            cursor.executemany(sql, registros)
            importou = True

# a confirmação aparece após a transação ser concluída
if importou:
    print(f"Importação concluída: {len(registros)} registros.")