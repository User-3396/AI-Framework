import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# 1. Pergunta do problema

# Quais características dos passageiros ajudam a prever a sobrevivência no Titanic?
# Tipo de problema: classificação, porque queremos prever uma categoria: 
# 1 = sobreviveu
# 0 = não sobreviveu 
 
# 2. coleta de dados
df = pd.read_csv('dataset/Titanic-Dataset.csv')


# 3. Feature engineering
df["family_size"] = df["SibSp"] + df["Parch"] + 1
df["is_alone"] = (df["family_size"] == 1).astype(int)

# 4. Seleção e limpeza inicial
features = ["Pclass", "Sex", "Age", "Fare", "Embarked", "family_size", "is_alone"]
target = "Survived"

X = df[features]
y = df[target]

# 5. Seleção do algoritmo - Logistic Regression

# 6. Separar treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Preparação das colunas
numeric_features = ["Age", "Fare", "family_size", "is_alone"]
categorical_features = ["Pclass", "Sex", "Embarked"]

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, numeric_features),
    ("cat", categorical_transformer, categorical_features)
])

# 8. Criar o modelo
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# 7. Treinar os dados
model.fit(X_train, y_train)

# 9. Avaliar
y_pred = model.predict(X_test)

print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de classificação:")
print(classification_report(y_test, y_pred))
print("\nMatriz de confusão:")
print(confusion_matrix(y_test, y_pred))

# 10. Implantar / salvar
joblib.dump(model, "titanic_model.pkl")

# Exemplo de nova previsão
novo_passageiro = pd.DataFrame([{
    "Pclass": 1,
    "Sex": "female",
    "Age": 29,
    "Fare": 100,
    "Embarked": "S",
    "family_size": 1,
    "is_alone": 1
}])

previsao = model.predict(novo_passageiro)
print("\nPrevisão para novo passageiro:", previsao[0])