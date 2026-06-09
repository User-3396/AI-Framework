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
