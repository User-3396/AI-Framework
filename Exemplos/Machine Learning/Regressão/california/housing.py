import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression



# Pergunta:
# Podemos prever o valor mediano das casas na Califórnia
# com base em atributos geográficos, demográficos e econômicos?



# Dados
df = pd.read_csv("datasets/housing.csv")

print("Informações do dataset:")
df.info()

print("\nPrimeiras linhas:")
print(df.head())



# Feature engineering
# Usando diretamente as variáveis do dataset.
# A variável alvo será median_house_value.

X = df.drop("median_house_value", axis=1)
y = df["median_house_value"]

print("\nShape de X:", X.shape)
print("Shape de y:", y.shape)


# Limpeza
# Esse dataset possui valores ausentes em total_bedrooms.
# Também possui uma variável categórica: ocean_proximity.

print("\nValores ausentes:")
print(df.isnull().sum())


# Separar colunas numéricas e categóricas

num_cols = [
    "longitude",
    "latitude",
    "housing_median_age",
    "total_rooms",
    "total_bedrooms",
    "population",
    "households",
    "median_income"
]

cat_cols = ["ocean_proximity"]

print("\nColunas numéricas:", num_cols)
print("Colunas categóricas:", cat_cols)



# Pré-processamento

# Numéricas:
# - preencher ausentes com mediana
# - normalizar
#
# Categóricas:
# - preencher ausentes com moda
# - aplicar OneHotEncoder

numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("num", numeric_transformer, num_cols),
    ("cat", categorical_transformer, cat_cols)
])



# Algoritmo
# Vamos usar Regressão Linear como modelo.
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("model", LinearRegression())
])


# Treino/teste
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nShape de X_train:", X_train.shape)
print("Shape de X_test:", X_test.shape)


# Modelo
pipeline.fit(X_train, y_train)

y_train_pred = pipeline.predict(X_train)
y_test_pred = pipeline.predict(X_test)


# Avaliação
mae = mean_absolute_error(y_test, y_test_pred)
mse = mean_squared_error(y_test, y_test_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_test_pred)

print("\nAvaliação do modelo:")
print(f"MAE  = {mae:.2f}")
print(f"MSE  = {mse:.2f}")
print(f"RMSE = {rmse:.2f}")
print(f"R²   = {r2:.4f}")


# Implantação
joblib.dump(pipeline, "housing_pipeline.pkl")

print("\nPipeline salvo com sucesso em: housing_pipeline.pkl")