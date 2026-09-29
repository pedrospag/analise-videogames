from getpass import getpass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import psycopg


def consultar_vendas(senha, ano_inicial, ano_final):
    # Consulta as vendas por gênero e região
    sql = """
        SELECT
            genero,
            SUM(vendas_na) AS america_norte,
            SUM(vendas_eu) AS europa,
            SUM(vendas_jp) AS japao,
            SUM(vendas_outros) AS outras_regioes
        FROM vendas_jogos
        WHERE ano BETWEEN %s AND %s
        GROUP BY genero
        ORDER BY japao DESC, genero;
    """

    with psycopg.connect(
        host="localhost",
        port=5432,
        dbname="analise_videogames",
        user="postgres",
        password=senha
    ) as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(sql, (ano_inicial, ano_final))

            registros = cursor.fetchall()
            colunas = [coluna.name for coluna in cursor.description]

    # Retorna os resultados como uma tabela
    return pd.DataFrame(registros, columns=colunas)


def gerar_grafico_japao(dados, pasta_graficos):
    # Prepara uma cópia para o gráfico
    dados_grafico = dados[["genero", "japao"]].copy()
    dados_grafico["japao"] = dados_grafico["japao"].astype(float)
    dados_grafico = dados_grafico.sort_values("japao")

    fig, ax = plt.subplots(figsize=(10, 6))

    barras = ax.barh(
        dados_grafico["genero"],
        dados_grafico["japao"],
        color="#2563EB"
    )

    # Adiciona os valores nas pontas das barras
    rotulos = [
        f"{valor:.2f}".replace(".", ",")
        for valor in dados_grafico["japao"]
    ]
    ax.bar_label(barras, labels=rotulos, padding=4)
    ax.set_xlim(0, max(dados_grafico["japao"].max() * 1.15, 1))

    ax.set_title(
        "Vendas no Japão por gênero\n"
        "Jogos lançados de 2010 a 2015"
    )
    ax.set_xlabel("Vendas acumuladas na base (milhões de unidades)")
    ax.set_ylabel("Gênero")

    fig.tight_layout()
    fig.savefig(pasta_graficos / "vendas_genero_japao.png", dpi=150)

    return fig


def gerar_comparativo_regioes(dados, pasta_graficos):
    regioes = ["america_norte", "europa", "japao"]
    titulos = ["América do Norte", "Europa", "Japão"]
    cores = ["#2563EB", "#D97706", "#059669"]

    # Prepara as regiões na mesma ordem de gêneros
    comparativo = dados.set_index("genero")[regioes].astype(float)
    comparativo = comparativo.sort_values("japao", ascending=False)

    fig, eixos = plt.subplots(
        nrows=1,
        ncols=3,
        figsize=(16, 7),
        sharex=True,
        sharey=True
    )

    # Desenha um painel para cada região
    for eixo, regiao, titulo, cor in zip(
        eixos, regioes, titulos, cores
    ):
        eixo.barh(comparativo.index, comparativo[regiao], color=cor)
        eixo.set_title(titulo)
        eixo.set_xlabel("Milhões de unidades")
        eixo.set_axisbelow(True)
        eixo.grid(axis="x", alpha=0.2)

    eixos[0].invert_yaxis()
    eixos[0].set_ylabel("Gênero")

    fig.suptitle(
        "Vendas acumuladas por gênero e região\n"
        "Jogos lançados de 2010 a 2015"
    )
    fig.tight_layout()

    fig.savefig(
        pasta_graficos / "comparativo_regioes.png",
        dpi=150,
        bbox_inches="tight"
    )

    return fig


def main():
    # Consulta os dados uma única vez
    senha = getpass("Senha do PostgreSQL: ")
    dados = consultar_vendas(senha, 2010, 2015)

    if dados.empty:
        print("Nenhum registro encontrado para o período.")
        return

    print(dados.to_string(index=False))

    # Prepara a pasta de saída
    pasta_graficos = Path(__file__).resolve().parent / "graficos"
    pasta_graficos.mkdir(exist_ok=True)

    gerar_grafico_japao(dados, pasta_graficos)
    gerar_comparativo_regioes(dados, pasta_graficos)

    print(f"\nGráficos salvos em: {pasta_graficos}")
    plt.show()


if __name__ == "__main__":
    main()