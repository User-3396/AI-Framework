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

