import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
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

# 4. Seleção de atributos
features = ["Pclass", "Sex", "Age", "Fare", "Embarked", "family_size", "is_alone"]
target = "Survived"

X = df[features]
y = df[target]

# 5. Algoritmo: Decision Tree

from sklearn.tree import DecisionTreeClassifier

# Separar treino e teste primeiro
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Preencher valores numéricos
for col in ["Age", "Fare"]:
    median = X_train[col].median()
    X_train[col] = X_train[col].fillna(median)
    X_test[col] = X_test[col].fillna(median)

# Preencher categóricos
for col in ["Embarked"]:
    mode = X_train[col].mode()[0]
    X_train[col] = X_train[col].fillna(mode)
    X_test[col] = X_test[col].fillna(mode)

# Converter categóricos em números
X_train = pd.get_dummies(X_train)
X_test = pd.get_dummies(X_test)

# Ajustar colunas para ficarem iguais
X_train, X_test = X_train.align(X_test, fill_value=0, axis=1)

# Criar modelo
model = DecisionTreeClassifier(random_state=42)

# Treinar
model.fit(X_train, y_train)


# Avaliar
y_pred = model.predict(X_test)

print("Acurácia:", accuracy_score(y_test, y_pred))
print("\nRelatório de classificação:")
print(classification_report(y_test, y_pred))
print("\nMatriz de confusão:")
print(confusion_matrix(y_test, y_pred))

# Implantar / salvar
joblib.dump(model, "titanic_decision_tree.pkl")

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



# Converter categóricos em números
novo_passageiro = pd.get_dummies(novo_passageiro)

# Alinhar colunas com as do treino
novo_passageiro = novo_passageiro.reindex(columns=X_train.columns, fill_value=0)

# Fazer previsão
previsao = model.predict(novo_passageiro)

print("Previsão para novo passageiro:", previsao[0])

