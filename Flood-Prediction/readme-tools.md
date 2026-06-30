# SpacePy [1](https://spacepy.github.io/index.html)
extension://bfdogplmndidlpjfhoijckpakkdjkkil/pdf/viewer.html?file=https%3A%2F%2Fscispace.com%2Fpdf%2Fspacepy-a-python-based-library-of-tools-for-the-space-564174mvu9.pdf 

## Para que ela serve?

O pacote resolve os problemas mais comuns enfrentados por cientistas espaciais, dividindo-se em ferramentas principais:

- __Manipulação de Dados Espaciais__: Permite ler, criar e converter formatos de arquivos padrão da NASA e da ESA, como os arquivos __CDF__ (_Common Data Format_) [2] e __HDF5__, usados em missões de satélites.
- __Modelos de Campo Magnético__: Inclui rotinas para calcular e mapear campos magnéticos planetários, além de conectar com modelos clássicos (como o modelo de Tsyganenko).
- __Coordenadas Espaciais__: Facilita a conversão ultraprecisa entre sistemas de coordenadas geocêntricas e geomagnéticas (como GEO, GSM, GSE e SM), essenciais para localizar satélites na magnetosfera.
- __Índices Geomagnéticos__ (`spacepy.toolbox.sw`): Faz o download e o tratamento automático de dados ambientais históricos e em tempo real, como os índices __Kp__, __Ap__, __Dst__ e __AE__, que medem a intensidade de tempestades solares na Terra.
- __Física de Cinturões de Radiação__: Possui ferramentas específicas para estudar os Cinturões de Van Allen e a difusão de partículas carregadas.

## Correlação Sol-Terra:

_Para usar recursos avançados de leitura de arquivos de satélite (`spacepy.pycdf`), o Colab precisará do pacote da NASA chamado CDF Library, que exige uma instalação de sistema adicional via apt-get se for necessário._

### 1. Cruzamento Imediato de Causa e Efeito

O Sol leva de 1 a 3 dias para enviar o plasma de uma tempestade até a Terra. 
Com o módulo spacepy.toolbox.sw, você puxa instantaneamente o histórico de índices como Kp (distúrbio planetário) e Dst (intensidade da corrente de anel na magnetosfera). 
Você pode cruzar o momento exato em que um satélite na órbita da Terra detectou o choque com os impactos em solo (ex: correntes induzidas em redes elétricas).

### 2. Alinhamento de Satélites (Conversão de Coordenadas)

Para saber se o satélite que mediu a tempestade solar estava de fato "de frente" para o Sol ou protegido atrás da Terra, você precisa de coordenadas como GSM ou GSE. 
Fazer essa matemática manualmente envolve matrizes de rotação complexas baseadas na hora e no dia do ano. O módulo `spacepy.coordinates` faz isso em uma linha:

```python
# Converte a posição do satélite de Geográfica para Geocêntrica Solar Magnetosférica (GSM)
coordenadas_gsm = spacepy.coordinates.Coords([[x, y, z]], 'GEO', 'car').convert('GSM', 'car')

```

### 3. Acesso Direto aos Dados Brutos de Satélites (CDF)

A imensa maioria das missões da NASA/ESA (como as sondas ACE, WIND, SOHO e Van Allen Probes) que monitoram o vento solar disponibiliza os dados brutos em arquivos .cdf. 
A SpacePy possui o melhor leitor Python para esse formato (`spacepy.pycdf`), permitindo que você extraia densidade, velocidade e temperatura do vento solar direto dos repositórios científicos para o seu DataFrame.

### 4. Modelagem da Magnetosfera

Se o seu estudo avalia se a tempestade solar conseguiu "comprimir" a defesa magnética da Terra a ponto de expor satélites de órbita geoestacionária, o módulo `spacepy.irbempy` permite calcular a posição da magnetopausa e mapear as linhas de campo magnético terrestre sob o estresse do vento solar.

# spacepy.toolbox e spacepy.omni - Sol -> Índices geomagnéticos

