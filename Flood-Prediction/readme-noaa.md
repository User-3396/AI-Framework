## 1. Satélites GOES (Geostationary Operational Environmental Satellite)

- __O que monitoram__: Explosões solares (Solar Flares), fluxo de Raios-X, Prótons, Elétrons e o campo magnético da Terra.
- __Identificação no JSON/URL__: Geralmente identificados por números (ex: `goes-16`, `goes-18`, `goes-19`).
- __Uso prático__: Se você quer saber se uma erupção solar acabou de acontecer, você consome dados do satélite GOES que estiver posicionado como "GOES-Primary" ou "GOES-Secondary".

### Satélite DSCOVR (Deep Space Climate Observatory)

- __O que monitora__: Vento Solar em tempo real (velocidade, densidade, temperatura) e o Campo Magnético Interplanetário (IMF). Ele fica posicionado no ponto de gravidade L1, entre o Sol e a Terra.
- __Identificação no JSON/URL__: As URLs contêm dscovr ou termos de vento solar como mag-5-minute e plasma-5-minute.
- __Uso prático__: Essencial para prever Auroras Boreais e tempestades geomagnéticas com cerca de 30 a 60 minutos de antecedência.

## 2. Entendendo os Parâmetros das Requisições

No repositório público da NOAA (`services.swpc.noaa.gov/json/`), a filtragem por parâmetros rígidos na URL (como `?start=...`) é limitada se comparada à API de terremotos do USGS. No entanto, o nível de detalhe e os intervalos de tempo são controlados de duas formas fundamentais:

### A. Parâmetro de Intervalo de Tempo (Construído no nome do arquivo)

A NOAA separa os arquivos JSON pelo intervalo de amostragem e pela duração do histórico. Você escolhe o nível de detalhe modificando o sufixo do arquivo na requisição:

- __Dados brutos/Imediatos (Alta resolução, curto prazo)__: Geralmente atualizados a cada 1 minuto, contendo apenas as últimas 24 horas.
  - Exemplo: `xray-1-day.json` (Dados detalhados minuto a minuto do último dia).
- __Dados consolidados (Baixa resolução, longo prazo)__: Agrupados em médias de 3 a 7 dias para análise de tendências.
  - Exemplo: `xray-3-day.json` ou `xray-7-day.json`.

### B. Estrutura dos Parâmetros Internos (Chaves do JSON)

Ao fazer o `requests.get()`, você receberá uma lista de dicionários. Para filtrar ou isolar um satélite específico dentro do código Python, você deve usar os seguintes parâmetros estruturais contidos na resposta:

- `time_tag`: Carimbo de data e hora (padrão UTC). Usado para filtrar janelas de tempo específicas via código.
- `satellite`: Indica o número do satélite que gerou aquele registro (ex: 16, 18). Útil se você quiser comparar dados de dois sensores GOES diferentes.
- `flux` / `density` / `speed`: A métrica científica do dado (ex: fluxo de raios-X em \(W/m^2\) ou velocidade do vento solar em \(km/s\)).

```python
import requests
from datetime import datetime

# Buscando fluxo de raios-X dos últimos 3 dias
url = "https://noaa.gov"
headers = {"User-Agent": "AstroPython/1.0"}

response = requests.get(url, headers=headers)
todos_dados = response.json()

# PARÂMETROS DE ESCOLHA (Configurados por você)
satelite_escolhido = 16  # Queremos dados apenas do GOES-16
data_limite = "2026-07-01 12:00:00"  # Exemplo de corte de horário

dados_filtrados = []

for registro in todos_dados:
    # 1. Filtro por satélite
    if registro.get("satellite") == satelite_escolhido:
        # 2. Filtro por parâmetro de tempo
        if registro["time_tag"] >= data_limite:
            dados_filtrados.append(registro)

print(f"Total de registros filtrados para o GOES-16 a partir de {data_limite}: {len(dados_filtrados)}")
```

