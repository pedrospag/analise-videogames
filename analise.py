from pathlib import Path
import pandas as pd         

# localiza o csv a partir da pasta deste script
caminho = Path(__file__).resolve().parent / 'vgsales.csv'

# carrega o arquivo em uma tabela
dados = pd.read_csv(caminho)

# mostra uma amostra dos registros
print(dados.head())

# exibe a quantidade de linhas e colunas
print("\nDimensões da tabela:", dados.shape)

# conta os valores ausentes em cada coluna
print("\nValores ausentes:")
print(dados.isna().sum())

# cria uma cópia para tratar sem alterar a tabela original
dados_tratados = dados.copy()

# converte o ano para inteiro, permitindo valores ausentes
dados_tratados["Year"] = dados_tratados["Year"].astype('Int64')

# identifica as publicadoras que não foram informadas
dados_tratados["Publisher"] = dados_tratados["Publisher"].fillna("Não informado")

# confere os tipos após o tratamento
print("\nTipos das colunas:")
print(dados_tratados.dtypes)

# mostra os anos e as publicadoras tratados
print("\nAmostra após o tratamento:")
print(dados_tratados[["Name","Year", "Publisher"]].head())

# confirma os anos que continuam sem informação
print("\nRegistros sem ano:", dados_tratados["Year"].isna().sum())