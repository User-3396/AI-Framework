# Clima Espacial (Sol-Terra)

### Variables Originadas no Sol (Condições Solar e Interplanetária)
Estas variáveis descrevem a matéria e a energia que o Sol ejetou e que estão cruzando o espaço em direção ao nosso planeta. Elas são coletadas por satélites no ponto Lagrangiano L1 (a cerca de 1,5 milhão de km da Terra).

- __Velocidade do Vento Solar (Solar Wind Speed)__: Mede a rapidez com que o plasma viaja. O vento normal sopra entre 300 e 500 km/s. Quando uma ejeção de massa coronal (CME) ou um buraco coronal atinge o sensor, essa velocidade pode passar de 800 km/s, empurrando o campo magnético da Terra com força.
- __Densidade de Prótons (Proton Density)__: Mede a quantidade de partículas (plasma) por centímetro cúbico. Um número alto (acima de 20-30 p/cm³) significa que o vento solar está "denso" e pesado, aumentando a pressão do impacto na nossa magnetosfera.
- __Temperatura do Vento Solar (Temperature)__: Mede a energia térmica cinética das partículas gasosas do vento solar. Flutuações drásticas indicam frentes de choque de tempestades solares.
- __Campo Magnético Interplanetário / Vetor $B_z$ (_IMF /_ $B_z$ _Component_)__: O vento solar carrega o magnetismo do Sol pelo espaço. O vetor $B_z$ aponta a direção norte ou sul desse campo. Se o $B_z$ estiver negativo (apontando para o Sul), ele se conecta perfeitamente ao campo magnético da Terra (que aponta para o Norte), abrindo as portas para a entrada de energia solar e gerando as tempestades geomagnéticas.
- __Fluxo de Prótons Solares (Solar Proton Flux / SEPs)__: Mede prótons de altíssima energia acelerados por explosões solares. Quando esse fluxo atinge níveis críticos, causa tempestades de radiação solar (Escala S da NOAA), ameaçando astronautas e satélites.

### Variáveis Medidas e Sentidas na Terra

Estas variáveis descrevem a reação do ambiente terrestre ao bombardeio do vento solar. Elas monitoram a magnetosfera, a ionosfera e as correntes elétricas no solo.

- __F10.7 Index (Fluxo de Rádio de 10,7 cm)__: Embora seja uma emissão do Sol, ele é medido por antenas na Terra e serve para estimar o nível de ionização da nossa alta atmosfera. Quanto maior o F10.7, mais densa fica a ionosfera terrestre, alterando a órbita de satélites baixos devido ao arrasto atmosférico.
- __Índice Dst (Disturbance Storm Time)__: Mede a intensidade da corrente elétrica de anel que circula ao redor da Terra no espaço. Valores normais ficam perto de zero. Valores muito negativos (ex: -100 nT a -400 nT) indicam que a Terra está passando por uma severa tempestade geomagnética global.
- __Índice AE (Auroral Electrojet)__: Mede a atividade elétrica especificamente nas regiões dos polos (zonas aurorais). Ele indica a intensidade das correntes que geram as auroras boreais e austrais.
- __TEC (Total Electron Content)__: Mede a quantidade total de elétrons livres na ionosfera da Terra. Variações bruscas no TEC distorcem diretamente os sinais que cruzam a atmosfera, gerando os temidos erros de precisão no GPS.

