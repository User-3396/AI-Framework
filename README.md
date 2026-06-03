# AI-Framework

## Bibliotecas:

### Numpy

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

### Pandas

  `Python` `open source` `dados tabulares`

  Usado para manipulação, análise e processamento de dados estruturados.
  
### Matplotlib

> Usada para visualização de dados por gráficos
>
> ```python
> import matplotlib.pyplot as plt
> valores =[1,2,3,4,5,6,7,8,9,10]
> plt.plot(valores)
> plt.show()
> ```

### EDA (Exploratory Data Analysis)

> É o processo de explorar, resumir e visualizar dados para compreender sua estrutura,
> identificar padrões, detectar anomalias e formular hipóteses
> 
> * Entender o dataset
> * identificar padrões
> * verificar correlaçõers
> * avaliar qualidae dos dados


## Instalações de pacotes/bibliotecas: 

  > `numpy` `pandas` `scikit-learn` (opicional) `matplotlib`

  ```bash
  pip install numpy pandas scikit-learn matplotlib
  ```
  
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

## Métricas 

* `Accuracy`: Mede a porcentagem de acertos gerais do modelo sobre o total de previsões.

* `Precision`: Mede, dentre todas as previsões que o modelo fez como sendo da classe positiva, quantas estavam realmente corretas.

* `Recall` (Sensibilidade): Mede, dentre todas as instâncias que eram realmente positivas, quantas o modelo conseguiu identificar.

* `F1-Score`: É uma média harmônica entre __precisão__ e __recall__, muito útil quando você tem um desequilíbrio entre as classes.
