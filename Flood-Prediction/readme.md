## Tipo de Problema a Tratar:

<div align="center" style="background-color: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; border-left: 5px solid #17a2b8;">
  <strong>Aprendizado-não-supervisionado</strong>
</div>

## Tecnicas: 

- `Random Forest` `Gradient Boosting` `CNN aplicadas em mapas geoespaciais`

## Datasets: 

- __Subject__: Atividades solares
  - [DTSN - 01-01-1818_now](https://www.sidc.be/SILSO/datafiles#total) - Número diário total de Sunspot, de 1818 a 'agora'. _Fonte: Royal Observatory of Belgium, SIDC (SILSO)_
- __Resultados__:
  - `Global Flood Database (NASA)`
  - `Flood Prediction Dataset (Kaggle)`
  - `Atmospheric and Oceanic Dynamics` [[src](https://www.kaggle.com/datasets/muhammadzakria2001/atmospheric-and-oceanic-dynamics?select=All_Feature_Data.csv)]

  <details><summary>Topics</summary>
  
    `GMSL` (Global Mean Sea Level)
    
    - `Date` [1880 - 2024]
    - `GMSL` [-192 - 83.9]
    - `CO2 conc.` [288 - 421]
    - `CO2 emissions` [858m - 38.5b]
    - `Long-run NO2 concentration` [276 - 338]
    - `Per-capita NO2 emissions in CO2 equivalents` []
    - `Long-run CH4 concentration` []
    - `Per-capita methane emissions in CO2 equivalents` []
    - `Global avg temp. anomaly relative to 1961-1990` []
    - `Sea surface temperature anomaly (relative to 1961-90 average)` []

  </details>

<details><summary>Juntando os dataframes</summary>

Para fazer um gráfico de correlação entre dois DataFrames diferentes (como o de Terremotos e o de Clima Espacial/Dst), você deve primeiro unificar os dados pela data usando o método `pd.merge_asof()` do Pandas (ideal para alinhar horários que não batem exatamente). Depois, você calcula a correlação com `.corr()` e usa o Seaborn para desenhar um mapa de calor (`heatmap`).
Aqui está o passo a passo completo e o código para gerar o gráfico:

1. Passo Preparatório: Alinhar e Juntar os DataFramesAntes de cruzar os dados, as colunas de tempo de ambos os DataFrames precisam estar ordenadas e convertidas para o formato `datetime`.

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Garantir que as colunas de tempo são datetime e estão ordenadas
dfEQ = dfEQ.sort_values('data')
df_dst = df_dst.sort_values('time')

# 2. Mesclar os dataframes pelo horário mais próximo (Merge Asof)
# Ele vai associar cada terremoto ao índice Dst medido naquela hora correspondente
df_unificado = pd.merge_asof(
    dfEQ, 
    df_dst, 
    left_on='data', 
    right_on='time', 
    direction='nearest'
)
```

2. Gerar o Gráfico de Correlação (Matriz e Heatmap)

Agora que os dados de magnitude e Dst estão na mesma linha, você filtra apenas as colunas numéricas que quer analisar e plota o gráfico:

```python
# 3. Selecionar apenas as colunas numéricas de interesse para a correlação
# (Substitua pelos nomes exatos das suas colunas)
colunas_analise = ['magnitude', 'dst']
df_correlacao = df_unificado[colunas_analise].dropna()

# 4. Calcular a matriz de correlação de Pearson
matriz_corr = df_correlacao.corr()

# 5. Configurar e desenhar o Gráfico (Heatmap)
plt.figure(figsize=(6, 4))
sns.heatmap(
    matriz_corr, 
    annot=True,          # Mostra o valor numérico da correlação dentro do quadrado
    cmap='coolwarm',     # Paleta de cor (azul para negativo, vermelho para positivo)
    fmt=".2f",           # Limita a duas casas decimais
    vmin=-1, vmax=1      # Força a escala a ir de -1 a 1
)

plt.title('Correlação: Atividade Sísmica vs Índice Dst')
plt.tight_layout()
plt.show()
```

3. Alternativa: Gráfico de Dispersão (Scatter Plot) com Linha de Tendência

Se você quiser visualizar a distribuição ponto a ponto para ver se há um padrão visual claro entre o Dst e a magnitude:

```python
plt.figure(figsize=(8, 5))
sns.regplot(data=df_correlacao, x='dst', y='magnitude', scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Dispersão: Índice Dst vs Magnitude do Terremoto')
plt.xlabel('Índice Dst (nT)')
plt.ylabel('Magnitude (Richter)')
plt.grid(True, alpha=0.3)
plt.show()
```

</details>

## Codding:

<details>
  <summary><kbd>Python</kbd></summary>
  
  ```Python
  import pandas as pd
  
  # Caminho local do arquivo ou URL direta do dataset
  df = pd.read_csv('caminho/do/arquivo.csv')
  
  # Visualizar as primeiras linhas
  print(df.head())
  ```
</details>


<details>
  <summary><kbd>Python</kbd></summary>

  ```Python
  # Verificar valores nulos
  print(df.isnull().sum())
  
  # Remover ou preencher valores ausentes
  df = df.dropna()  # ou df.fillna(valor)
  ```
</details>

<details>
  <summary>to import</summary>
  
  ```python
  import numpy as np # linear algebra
  import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
  import matplotlib.pyplot as plt
  import seaborn as sns
  
  dataSolar =pd.read_csv('./datasets/DTSN-01-01-1818.csv')


  # Tratamendo dos dados:
  # Tratar os valores ausentes (-1) para que não apareçam no gráfico:
  dataSolar['num_manchas'] = dataSolar['num_manchas'].replace(-1, None)

  ## Remover NaN de colunas
  # i =dataSolar['startTime'].notna() & dataSolar['speed'].notna() # vetor booleano auxiliar onde não ha NaN
  # dataSolar =dataSolar[i]
  # data_clean =dataSolar.dropna(subset=['speed', 'halfAngle'])#.copy()
  
  ## Remover Null ou None:
  dataSolar =dataSolar[dataSolar['num_manchas'].notnull()]


  ## Correção de tipagem
  # data_clean['speed'] =data_clean['speed'].astype(float)
  # data_clean['halfAngle'] =data_clean['halfAngle'].astype(float)
  
  # dataSolar['startTime'] =pd.to_datetime(dataSolar['startTime'], utc=True) # Conversao para datetime
  # dataSolar =dataSolar.sort_values('startTime') # Ordenar

  # dataSolar['startTime'] =dataSolar['startTime'].dt.strftime('%Y%m%d').astype(int) # Conversao para int
  # print(dataSolar['startTime'].iloc[0:12])

  # Linhas e colunas:
  # print(dataSolar.shape)
  # print(data_clean.shape)


  ## 3. Grafico
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



## Estudos

https://www.biorxiv.org/content/biorxiv/early/2018/10/20/448449.full.pdf
https://www.sciencedaily.com/releases/2019/03/190321083637.htm