[fonte 1.1](https://www.ncei.noaa.gov/products/geomagnetic-indices) [fonte 1.2. trad](https://www.google.com/url?sa=t&source=web&rct=j&url=https%3A%2F%2Ftranslate.google.com%2Ftranslate%3Fu%3Dhttps%3A%2F%2Fwww.ncei.noaa.gov%2Fproducts%2Fgeomagnetic-indices%26hl%3Dpt%26sl%3Den%26tl%3Dpt%26client%3Dsge&ved=0CAEQ1fkOahgKEwiwn4bGnreVAxUAAAAAHQAAAAAQhwE&opi=89978449)

### 1. Dados Geomagnéticos Afetados pelo Sol

Quando ocorrem ejeções de massa coronal ou ventos solares rápidos, a magnetosfera terrestre sofre compressões e indução de correntes elétricas. Esse impacto é medido principalmente por três vertentes de dados:

__Índices de Perturbação Global__ 

- __Índice Kp (Planetary K-index)__: Mede desvios no campo magnético da Terra em intervalos de 3 horas. Varia em uma escala quase logarítmica de 0 a 9. Valores acima de 5 indicam tempestades geomagnéticas.
- __Índice Dst (Disturbance Storm-Time)__: Mede a intensidade da corrente de anel equatorial da Terra (expressa em nanoTeslas - nT). Valores muito negativos (ex: -100 nT ou menos) apontam para uma tempestade severa em andamento.
- __Índice AE (Auroral Electrojet)__: Monitora a atividade magnética nas regiões polares (aurorais), ideal para estudar correntes de jato na ionosfera.

__Dados de Vento Solar (Causa Direta)__ 

- __Campo Magnético Interplanetário (\(B_{z}\))__: O vetor \(B_{z}\) mede a orientação norte-sul do campo magnético solar. Se o \(B_{z}\) apontar fortemente para o sul (negativo), ele se conecta facilmente ao campo magnético da Terra, despejando energia na atmosfera.
- __Velocidade e Densidade do Plasma__: A velocidade do vento solar (geralmente medida em km/s) e a densidade de prótons/elétrons indicam a pressão dinâmica exercida contra a Terra.


### 2. APIs para Análise Temporal (Prontas para o Jupyter Notebook)

Existem repositórios internacionais oficiais que expõem esses dados em formatos estruturados como JSON ou CSV, perfeitos para criar DataFrames no pandas.

__Opcão A: API do NOAA SWPC (Dados em Tempo Real e Recentes)__

O _Space Weather Prediction Center_ (SWPC) da NOAA fornece endpoints diretos em JSON sem necessidade de criar chaves de autenticação (tokens).

- __Endpoint do Índice Kp dos últimos dias__: `https://noaa.gov` 
- __Endpoint do Vento Solar em tempo real (dados de satélites como DSCOVR)__: `https://noaa.gov` (Plasma), `https://noaa.gov` (Campo magnético / \(B_{z}\))

__Opção B: API de Web Services do GFZ Potsdam (Séries Temporais Longas)__ 

O Centro Alemão de Geociências (GFZ) é a instituição oficial responsável por calcular o índice Kp histórico. Eles possuem uma API pública excelente para extrair séries temporais longas de dados em formatos amigáveis (como JSON ou texto formatado).

- __Endpoint da API (Exemplo para obter Kp)__: `https://gfz-potsdam.de`

### 3. Exemplo Prático de Código no Jupyter

Você pode usar o pacote especializado Python [geomagindices](https://pypi.org/project/geomagindices/) que automatiza o download dessas séries temporais e as converte diretamente em tabelas estruturadas:

```python
# Instala a biblioteca silenciosamente se necessário
%pip install geomagindices pandas matplotlib -q

import datetime
import geomagindices as gi

# Define o período temporal da análise
data_inicio = datetime.datetime(2025, 1, 1)
data_fim = datetime.datetime(2025, 1, 10)

# A API da biblioteca busca os dados históricos automaticamente
df = gi.get_indices([data_inicio, data_fim])

# Exibe o DataFrame resultante para análise temporal (contendo Kp, Ap, F10.7)
df.head()
```

Se preferir consumir a API da NOAA manualmente via HTTP para obter dados em tempo real, use a estrutura padrão:

```python
import pandas as pd
import requests

url = "https://noaa.gov"
resposta = requests.get(url).json()

# O NOAA envia os dados com os cabeçalhos na primeira linha
colunas = resposta[0]
dados = resposta[1:]

df_bz = pd.DataFrame(dados, columns=colunas)
df_bz['time_tag'] = pd.to_datetime(df_bz['time_tag'])
df_bz['bz'] = pd.to_numeric(df_bz['bz'])

# Agora você pode plotar a variação temporal do Bz
df_bz.plot(x='time_tag', y='bz', title="Análise Temporal de Bz (Campo Magnético Solar)")
```

## Escalas: 

- __Escala R__ (Radio Blackouts ou Apagões de Rádio): Enquanto os canais XRSA e XRSB medem a energia que sai do Sol, a Escala R traduz o impacto físico real gerado na ionosfera da Terra.
- __Escala S (Solar Radiation Storms)__: Mede o impacto de prótons energéticos que atingem os polos magnéticos da Terra. Avalia o risco de radiação para astronautas, passageiros de aviões em altas altitudes e falhas eletrônicas em satélites.
- __Escala G (Geomagnetic Storms)__: Mede o impacto das Ejeções de Massa Coronal (CME) na Magnetosfera da Terra. É calculada usando o Índice Kp (que vai de 0 a 9). Mostra a força de tempestades geomagnéticas capazes de induzir correntes elétricas em redes de energia (causando apagões na Terra) e criar auroras polares.

