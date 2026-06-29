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
