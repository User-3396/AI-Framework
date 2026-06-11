# Guia Prático: Manipulação de Datasets e Visualização de Dados no Jupyter Notebook

Este documento serve como um guia rápido e de referência para manipulação de DataFrames com `pandas` e geração de gráficos utilizando `Matplotlib` e `Seaborn`.

---

## 1. Configuração Inicial do Ambiente

Sempre inicie o seu notebook importando as bibliotecas essenciais e garantindo a exibição correta dos gráficos.

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Garante que os gráficos sejam renderizados diretamente no notebook
%matplotlib inline

# Configuração opcional para melhorar o visual dos gráficos do Seaborn
sns.set_theme(style="whitegrid")
```

---

## 2. Seleção e Exibição de Colunas Específicas

Para visualizar ou isolar apenas colunas do seu interesse, utilize colchetes duplos `[[ ]]`. O uso de colchetes simples gera erro ao passar uma lista.

```python
# Selecionando exatamente 3 colunas por nome
df_selecionado = df[['coluna_A', 'coluna_B', 'coluna_C']]

# Exibindo as 5 primeiras linhas do recorte
df_selecionado.head()
```

---

## 3. Tratamento de Valores Ausentes (NaN)

Gráficos e cálculos matemáticos falham ou distorcem resultados quando há valores nulos (`NaN`). 

### Cenário A: Eliminar linhas nulas (Recomendado para Gráficos)
Remove a linha inteira apenas se o `NaN` estiver nas colunas que você vai usar para a análise.
```python
# Limpa o DataFrame focando apenas nas colunas de interesse
df_limpo = df.dropna(subset=['coluna_A', 'coluna_B'])
```

### Cenário B: Preencher os valores nulos
Substitui o `NaN` por uma métrica (como a média) ou por um valor fixo (como zero).
```python
# Substituindo por Zero
df['coluna_A'] = df['coluna_A'].fillna(0)

# Substituindo pela Média (mantém o equilíbrio estatístico da coluna)
df['coluna_B'] = df['coluna_B'].fillna(df['coluna_B'].mean())
```

---

## 4. Limitando as Linhas a serem Plotadas

Evite lentidão no Jupyter ao lidar com datasets volumosos limitando a quantidade de registros enviados ao gráfico.

### Cenário A: Primeiras ou Últimas N linhas
```python
df_top20 = df.head(20)  # Primeiras 20 linhas
df_ultimas10 = df.tail(10)  # Últimas 10 linhas
```

### Cenário B: Recorte/Intervalo específico (`iloc`)
```python
# Corta do índice 50 até o 149 (100 linhas no total)
df_recorte = df.iloc[50:150]
```

### Cenário C: Amostragem Aleatória (Amostra Estatística)
```python
# Seleciona 500 linhas aleatórias. random_state garante repetibilidade do teste.
df_amostra = df.sample(n=500, random_state=42)
```

### Cenário D: Filtro Condicional (Máscara Booleana)
```python
# Filtrando apenas linhas onde o valor é maior que um critério
df_filtrado = df[df['coluna_preco'] > 150.00]
```

---

## 5. Galeria de Gráficos Essenciais

Abaixo está o código integrado aplicando seleção de colunas, remoção de `NaN` e plotagem correta.

### Gráfico de Linhas (Tendências Temporais / Sequenciais)
```python
plt.figure(figsize=(10, 4))
plt.plot(df_limpo['coluna_A'], label='Tendência A', color='blue', linewidth=2)
plt.title('Evolução dos Valores da Coluna A', fontsize=14)
plt.xlabel('Índice/Tempo')
plt.ylabel('Valores')
plt.legend()
plt.grid(True)
plt.show()
```

### Gráfico de Dispersão (Correlação entre duas variáveis)
```python
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df_limpo, x='coluna_A', y='coluna_B', hue='coluna_categoria', palette='Set2')
plt.title('Dispersão e Agrupamento: Coluna A vs Coluna B', fontsize=14)
plt.xlabel('Eixo X (Coluna A)')
plt.ylabel('Eixo Y (Coluna B)')
plt.show()
```

### Gráfico de Barras (Comparações entre Categorias)
```python
# Passo prévio: Agrupar para tirar a média por categoria
df_agrupado = df_limpo.groupby('coluna_categoria')['coluna_A'].mean().reset_index()

plt.figure(figsize=(8, 4))
sns.barplot(data=df_agrupado, x='coluna_categoria', y='coluna_A', palette='viridis')
plt.title('Média da Coluna A por Categoria', fontsize=14)
plt.xticks(rotation=45) # Rotaciona os nomes do eixo X se forem muito compridos
plt.show()
```

### Histograma (Distribuição e Frequência)
```python
plt.figure(figsize=(8, 4))
sns.histplot(df_limpo['coluna_A'], bins=20, kde=True, color='purple')
plt.title('Análise de Distribuição de Frequência', fontsize=14)
plt.xlabel('Intervalos de Valores')
plt.ylabel('Contagem / Frequência')
plt.show()
```

---

## 6. Situações Extras e Avançadas

### Cenário 1: Comparações lógicas entre colunas ignorando NaN
Se você precisa comparar os valores de duas colunas linha por linha, certifique-se de que ambas existem na linha testada.
```python
# Filtro garante que nenhuma das duas colunas seja nula na linha de análise
condicao_validacao = df['coluna_A'].notna() & df['coluna_B'].notna()
df_validado = df[condicao_validacao]

# Cria uma nova coluna baseada na comparação lógica
df_validado['A_maior_que_B'] = df_validado['coluna_A'] > df_validado['coluna_B']
```

### Cenário 2: Exportar o resultado tratado para um novo arquivo
Depois de selecionar as 3 colunas, filtrar os `NaN` e limitar as linhas, você pode salvar o resultado final.
```python
# Salva o dataframe modificado sem exportar a coluna de índices numéricos
df_limpo.to_csv('meu_dataset_tratado.csv', index=False)
```
