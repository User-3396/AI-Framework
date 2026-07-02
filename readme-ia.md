`Modelagem Preditiva`: ARIMA, SARIMA, Redes LSTM, LightGBM e XGBoost
`Modelos de series temporais`: Metricas var (Vetor Autorregressivo), LSTM ou XGBoost Regressor

- __LSTM__ 
- __Cross-Correlation__:
  - Eventuais impactos da atividade solar no clima terrestre não são imediatos. Use funções de correlação cruzada com lags (atrasos) de 1 a 24 meses para descobrir se um pico solar antecede ou sucede uma alteração no El Niño.
  - Mede a correlação entre duas séries temporais em diferentes defasagens (lags).
  - Exemplo: verificar se picos de manchas solares (SILSO) estão correlacionados com aumento de terremotos meses ou anos depois.

- __Lagging (defasagem de séries)__
  - Criar versões deslocadas da série solar (ex.: irradiância atrasada em 6 meses, 1 ano, etc.).
  - Comparar com séries de terremotos ou fenômenos terrestres.

- __Análise espectral (Fourier/Wavelet)__

  - Identificar periodicidades comuns (ex.: ciclo solar de 11 anos vs. ciclos climáticos ou sísmicos).

- __Modelos de séries temporais multivariadas (VAR, LSTM)__
  - Permitem capturar relações dinâmicas entre múltiplas séries com defasagens.

- __Modelos de Machine Learning__: Para prever o ONI/SOI usando manchas solares, utilize modelos de séries temporais multivariadas como MÉTRICAS VAR (Vetor Autorregressivo), Redes Neurais LSTM ou algoritmos de boosting como o XGBoost Regressor, inserindo as manchas solares defasadas no tempo como features preditivas.

* __Exemplo__: 

```python
import pandas as pd
import matplotlib.pyplot as plt

# Supondo que você já tenha os DataFrames eq (terremotos) e sunspots (manchas solares)
# Agregar por mês para facilitar
eq_monthly = eq.groupby(eq['date'].dt.to_period('M')).Magnitude.mean()
sunspots_monthly = sunspots.groupby(sunspots['date'].dt.to_period('M')).sunspot_number.mean()

# Converter para séries temporais
eq_series = eq_monthly.to_timestamp()
sun_series = sunspots_monthly.to_timestamp()

# Alinhar datas
data = pd.concat([eq_series, sun_series], axis=1)
data.columns = ['Magnitude_media','Sunspots']

# Calcular correlação cruzada com defasagem
lags = range(-24, 25)  # até 2 anos de atraso/adiantamento
correlations = [data['Magnitude_media'].corr(data['Sunspots'].shift(lag)) for lag in lags]

# Plotar correlação vs. lag
plt.figure(figsize=(10,5))
plt.plot(lags, correlations, marker='o')
plt.axhline(0, color='gray', linestyle='--')
plt.xlabel("Defasagem (meses)")
plt.ylabel("Correlação")
plt.title("Correlação cruzada entre terremotos e manchas solares")
plt.show()
```

### Interpretação

- Se aparecer um pico de correlação em lag positivo, significa que a atividade solar antecede os fenômenos terrestres.
- Se o pico for em lag negativo, significa que os fenômenos terrestres ocorrem antes dos sinais solares (menos provável).
- Se não houver correlação significativa, pode indicar ausência de relação direta ou necessidade de considerar outros fatores intermediários (ex.: clima, tectônica).

# Técnicas

1. __Downsampling Estatístico (Agregação)__

Em vez de usar dados a cada minuto, reduza a frequência para intervalos horários (1H) ou diários (1D). Isso diminui drasticamente o volume de dados, além de remover ruídos de alta frequência.

- __Média ou Mediana__: Preservam a tendência central dos dados (ex: nível da água ou temperatura média).
- __Mínimo e Máximo (Min/Max)__: Essenciais para capturar a amplitude de variação em dados ambientais ou hidrológicos.
- __Técnica OHLC__: Usada no mercado financeiro, mas excelente para dados climáticos extremos. Agrupa o primeiro (Open), o maior (High), o menor (Low) e o último (Close) valor do período.

2. __Criação de Features de Janelas (Rolling Windows)__
Modelos preditivos precisam conhecer o passado. Crie janelas deslizantes para calcular estatísticas sobre o histórico recente (ex: a média dos últimos 7 dias).

- __Lag Features__: Valores de t-1, t-24, etc.
- __Rolling Features__: Média móvel, desvio padrão móvel ou variância móvel dentro da janela.

```python
import pandas as pd
import numpy as np

# Supondo que 'df' já foi carregado com dados por minuto e tem o 'datetime' como índice
df = df.sort_index()

# 1. Downsampling: Reduzindo de minuto para hora (calcula a média e o desvio padrão)
df_hourly = df.resample('1H').agg({
    'valor_observado': ['mean', 'std', 'max', 'min']
})

# Nivelar o MultiIndex gerado pelo agg
df_hourly.columns = ['media', 'desvio_padrao', 'maximo', 'minimo']

# 2. Feature Engineering: Janela Deslizante (Rolling Window)
# Exemplo: Média móvel das últimas 24 horas (janela de 1 dia)
df_hourly['media_movel_24h'] = df_hourly['media'].rolling(window=24).mean()

# 3. Lag Features: Valor da variável alvo há 24 horas (passado)
df_hourly['lag_24h'] = df_hourly['media'].shift(24)

# Limpar valores nulos gerados pelas janelas e lags
df_final = df_hourly.dropna()
```

### Boas Práticas para o Pipeline

- __Evite Data Leakage__: Ao calcular janelas, calcule somente com base em dados do passado em relação à linha do tempo preditiva.
- __Lidar com Falhas__: Dados de sensores do USGS e NOAA podem ter falhas (NaNs). Certifique-se de preencher esses buracos com interpolação linear simples antes do downsampling.
- __Formato de Armazenamento__: Para dataframes de vários anos, exporte os dados limpos em formatos colunais otimizados e comprimidos para leitura rápida, como `.parquet` ou `.zarr`, em vez de arquivos CSV. [[1](https://waterdata.usgs.gov/blog/cloud_data/)]