```python
import pandas as pd
import numpy as np
import spacepy.toolbox as tb
import spacepy.omni as omni

# 1. Sincronizar e atualizar a base de dados OMNI (Vento Solar + Índices da Terra)
# Nota: Isso baixa os dados estruturados da NASA para o seu computador
print("Atualizando base OMNI... Pode levar alguns minutos no primeiro uso.")
tb.update(omni=True)

# 2. Carregar um intervalo de tempo para treino/teste (Ex: anos de 2021 a 2023)
# O Omni ticks cria o vetor de tempo correto
ticks = omni.get_omni_ticks([2021, 2023])
data = omni.get_omni(ticks)

# 3. Criar o DataFrame base com as variáveis críticas de L1 e da Terra
df = pd.DataFrame({
    'Bz_IMF': data['BzIMF'],      # Campo Magnético Interplanetário Z (crítico para acoplamento)
    'V_sw': data['Velocity'],     # Velocidade do vento solar (km/s)
    'N_sw': data['Density'],      # Densidade do vento solar (N/cm³)
    'T_sw': data['Temperature'],  # Temperatura do plasma
    'Kp': data['Kp']              # Target Terrestre: Índice de atividade geomagnética (0 a 9)
}, index=pd.to_datetime(data['UTC']))

# Limpar flags de dados ausentes comuns em dados espaciais (ex: 999.9 ou 9999)
df = df.replace([999.9, 9999.0, 99.9], np.nan).ffill()

# 4. Engenharia de Features (Feature Engineering para Séries Temporais)
# Criando janelas históricas (Lags) dos dados solares para o modelo entender a tendência
passos_historicos = 3  # Olhar 3 horas para o passado

for i in range(1, passos_historicos + 1):
    df[f'Bz_IMF_lag_{i}'] = df['Bz_IMF'].shift(i)
    df[f'V_sw_lag_{i}'] = df['V_sw'].shift(i)
    df[f'N_sw_lag_{i}'] = df['N_sw'].shift(i)

# Criando estatísticas móveis do vento solar (Últimas 6 horas)
df['Bz_mean_6h'] = df['Bz_IMF'].rolling(window=6).mean()
df['V_sw_std_6h'] = df['V_sw'].rolling(window=6).std()

# 5. Definir o Target Preditivo (Janela para o Futuro)
# Exemplo: Prever o Kp da Terra com 1 hora de antecedência (t+1)
df['Target_Kp_Futuro'] = df['Kp'].shift(-1)

# Remover linhas com valores NaN gerados pelos shifts e rollings
df_ml = df.dropna()

# Visualizar o DataFrame pronto para os algoritmos de ML (Scikit-Learn, XGBoost, etc.)
print("\nDataFrame pronto para Machine Learning:")
print(df_ml.head())
```

### Por que essa estrutura funciona para Modelos Preditivos?

- __Janela de Input (X)__: Ao usar `shift(1)`, `shift(2)`, você garante que o modelo (como um XGBoost, Random Forest ou rede LSTM) receba a assinatura temporal de como o vento solar estava evoluindo antes do impacto.
- __Alvo Antecipado (y)__: O `shift(-1)` joga o dado terrestre para o "passado" da linha atual. Na prática, o modelo usará os dados de vento solar de agora para adivinhar o Kp de daqui a 1 hora.
- __Dados Omni limpos__: O `spacepy.omni` já traz os dados interpolados e ajustados considerando o tempo de viagem do ponto L1 até o topo da atmosfera magnética da Terra (o chamado _bow shock_).

## Usando __XGBoost__, __Random Forest__ ou __Regressão Logística__

```python
from sklearn.ensemble import RandomForestClassifier

# Treinar o classificador
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Em vez de prever 0 ou 1, prevemos as probabilidades
# [:, 1] extrai a probabilidade da classe 1 (Ocorrência da Tempestade)
probabilidades = modelo.predict_proba(X_test)[:, 1]

# 'probabilidades' agora será uma lista de valores entre 0.0 e 1.0
print(probabilidades[:5]) 
# Saída visual: [0.12, 0.85, 0.43, 0.91, 0.05]
```

1. __Criar um Target Binário__: Transformar o índice contínuo Kp em `1` (haverá tempestade, ex: Kp \(\ge \) 5) ou `0` (não haverá tempestade, Kp < 5).
2. __Treinar o Modelo com Saída Probabilística__: Usar um algoritmo de classificação e extrair a previsão com o método `.predict_proba()`.

