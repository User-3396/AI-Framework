## Topics
- `Sunspot` (Mancha Solar)
- `CME (Coronal Mass Ejection)`
- `Geomagnetic/Radiation Storms`

## 1. Dados de Atividade Solar (Séries Temporais)

- ### SILSO (Sunspot Index and Long-term Solar Observations)
> - __O que contém__: Dados históricos de contagem de manchas solares (Sunspot Number), o indicador mais clássico de atividade solar.
> - __Resolução__: Diária, mensal e anual.
> - __Janela de Tempo__: Desde 1700 até o presente.
> - __Por que usar__: É o dataset mais longo disponível, ideal para correlações de longo prazo (séculos) com o clima.

### LASP Interactive Solar Irradiance Data Center (LISIRD) 
> - __O que contém__: Dados de Irradiância Solar Total (TSI) e Irradiância Solar Espectral (SSI). Mede a quantidade real de energia que chega à Terra.
> - __Resolução__: Diária ou mensal.
> - __Janela de Tempo__: Dados compostos desde 1978 (era dos satélites) e reconstruções históricas que voltam até 1610.

### NOAA Space Weather Prediction Center (SWPC)
> - __O que contém__: Índices geomagnéticos (como o índice \(Kp\) ou \(Ap\)) e fluxo de rádio solar (F10.7 cm).
> - __Resolução__: Horária e diária.
> - __Janela de Tempo__: Décadas recentes até o presente.
> - __Por que usar__: Excelente para analisar o impacto de tempestades solares de curto prazo na atmosfera terrestre.

## 2.1 Dados Climáticos da Terra (Alinhados no Tempo)
Para bater com as datas dos dados solares, você deve usar anomalias globais estruturadas:

### HadCRUT5 (Hadley Centre/UEA)
> - __O que contém__: Anomalias de temperatura da superfície global (terra e oceanos).
> - __Resolução__: Mensal.
> - __Janela de Tempo__: Desde 1850 até o presente.
> - __Vantagem__: Cruza perfeitamente com a série histórica de manchas solares do SILSO para estudar o impacto no aquecimento/resfriamento global.

### CO2 e Gases Estufa (Keeling Curve / NOAA)
> - __O que contém__: Concentração de dióxido de carbono na atmosfera.
> - __Resolução__: Mensal e anual desde 1958.
> - __Vantagem__: Essencial como variável de controle na sua correlação. Para provar a influência solar, você precisará isolar o efeito dos gases estufa usando correlação parcial ou modelos de regressão múltipla.

## 2.2 Outros Dados compatíveis para correlação com atividade solar

> - __Geomagnetismo__: _Dst Index / Kp Index (NOAA, Kyoto WDC)_ - Distúrbios geomagnéticos;
> - __Ionosfera__: _Ionospheric TEC (Total Electron Content) – NASA, ESA_ - Conteúdo eletrônico na ionosfera;
> - __Clima Espacial__: _Auroral Electrojet Index (AE) – NOAA_ - 
> - __Atmosfera terrestre__: [_Rede SONDA (INPE/LABREN)_](https://sonda.ccst.inpe.br) - 
> - __Energia solar e UV__: [_NOAA UV Index & Ozone Data_](https://www.ngdc.noaa.gov/stp/solar) - 
> - __Eventos extremos__: _Global Flood Database (NASA)_ - enchentes globais


# Refferences

- https://opendataset.info/category/climate
- https://wmo.int/publication-series/state-of-global-climate
