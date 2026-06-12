import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. DOWNLOAD E TRATAMENTO DOS DADOS DE MANCHAS SOLARES (SILSO)
# -----------------------------------------------------------------------------
print("Baixando dados de manchas solares...")
sunspot_url = "https://sidc.be"

# O arquivo do SILSO usa ponto e vírgula como separador e não tem cabeçalho
# Colunas: Ano, Mês, Data em fração de ano, Média Mensal, Desvio Padrão, Número de observações, Indicador
sunspot_df = pd.read_csv(sunspot_url, sep=';', header=None, usecols=[0, 1, 3], names=['Ano', 'Mes', 'Manchas'])

# Criar coluna de data
sunspot_df['Data'] = pd.to_datetime(sunspot_df[['Ano', 'Mes']].assign(Day=1))
sunspot_df = sunspot_df.set_index('Data')[['Manchas']]

# -----------------------------------------------------------------------------
# 2. DOWNLOAD E TRATAMENTO DOS DADOS DO EL NIÑO (NOAA - ONI)
# -----------------------------------------------------------------------------
print("Baixando dados do Oceanic Niño Index (ONI)...")
oni_url = "https://noaa.gov"

# O arquivo da NOAA é delimitado por espaços em branco fixos
oni_df = pd.read_csv(oni_url, sep=r'\s+', header=0)

# Mapear as estações de 3 meses (ex: DJF, JFM) para o mês central (ex: Janeiro, Fevereiro)
# O ONI usa blocos móveis. Vamos aproximar para o mês correspondente da linha
oni_df['Mes'] = ((oni_df.index) % 12) + 1

# Renomear colunas do arquivo original (geralmente SEAS, YR, TOTAL, ANOM)
# Queremos a coluna de anomalia (ANOM), que define o El Niño/La Niña
oni_df.columns = ['SEAS', 'Ano', 'Total', 'ONI_Anomalia', 'Mes']
oni_df['Data'] = pd.to_datetime(oni_df[['Ano', 'Mes']].assign(Day=1))
oni_df = oni_df.set_index('Data')[['ONI_Anomalia']]

# -----------------------------------------------------------------------------
# 3. ALINHAMENTO DAS SÉRIES TEMPORAIS
# -----------------------------------------------------------------------------
# Unir os datasets pela data correspondente (interseção automática do período)
dados_combinados = sunspot_df.join(oni_df, how='inner')

# Normalizar os dados (Z-score) para que fiquem na mesma escala gráfica
dados_norm = (dados_combinados - dados_combinados.mean()) / dados_combinados.std()

print(f"Período analisado: de {dados_combinados.index.min().strftime('%m/%Y')} até {dados_combinados.index.max().strftime('%m/%Y')}")

# -----------------------------------------------------------------------------
# 4. CÁLCULO DA CORRELAÇÃO CRUZADA (CROSS-CORRELATION)
# -----------------------------------------------------------------------------
def calcular_cross_corr(series1, series2, max_lag=60):
    """Calcula a correlação de Pearson para diferentes lags (meses)"""
    lags = np.arange(-max_lag, max_lag + 1)
    correlacoes = []
    
    for lag in lags:
        if lag < 0:
            # Series 1 (Sol) antecede Series 2 (El Niño)
            c = series1.iloc[:lag].corr(series2.shift(lag).dropna())
        elif lag > 0:
            # Series 1 (Sol) sucede Series 2 (El Niño)
            c = series1.shift(lag).dropna().corr(series2.iloc[lag:])
        else:
            c = series1.corr(series2)
        correlacoes.append(c)
        
    return lags, correlacoes

# Consideramos um atraso de até 60 meses (5 anos) para avaliar ciclos longos
lags, corrs = calcular_cross_corr(dados_combinados['Manchas'], dados_combinados['ONI_Anomalia'], max_lag=60)

# -----------------------------------------------------------------------------
# 5. VISUALIZAÇÃO DOS GRÁFICOS
# -----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# Gráfico 1: Linha do Tempo Comparativa (Dados Normalizados)
ax1.plot(dados_norm.index, dados_norm['Manchas'], label='Manchas Solares (SILSO)', color='orange', alpha=0.7)
ax1.plot(dados_norm.index, dados_norm['ONI_Anomalia'], label='Oceanic Niño Index (NOAA)', color='blue', alpha=0.6)
ax1.set_title('Histórico Comparativo: Atividade Solar vs. El Niño (Normalizados)')
ax1.set_xlabel('Ano')
ax1.set_ylabel('Desvios Padrão (Z-Score)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.5)

# Gráfico 2: Correlação Cruzada
ax2.bar(lags, corrs, color='purple', width=0.6, alpha=0.8)
ax2.axhline(0, color='black', linewidth=0.8)
# Linhas de significância estatística aproximada (95% de confiança)
conf_lim = 1.96 / np.sqrt(len(dados_combinados))
ax2.axhline(conf_lim, color='red', linestyle='--', alpha=0.7, label='Significância 95%')
ax2.axhline(-conf_lim, color='red', linestyle='--', alpha=0.7)

ax2.set_title('Correlação Cruzada entre Manchas Solares e ONI')
ax2.set_xlabel('Lag em Meses (Valores negativos = Sol antecede o El Niño)')
ax2.set_ylabel('Coeficiente de Correlação de Pearson')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()