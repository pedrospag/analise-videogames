import psycopg
from getpass import getpass

# solicita a senha sem exibi-la no terminal
senha = getpass("Senha do PostgreSQL: ")

# abre a conexão e a fecha ao finalizar o bloco
with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="analise_videogames",
    user="postgres",
    password=senha
) as conexao:
    with conexao.cursor() as cursor:
        # confere o banco conectado e a quantidade de registros
        cursor.execute(
            "SELECT current_database(), COUNT(*) FROM vendas_jogos;"
        )

        banco, quantidade = cursor.fetchone()

        print(f"Banco conectado: {banco}")
        print(f"Registros na tabela: {quantidade}")