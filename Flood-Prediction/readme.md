## Tipo de Problema a Tratar:

<div align="center" style="background-color: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 5px; border-left: 5px solid #17a2b8;">
  <strong>Aprendizado-não-supervisionado</strong>
</div>

## Tecnicas: 

- Random Forest, Gradient Boosting, CNN aplicadas em mapas geoespaciais

## Datasets: 

- __Subject__: Atividades solares
  - [DTSN - 01-01-1818_now](https://www.sidc.be/SILSO/datafiles#total) - Número diário total de Sunspot, de 1818 a 'agora'. _Fonte: Royal Observatory of Belgium, SIDC (SILSO)_
- __Resultados__:
  - `Global Flood Database (NASA)`
  - `Flood Prediction Dataset (Kaggle)`
  - [`Atmospheric and Oceanic Dynamics`](https://www.kaggle.com/datasets/muhammadzakria2001/atmospheric-and-oceanic-dynamics?select=All_Feature_Data.csv)
 
  
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
  
  # dataSolar =pd.read_csv('datasets/nasa_cme.csv')
  dataSolar =pd.read_csv('/kaggle/input/datasets/ankush000singh/nasa-cme-space-weather-dataset-20002020/nasa_cme_dataset (1).csv')
  # dataFlood =pd.read_csv('datasets/Unknow/flood.csv')
  # print(dataSolar.head())
  # print(dataSolar.head())
  
  # Tratamendo dos dados:
  ## 1. NaN de colunas
  i =dataSolar['startTime'].notna() & dataSolar['speed'].notna() # vetor booleano auxiliar onde não ha NaN
  dataSolar =dataSolar[i]
  
  
  # data_clean =dataSolar.dropna(subset=['speed', 'halfAngle'])#.copy()
  
  ## 2. Correção de tipagem
  # data_clean['speed'] =data_clean['speed'].astype(float)
  # data_clean['halfAngle'] =data_clean['halfAngle'].astype(float)
  
  dataSolar['startTime'] =pd.to_datetime(dataSolar['startTime'], utc=True) # Conversao para datetime
  dataSolar =dataSolar.sort_values('startTime') # Ordenar
  
  # dataSolar['startTime'] =dataSolar['startTime'].dt.strftime('%Y%m%d').astype(int) # Conversao para int
  # print(dataSolar['startTime'].iloc[0:12])
  # Linhas e colunas:
  # print(dataSolar.shape)
  # print(data_clean.shape)
  
  
  
  # t =dataSolar["startTime"] # tempo/data
  # t =dataSolar["startTime"].iloc(40:100) # tempo/data
  # print(data_clean.head(10)['startTime', 'speed', 'halfAngle'])
  # print(data_clean.iloc[10:20])
  
  ## 3. Grafico
  # plt.figure(figsize=(10, 6), facecolor='#101010')
  # print(dataSolar[['startTime', 'speed']].head(12))
  x =dataSolar['startTime'].head(2)
  y =dataSolar['speed'].head(2)
  # df = df.sort_values('data_grafico') # Ordenar por data
  plt.plot(x,y, label="relação", color='green', linestyle='--', marker='o')
  # sns.scatterplot(data=data_clean, x ='speed', y ='halfAngle', hue='type', palete='viridis', s =100)
  # sns.lineplot(data=data_clean, x ='speed', y ='halfAngle', hue='type', palete='viridis', s =100)
  
  # plt.title('Comparação entre Velocidade e Ângulo de Abertura das CMEs')
  # plt.xlabel('Velocidade (km/s)')
  # plt.ylabel('Meio Ângulo (Graus)')
  # plt.grid(True, linestyle='--', alpha=0.5)
  
  # # plt.legend()
  # plt.show()
  ```
</details>



## Estudos

https://www.biorxiv.org/content/biorxiv/early/2018/10/20/448449.full.pdf
https://www.sciencedaily.com/releases/2019/03/190321083637.htm
