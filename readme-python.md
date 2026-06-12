```python
# Exibe colunas e tipos de dados
print(df.dtypes)
```

```python
# Exibe resumo completo do DataFrame
df.info()
```

### Seleção de linhas/dados:
<details><summary>detalhes</summary>
  
```python
# Mostrar as primeiras 5 linhas
print(df.head())

# Mostrar as ultimas 5 linhas
print(df.tail())

# Mostrar x primeiras/ultimas linhas
print(df.head(x))
print(df.tail(x))

# A. Filtrando o ano de 2020
df_2020 = df[df['data'].between('2020-01-01', '2020-12-31')]

# B. Filtrando direto pelo ano 2020
df_2020 = df[df['data'].dt.year == 2020]

# C. 
resultado = df[(df["nome_da_coluna"] >= "2020-01-01") & (df["nome_da_coluna"] <= "2020-12-31")]

# D. Filtrando com uma string de consulta
resultado = df.query("'2020-01-01' <= nome_da_coluna <= '2020-12-31'")

```

</details>

### Conversão de tipos:
<details><summary>detalhes</summary>

```python
# de um objeto/texto para datetime:
df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')
```

```python
colunas = ['ano', 'mes', 'dia', 'data_decimal', 'num_manchas', 'desvio_padrao', 'num_observacoes', 'status']

# Lendo o arquivo adicionando os nomes das colunas e tratando o ponto e vírgula
df = pd.read_csv('../input/seu-dataset/SN_d_tot_V2.0.csv', sep=';', names=colunas)
```

```python
# Conta os valores nulos de cada coluna
print(df.isnull().sum())
```

```python
# Conta todos os valores nulos do dataset inteiro
print(df.isnull().sum().sum())
```
</details>

### Importação de dados csv:

```python
# Substitua o nome da pasta e do arquivo pelo caminho real
df = pd.read_csv('../input/nome-do-dataset/nome-do-arquivo.csv')
```

### Exemplo de importação:

```python
import pandas as pd

# 1. Carregar dados solares (ex: SILSO manchas solares mensais)
df_solar = pd.read_csv('solar_spots_monthly.csv', parse_dates=['Date'])
df_solar.set_index('Date', inplace=True)

# 2. Carregar dados climáticos (ex: HadCRUT5 anomalias mensais)
df_clima = pd.read_csv('hadcrut5_anomalies_monthly.csv', parse_dates=['Date'])
df_clima.set_index('Date', inplace=True)

# 3. Mesclar os datasets pela data correspondente (Inner Join)
df_correlacao = pd.merge(df_solar, df_clima, left_index=True, right_index=True)

# 4. Calcular a correlação de Pearson ou Spearman
resultado_correlacao = df_correlacao.corr(method='pearson')
print(resultado_correlacao)
```
