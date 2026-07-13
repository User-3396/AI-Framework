### Principais Vulcões em Atividade

__1. Kīlauea (Havaí, Estados Unidos)__

Localizado nas ilhas do Havaí, este é um dos vulcões mais ativos e estudados do mundo. Ele entra em erupção frequentemente, atraindo visitantes devido aos seus rios e fluxos de lava visíveis.

__2. Etna (Sicília, Itália)__ 

Situado na ilha da Sicília, é o vulcão mais alto e ativo de toda a Europa. Suas erupções são frequentes e frequentemente iluminam o céu noturno com ejeções de lava.

__3. Merapi (Java, Indonésia)__ 

Localizado na Indonésia — um dos países com maior atividade vulcânica do mundo —, o Merapi é conhecido por ser extremamente ativo e perigoso, com erupções frequentes que ameaçam áreas densamente povoadas.

__4. Villarrica (Região da Araucanía, Chile)__ 

Um dos vulcões mais ativos da América do Sul. Ele possui um lago de lava quase constante em sua cratera e é uma referência importante de monitoramento e turismo na Cordilheira dos Andes.

__5. Nyiragongo (República Democrática do Congo)__ 

Famoso por abrigar o maior lago de lava fluido da Terra. Ele é considerado um dos vulcões mais perigosos da África devido à composição química da sua lava, que pode escorrer rapidamente e ameaçar a cidade de Goma.

__6. Sakurajima (Kyushu, Japão)__ 

Outro gigante situado no Anel de Fogo, o Sakurajima registra pequenas erupções quase diárias, gerando plumas de fumaça e cinzas constantes na região.

### Atividades no maximo solar (do Ciclo Solar 25, de 2024 a 2026)

- __Kīlauea (EUA)__: Entrou em uma fase eruptiva histórica e frenética iniciada em dezembro de 2024. Até meados de 2026, bateu recordes com dezenas de episódios consecutivos de fontes e rios de lava na cratera Halemaʻumaʻu.
- __Etna (Itália)__: Manteve seu comportamento altamente dinâmico ao longo de 2024, 2025 e 2026, expelindo colunas de cinzas e fluxos de lava visíveis a quilômetros de distância.
- __Merapi e Semeru (Indonésia)__: A Indonésia registrou intensa atividade. O Semeru permaneceu em erupção contínua e explosiva durante todo o período de 2024 a 2026, enquanto o Merapi seguiu gerando fluxos piroclásticos perigosos.
- __Vulcões da Islândia (Península de Reykjanes)__: Protagonizaram uma das séries de erupções mais famosas desse período. Desde o fim de 2023, cruzando todo o ano de 2024 e 2025, o sistema islandês abriu fissuras colossais, expelindo milhões de metros cúbicos de magma e modificando a geografia local.
- __Villarrica (Chile)__: Registrou recorrentes alertas e atividade interna instável com emissão de gases e incandescência noturna na Cordilheira dos Andes.
- __Sangay (Equador) e Manam (Papua Nova Guiné)__: Mantiveram erupções ininterruptas de caráter altamente explosivo e efusivo entre 2024 e 2026.

### Exemplo de junção com atividades solares: 

```python
import pandas as pd
import sunpy.timeseries
import matplotlib.pyplot as plt

# 1. BAIXAR DADOS DE MANCHAS SOLARES (SUNPY/NOAA)
noaa_url = "https://noaa.gov"
ts_sunspot = sunpy.timeseries.TimeSeries(noaa_url, source='NOAAIndices')

# Converter para DataFrame do Pandas e isolar a coluna de manchas (ssn)
df_solar = ts_sunspot.to_dataframe()
df_solar = df_solar[['ssn']].dropna()
# Garantir que o índice seja do tipo Datetime (padrão SunPy é mensal)
df_solar.index = pd.to_datetime(df_solar.index).to_period('M').to_timestamp()

# 2. SIMULAR / CARREGAR DADOS VULCÂNICOS
# Nota: Substitua esta simulação pelo seu arquivo real de erupções (ex: df_volcano = pd.read_csv('volcano.csv'))
datas_vulcões = pd.date_range(start=df_solar.index.min(), end=df_solar.index.max(), freq='ME')
import numpy as np
np.random.seed(42)
erupcoes_simuladas = np.random.poisson(lam=3, size=len(datas_vulcões)) # Média de 3 erupções/mês

df_volcano = pd.DataFrame({'erupcoes': erupcoes_simuladas}, index=datas_vulcões)

# 3. JUNTAR OS DATAFRAMES (PELA DATA)
df_comparativo = df_solar.join(df_volcano, how='inner')

# 4. CONFIGURAR A JANELA DESLIZANTE (Escolha o tamanho aqui)
# Exemplo: Janela móvel de 12 meses (1 ano) calculando a média
tamanho_janela = 12 

df_comparativo['solar_suavizado'] = df_comparativo['ssn'].rolling(window=tamanho_janela, center=True).mean()
df_comparativo['vulcões_suavizado'] = df_comparativo['erupcoes'].rolling(window=tamanho_janela, center=True).mean()

# 5. PLOTAR O COMPARATIVO COM DOIS EIXOS Y
fig, ax1 = plt.subplots(figsize=(12, 6))

# Eixo esquerdo: Manchas Solares
color = 'tab:orange'
ax1.set_xlabel('Ano')
ax1.set_ylabel('Nº de Manchas Solares (Média Móvel)', color=color)
ax1.plot(df_comparativo.index, df_comparativo['solar_suavizado'], color=color, linewidth=2, label='Solar')
ax1.tick_params(axis='y', labelcolor=color)

# Eixo direito: Atividade Vulcânica
ax2 = ax1.twinx()  
color = 'tab:red'
ax2.set_ylabel('Nº de Erupções (Média Móvel)', color=color)
ax2.plot(df_comparativo.index, df_comparativo['vulcões_suavizado'], color=color, linewidth=2, linestyle='--', label='Vulcões')
ax2.tick_params(axis='y', labelcolor=color)

plt.title(f"Comparativo: Atividade Solar vs Vulcânica (Janela Móvel de {tamanho_janela} meses)")
fig.tight_layout()
plt.show()

```
