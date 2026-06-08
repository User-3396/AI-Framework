## Tipo de Problema a Tratar:

`Aprendizado-não-supervisionado`

## Tecnicas: 

- Random Forest, Gradient Boosting, CNN aplicadas em mapas geoespaciais

## Datasets: 

- __Subject__: Atividades solares []
- __Resultados__:
  - `Global Flood Database (NASA)`
  - `Flood Prediction Dataset (Kaggle)`
  - [`Atmospheric and Oceanic Dynamics`](https://www.kaggle.com/datasets/muhammadzakria2001/atmospheric-and-oceanic-dynamics?select=All_Feature_Data.csv)

> ```Python
> import pandas as pd
> 
> # Caminho local do arquivo ou URL direta do dataset
> df = pd.read_csv('caminho/do/arquivo.csv')
> 
> # Visualizar as primeiras linhas
> print(df.head())
> ```

> ```Python
> # Verificar valores nulos
> print(df.isnull().sum())
> 
> # Remover ou preencher valores ausentes
> df = df.dropna()  # ou df.fillna(valor)
> ```