```python
import pandas as pd
import numpy as np
import spacepy.toolbox as tb
import spacepy.omni as omni
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss

# ==========================================
# 1. ATUALIZAÇÃO E CARREGAMENTO DOS DADOS
# ==========================================
print("Sincronizando base OMNI via SpacePy...")
tb.update(omni=True)

ticks = omni.get_omni_ticks()
data = omni.get_omni(ticks)

# Criar DataFrame base
df = pd.DataFrame({
    'Bz_IMF': data['BzIMF'],      # Campo magnético solar Z
    'V_sw': data['Velocity'],     # Velocidade do vento solar
    'N_sw': data['Density'],      # Densidade do vento solar
    'Kp': data['Kp']              # Índice geofísico terrestre
}, index=pd.to_datetime(data['UTC']))

# Limpar dados ausentes (comum em física espacial)
df = df.replace([999.9, 9999.0, 99.9], np.nan).ffill()

# ==========================================
# 2. ENGENHARIA DE FEATURES (PASSADO -> HISTÓRICO)
# ==========================================
# Criar atrasos temporais (lags) de 1 e 2 horas para o vento solar
for i in:
    df[f'Bz_IMF_lag_{i}'] = df['Bz_IMF'].shift(i)
    df[f'V_sw_lag_{i}'] = df['V_sw'].shift(i)
    df[f'N_sw_lag_{i}'] = df['N_sw'].shift(i)

# ==========================================
# 3. DEFINIÇÃO DO TARGET BINÁRIO (FUTURO)
# ==========================================
# Definir o alvo para daqui a 1 hora (shift -1)
df['Kp_Futuro'] = df['Kp'].shift(-1)

# Aplicar o limiar: Kp >= 5 significa Tempestade Geomagnética (True/1, False/0)
df['Tempestade_Alvo'] = (df['Kp_Futuro'] >= 5).astype(int)

# Limpar linhas com NaNs gerados pelos shifts
df_ml = df.dropna()

# ==========================================
# 4. DIVISÃO DE TREINO E TESTE
# ==========================================
# Features (X) e rótulo (y)
features = ['Bz_IMF', 'V_sw', 'N_sw', 
            'Bz_IMF_lag_1', 'V_sw_lag_1', 'N_sw_lag_1',
            'Bz_IMF_lag_2', 'V_sw_lag_2', 'N_sw_lag_2']

X = df_ml[features]
y = df_ml['Tempestade_Alvo']

# Divisão temporal ou aleatória (usando aleatória para simplificar o exemplo)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_test_split=42)

# ==========================================
# 5. TREINAMENTO DO MODELO PROBABILÍSTICO
# ==========================================
print("\nTreinando o classificador probabilístico...")
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# EXTRAÇÃO DAS PROBABILIDADES (0.0 a 1.0)
# [:, 1] pega apenas a probabilidade da classe 1 (Ocorrência da tempestade)
probabilidades = modelo.predict_proba(X_test)[:, 1]

# ==========================================
# 6. AVALIAÇÃO DO DESEMPENHO PROBABILÍSTICO
# ==========================================
auc = roc_auc_score(y_test, probabilidades)
brier = brier_score_loss(y_test, probabilidades)

print(f"\n--- Resultados da Validação ---")
print(f"ROC-AUC Score: {auc:.4f} (Mede a capacidade de separação do modelo, ideal próximo de 1.0)")
print(f"Brier Score: {brier:.4f} (Mede a calibração da porcentagem, ideal próximo de 0.0)")

# Exibir exemplos práticos das previsões contínuas obtidas
df_resultado = pd.DataFrame({
    'Realidade (Ocorreu?)': y_test.values,
    'Probabilidade Prevista (0.0 a 1.0)': probabilidades
})
print("\nAmostra de Previsões Realizadas:")
print(df_resultado.head(10))

```

## Sol -> Terremotos

Cientificamente, o assunto é altamente controverso: a comunidade sismológica majoritária descarta uma relação direta causal, enquanto alguns grupos minoritários pesquisam mecanismos de acoplamento eletromagnético na crosta terrestre.
Abaixo estão as mudanças práticas estruturais que você precisará aplicar no seu pipeline de Machine Learning:

### 1. Mudança Drástica no Target (Variável `y`)

O índice Kp (magnetismo) deixa de ser o seu foco. Você precisará conectar seu script a um banco de dados sismológico global, como o do __USGS (Serviço Geológico dos EUA)__.

- __Nova API / Dados__: Em vez de ler apenas o SpacePy, você usará bibliotecas como a obspy ou requisições HTTP na API do USGS para extrair latitude, longitude, magnitude e tempo exato de terremotos.
- __Definição de Incidente__: Você precisará criar uma máscara binária baseada na magnitude (Ex: `Magnitude >= 6.0`) ou na contagem diária global de sismos de grande porte.

### 2. Ajuste na Engenharia de Janelas Temporais (Lags)

Diferente das tempestades magnéticas que levam minutos ou poucas horas para responder ao vento solar, as teorias que tentam correlacionar Sol e terremotos trabalham com atrasos muito maiores.

- __Janelas longas__: Suas features de vento solar (`Bz`, `Velocidade`, `Densidade`) e de fluxo de prótons solares precisarão de lags acumulados de 24 horas, 48 horas ou até 7 dias antes do evento sismológico acontecer.

### 3. Inclusão de Dados de Linhas de Corrente Telúricas

Pesquisadores que buscam essa correlação defendem que a energia magnética solar induz correntes elétricas no solo (correntes telúricas), que por sua vez poderiam afetar falhas geológicas ativas pelo efeito piezoelétrico.

- Para o modelo ter algum sentido físico, além dos dados solares do SpacePy, você precisará adicionar dados de __Magnetômetros de Solo__ (disponíveis na rede INTERMAGNET) próximos às falhas geológicas estudadas.

### 4. O Desafio do Desbalanceamento Extremo (_Data Imbalance_)

Se prever tempestades solares já exige lidar com dados desbalanceados, prever grandes terremotos é ordens de magnitude mais difícil:

- Terremotos severos (Magnitude ≥ 6) são eventos estatisticamente muito raros. Seu target terá 99,99% de zeros e 0,01% de uns. Modelos de Machine Learning tendem a simplesmente "chutar" zero o tempo todo para obter alta acurácia. Técnicas severas de balanceamento (como SMOTE ou penalização de pesos de classe) serão obrigatórias.

Ex: 

```python
# Como ficaria a junção teórica no seu DataFrame
df_sismico = pd.DataFrame({
    'Vento_Solar_Vel': data_omni['Velocity'], # Causa proposta
    'Fluxo_Protons': data_omni['Fluxo'],       # Causa proposta
    'Terremoto_Ocorreu': [0, 0, 1, 0, 0]       # Novo Target (Dados do USGS)
})
```
