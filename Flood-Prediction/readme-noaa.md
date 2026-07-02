# 1. Satélites 

### GOES (Geostationary Operational Environmental Satellite)

- __O que monitoram__: Explosões solares (Solar Flares), fluxo de Raios-X, Prótons, Elétrons e o campo magnético da Terra.
- __Identificação no JSON/URL__: Geralmente identificados por números (ex: `goes-16`, `goes-18`, `goes-19`).
- __Uso prático__: Se você quer saber se uma erupção solar acabou de acontecer, você consome dados do satélite GOES que estiver posicionado como "GOES-Primary" ou "GOES-Secondary".

- __xrsa (Short Channel - 0.5 a 4 Å (_angstroms_))__: Medição de canal curto de Raios X.
- __xrsb (Long Channel - 1 a 8 Å)__: Medição de canal longo de Raios X. É a coluna xrsb que você deve utilizar para calcular e identificar as classes de explosão solar (A, B, C, M, X).

### Satélite DSCOVR (Deep Space Climate Observatory)

- __O que monitora__: Vento Solar em tempo real (velocidade, densidade, temperatura) e o Campo Magnético Interplanetário (IMF). Ele fica posicionado no ponto de gravidade L1, entre o Sol e a Terra.
- __Identificação no JSON/URL__: As URLs contêm dscovr ou termos de vento solar como mag-5-minute e plasma-5-minute.
- __Uso prático__: Essencial para prever Auroras Boreais e tempestades geomagnéticas com cerca de 30 a 60 minutos de antecedência.

## 2. Entendendo os Parâmetros das Requisições

<details><summary>detalhes</summary>

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

</details>

# Imagens: 

<details><summary>detalhes</summary>

Para obter imagens, em vez de buscar pelo instrumento de Raios X, nós buscamos pelo instrumento AIA (do satélite [SDO](https://sdo.gsfc.nasa.gov/)) ou pelo instrumento SUVI (presente nos próprios satélites GOES-18 e GOES-19).

```bash
pip install sunpy astropy matplotlib
```

```python
import matplotlib.pyplot as plt
from sunpy.net import Fido, attrs as a
import sunpy.map

def baixar_imagem_sol(data_hora):
    """
    Busca e baixa uma imagem ultravioleta do Sol (comprimento de onda 171 Å)
    para uma data e hora específicas utilizando o satélite SDO (instrumento AIA).
    
    Exemplo de formato para data_hora: '2024-05-10 12:00:00'
    """
    print(f"Buscando imagem do Sol para a data: {data_hora}...")
    
    # 1. Configura a busca. Usamos uma janela de 10 minutos ao redor da hora desejada
    # e definimos o comprimento de onda de 171 Angstroms (mostra a coroa solar em dourado/amarelo)
    resultado = Fido.search(
        a.Time(data_hora, data_hora + " 00:10:00"),
        a.Instrument.aia,
        a.Wavelength(171 * a.Unit('Angstrom'))
    )
    
    if not resultado:
        print("Nenhuma imagem encontrada para este horário.")
        return None
        
    # Seleciona apenas o primeiro arquivo encontrado para poupar download
    primeiro_resultado = resultado[0, 0] 
    
    # 2. Faz o download do arquivo FITS (formato de imagem científica)
    arquivo_baixado = Fido.fetch(primeiro_resultado)
    
    # 3. Carrega o arquivo baixado utilizando o SunPy Map
    mapa_solar = sunpy.map.Map(arquivo_baixado[0])
    
    # 4. Plota e exibe a imagem do Sol
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(projection=mapa_solar)
    mapa_solar.plot(axes=ax)
    mapa_solar.draw_limb(axes=ax) # Desenha a borda do Sol
    
    plt.title(f"Sol em {data_hora} - AIA 171 Å")
    plt.show()
    
    return arquivo_baixado[0]

# --- EXEMPLO DE USO ---
# Vamos buscar uma imagem do dia 10 de Maio de 2024 às 12h00 UTC
caminho_arquivo = baixar_imagem_sol("2024-05-10 12:00:00")
print(f"Imagem salva localmente em: {caminho_arquivo}")

```

- `171`: Mostra a coroa solar e loops magnéticos. Fica com uma coloração amarelada clássica.
- `193`: Destaca regiões ativas e buracos coronais (zonas de vento solar forte). Visual mais acastanhado.
- `304`: Mostra filamentos e erupções gigantes saindo da borda do Sol. Visual vermelho intenso.
- `1600`: Revela a transição entre a superfície física do Sol (fotosfera) e a atmosfera solar.

</details>
