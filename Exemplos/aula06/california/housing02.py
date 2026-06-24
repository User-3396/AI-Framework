import joblib
import pandas as pd


# Carregar modelo treinado
pipeline = joblib.load("housing_pipeline.pkl")


# Novo dado para previsão
dados = {
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 41.0,
    "total_rooms": 880.0,
    "total_bedrooms": 129.0,
    "population": 322.0,
    "households": 126.0,
    "median_income": 8.3252,
    "ocean_proximity": "NEAR BAY"
}


# converter para DataFrame
novo_dado = pd.DataFrame([dados])


print("Dados enviados:")
print(novo_dado)


# Previsão
predicao = pipeline.predict(novo_dado)

valor = predicao[0]

print("\nValor mediano previsto: $ {:,.2f}".format(valor))