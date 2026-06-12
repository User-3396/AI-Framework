import pandas as pd
import numpy as np

# 1. Definição da URL oficial do arquivo de 3 casas decimais
url_soi = "https://uea.ac.uk"

# 2. Mapeamento exato das larguras das colunas com base no formato (i5, 12f8.3)
# 5 caracteres para o Ano + 12 colunas de 8 caracteres para os meses
larguras_colunas = [5] + [8] * 12

# Nomes das colunas correspondentes
nomes_colunas = ['Ano', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# 3. Leitura do arquivo tratando o espaçamento fixo estruturado
df_matriz = pd.read_fwf(url_soi, widths=larguras_colunas, names=nomes_colunas, header=None)

# 4. Pivotagem da matriz (Ano x Meses) para o formato longo (Série Temporal)
df_longo = df_matriz.melt(id_vars=['Ano'], var_name='Mes_Nome', value_name='SOI')

# 5. Conversão dos nomes dos meses para formato numérico
meses_map = {'Jan': 1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai': 5, 'Jun': 6, 
             'Jul': 7, 'Ago': 8, 'Set': 9, 'Out': 10, 'Nov': 11, 'Dez': 12}
df_longo['Mes'] = df_longo['Mes_Nome'].map(meses_map)

# 6. Criação do índice de data no padrão do Pandas (Primeiro dia de cada mês)
df_longo['Data'] = pd.to_datetime(df_longo[['Ano', 'Mes']].assign(Day=1))
df_final = df_longo.set_index('Data')[['SOI']].sort_index()

# 7. Tratamento do valor ausente oficial (-99.990) indicado na imagem
df_final['SOI'] = df_final['SOI'].replace(-99.990, np.nan)
df_final = df_final.dropna()

# Visualização do resultado ajustado pronto para Machine Learning
print("Formato final dos dados ajustados:")
print(df_final.head())


# i5: O ano ocupa os primeiros 5 caracteres.
# 12f8.3: Cada um dos 12 meses seguintes ocupa exatamente 8 caracteres.
# f8.3: A média anual ocupa os últimos 8 caracteres (vamos descartar essa coluna para focar na série temporal mensal).


