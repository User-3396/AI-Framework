# A. Dados Costeiros, Marés e Correntes (Mar) -----------------------------------------------------------
# Instale no terminal: pip install noaa-coops
import pandas as pd
from noaa_coops import Station # noaa-coops converte automaticamente as consultas via API Tides & Currents do NOAA em DataFrames

# Exemplo: Estação de Seattle (ID: 9447130)
estacao = Station(id="9447130")

# Buscando dados de marés observadas (últimos dias)
df_mares = estacao.get_data(
    begin_date="20260501",
    end_date="20260601",
    product="water_level",
    datum="MLLW",
    units="metric"
)
print(df_mares.head())


# B. Atividade Solar e Clima Espacial ---------------------------------------------------------------
# O SWPC (Space Weather Prediction Center) do NOAA fornece APIs públicas em formato JSON

import pandas as pd
import requests

# Dados de vento solar dos últimos 7 dias via API do NOAA
url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
response = requests.get(url)
data = response.json()

# O primeiro elemento geralmente contém os cabeçalhos das colunas
df_vento_solar = pd.DataFrame(data[1:], columns=data[0])
print(df_vento_solar.head())

