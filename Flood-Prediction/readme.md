## Tecnicas: 
- Random Forest, Gradient Boosting, CNN aplicadas em mapas geoespaciais

## Datasets: 
- `Global Flood Database (NASA)` ou o `Flood Prediction Dataset (Kaggle)`

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
