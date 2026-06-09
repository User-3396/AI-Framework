# AI-Framework

## Função

__Detecção de Anomalias com Aprendizado Não Supervisionado__ 

- __Objetivo__: Identificar eventos climáticos atípicos na Terra que aconteceram exatamente no mesmo momento de picos solares anômalos, sem precisar rotular os dados manualmente.
- __IA Utilizada__: Autoencoders (Redes Neurais de Compressão) ou Isolation Forests.
- __Como funciona__: A IA aprende o comportamento normal "Sol-Terra" dos últimos 100 anos. Quando ocorre uma combinação de dados que foge do padrão aprendido, o modelo acende um alerta (alto erro de reconstrução).
- __Finalidade Prática__: Descoberta científica de novas correlações ou reações em cadeia na alta atmosfera que a ciência ainda não mapeou.

```python
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

# Criando 'lags' (atrasos) para a IA entender o tempo
# O clima responde ao sol meses depois
df_correlacao['solar_lag_1_mes'] = df_correlacao['Sunspots'].shift(1)
df_correlacao['solar_lag_6_mes'] = df_correlacao['Sunspots'].shift(6)
df_correlacao.dropna(inplace=True)

# X = Atividade solar (presente e passada) | y = Anomalia de temperatura na Terra
X = df_correlacao[['Sunspots', 'solar_lag_1_mes', 'solar_lag_6_mes']]
y = df_correlacao['Temperature_Anomaly']

# Treinar o modelo de IA
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
modelo = XGBRegressor()
modelo.fit(X_train, y_train)
```

<img src="js-hex.svg">

## Bibliotecas
- <details>
  <summary><kbd>Numpy</kbd></summary>

  - operações matemáticas vetorizadas
  - suporte para arrays multidimensionais
  - base para Pandas, Scikit-learn, TensorFlow e Pytorch

  ```python
  import numpy as np

  a = np.array([1, 2, 3, 4])
  print(a)
  print(type(a))
  ```

  ```log
  [1 2 3 4]
  <class 'numpy.ndarray'>
  ```
</details> 

- <details>
  <summary>Pandas</summary>

  `Python` `open source` `dados tabulares`

  <p style="background-color: rgb(100,80,0)">Usado para manipulação, análise e processamento de dados estruturados.</p>
</details> 

- <details>
  <summary>Matplotlib</summary>
  
  Usada para visualização de dados por gráficos
  
  ```python
  import matplotlib.pyplot as plt
  valores =[1,2,3,4,5,6,7,8,9,10]
  plt.plot(valores)
  plt.show()
  ```
</details>

### EDA (Exploratory Data Analysis)

 É o processo de explorar, resumir e visualizar dados para compreender sua estrutura, identificar padrões, detectar anomalias e formular hipóteses

* Entender o dataset
* identificar padrões
* verificar correlaçõers
* avaliar qualidae dos dados

## Instalações de pacotes/bibliotecas: 

![](https://img.shields.io/badge/Numpy-green) * ![](https://img.shields.io/badge/Pandas-yellow) * ![](https://img.shields.io/badge/opicional-scikit--learn-blue) * ![](https://img.shields.io/badge/matplotlib-red)

> ```bash
> pip install numpy pandas scikit-learn matplotlib
> ```

Se usar PyTorch:

```bash
pip install torch torchvision torchaudio
```

Se usar TensorFlow:

```bash
pip install tensorflow
```

---

## Pipeline

> ## Métricas 
> 
> * `Accuracy`: Mede a porcentagem de acertos gerais do modelo sobre o total de previsões.
> * `Precision`: Mede, dentre todas as previsões que o modelo fez como sendo da classe positiva, quantas estavam realmente corretas.
> * `Recall` (Sensibilidade): Mede, dentre todas as instâncias que eram realmente positivas, quantas o modelo conseguiu identificar.
> * `F1-Score`: É uma média harmônica entre __precisão__ e __recall__, muito útil quando você tem um desequilíbrio entre as classes.

> # Kaggle 
> 
> - baixar e extrair um dataset .csv
> - carregar-lo pelo script:
> ```pyhon
> import pandas as pd
> df =pd.read_csv('nome_do_arquivo.csv')
> ```


