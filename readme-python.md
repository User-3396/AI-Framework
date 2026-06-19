## Comandos Pandas:

<details><summary>detalhes</summary>

### Fazendo um DataFrame

```python
data = {'Name': ['Tom', 'Nick', 'Krish', 'Jack'], 'Age': [20, 21, 19, 18]}
df = pd.DataFrame(data)

# Fazendo um DataFrame de um numpy array
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
df = pd.DataFrame(data, columns=['a', 'b', 'c'])
```

</details>

```python
# Exibe colunas e tipos de dados
print(df.dtypes)
```

```python
# Exibe resumo completo do DataFrame
df.info()
```

### Seleção/exploração de linhas/dados:

<details><summary>detalhes</summary>

- __df.shape__: Retorna uma tupla com a quantidade de linhas e colunas → (linhas, colunas).
- __df.info()__: Mostra os tipos de dados de cada coluna e a quantidade de valores não-nulos.
- __df.describe()__: Exibe um resumo estatístico das colunas numéricas (média, desvio padrão, mínimo, máximo).
- __df.columns__: Retorna uma lista com o nome de todas as colunas.
- __df.loc[linha, 'Coluna']__: Acessa dados específicos usando os rótulos do índice e da coluna.
- __df.iloc[linha_idx, col_idx]__: Acessa dados usando a posição numérica (índice inteiro).
- __df[df['Idade'] > 30]__: Filtra o DataFrame retornando apenas as linhas onde a condição é verdadeira.

- __df.dropna()__: Remove linhas que possuem pelo menos um valor vazio (NaN).
- __df.fillna(valor)__: Preenche os valores vazios com um valor específico ou cálculo (ex: df.mean()).
- __df.drop('Coluna', axis=1)__: Deleta a coluna especificada.
- __df.rename(columns={'Velho': 'Novo'})__: Renomeia colunas.
- __df['Coluna'].astype(int)__: Altera o tipo de dado da coluna (ex: de string para inteiro).

```python
# Ordenar
df_ordenado = df.sort_values(by='id')
df_ordenado = df.sort_values(by='id', ascending=False)

```


### Agrupamento e Estatística
Comandos utilizados para extrair insights e agregar valores.

- __df['Coluna'].value_counts()__: Conta a ocorrência de cada valor único na coluna.
- __df['Coluna'].unique()__: Retorna os valores únicos de uma coluna.
- __df.groupby('Coluna').mean()__: Agrupa os dados com base em uma coluna e calcula a média das outras.
- __df.sort_values(by='Coluna', ascending=False)__: Ordena o DataFrame pelos valores de uma coluna (do maior para o menor).

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

# numero de linhas e colunas:
print(df.shape)

total_linhas = df.shape[0]   # Pega apenas o primeiro número
total_colunas = df.shape[1]  # Pega apenas o segundo número

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
df['speed'] =df['speed'].astype(float)
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

### Tratamento de nulls e NaN:

<details><summary>detalhes</summary>

```python
# lista nulos
df.isnull()

# Dropping rows with missing values
df.dropna(inplace=True)

# Filling missing values with 0
df.fillna(0, inplace=True)

# Dropping rows with missing values
df.dropna(inplace=True)

# Remover do dataframe nulos
# vetor auxiliar de booleanos, onde true se houver valor valido
i =df['x'].notna() & dataSolar['y'].notna() # linhas com 'x' e 'y' validos
df =df[i]
```

</details>

### Importação de dados csv:

```python
# Substitua o nome da pasta e do arquivo pelo caminho real
df = pd.read_csv('../input/nome-do-dataset/nome-do-arquivo.csv')
```
### Dataframes: `pd.merge`

- __Estrutura__: 

```python
resultado = pd.merge(df_esquerda, df_direita, on='coluna_chave', how='inner')

# on='...' indica qual coluna será usada como chave de junção entre os dois DataFrames, sendo o nome igual em ambas as tabelas
```

<details><summary>detalhes</summary>

- __Principais Parâmetros__:

- `on`: Nome da coluna (ou lista de colunas) presente em ambos os DataFrames que servirá como "chave" para a união.
- `left_on` e `right_on`: Usados quando as colunas que você deseja usar como chave possuem nomes diferentes em cada DataFrame.
- `how`: Define a lógica de como as linhas que não dão match são tratadas. As opções são:
  - `'inner'` (Padrão): Retorna apenas as linhas onde as chaves existem em ambos os DataFrames.
  - `'left'`: Mantém todas as linhas do DataFrame da esquerda e adiciona as correspondentes da direita. Onde não há correspondência, insere NaN.
  - `'right'`: Mantém todas as linhas do DataFrame da direita e adiciona as correspondentes da esquerda. Preenche com NaN onde não há match.
  - `'outer'`: Retorna todas as linhas de ambos os DataFrames. Preenche com NaN onde os dados não se cruzam.

- __Exemplo__:

```python
import pandas as pd

# Tabela 1: Vendas
df_vendas = pd.DataFrame({
    'id_venda': [1, 2, 3],
    'id_produto': [101, 102, 101],
    'valor': [50, 30, 50]
})

# Tabela 2: Produtos
df_produtos = pd.DataFrame({
    'id_produto': [101, 102],
    'nome': ['Caneta', 'Lápis']
})

# Cruzando as tabelas
df_completo = pd.merge(df_vendas, df_produtos, on='id_produto', how='inner')
print(df_completo)
```
</details>

### Plotagem

<details><summary>detalhes</summary>

```python
# Redimensionamento
plt.figure(figsize=(10, 6))

# Altera o fundo interno (área do gráfico)
plt.gca().set_facecolor('#0F0F0F') 

# Altera o fundo externo (área da figura completa)
plt.gcf().patch.set_facecolor('#e0e0e0') 

# print(dataSolar[['startTime', 'speed']].head(12))
x =dataSolar['data'].head(50)
y =dataSolar['num_manchas'].head(50)
y2 =dataSolar['desvio_padrao'].head(50)
# df = df.sort_values('data_grafico') # Ordenar por data
plt.plot(x,y, label="manchas", color='green', linestyle='-', marker='o')
plt.plot(x,y2, label="desvio padrao", color='yellow', linestyle='--', marker='o')
# sns.scatterplot(data=data_clean, x ='speed', y ='halfAngle', hue='type', palete='viridis', s =100)
# sns.lineplot(data=data_clean, x ='speed', y ='halfAngle', hue='type', palete='viridis', s =100)

# plt.title('Comparação entre Velocidade e Ângulo de Abertura das CMEs')
# plt.xlabel('Velocidade (km/s)')
# plt.ylabel('Meio Ângulo (Graus)')
# plt.grid(True, linestyle='--', alpha=0.5)

plt.legend()
plt.show()
```
</details>

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
