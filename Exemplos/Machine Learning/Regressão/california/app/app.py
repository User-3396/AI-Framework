from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)

# carregar pipeline treinado
pipeline = joblib.load("housing_pipeline.pkl")


@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    erro = None

    valores = {
        "longitude": "",
        "latitude": "",
        "housing_median_age": "",
        "total_rooms": "",
        "total_bedrooms": "",
        "population": "",
        "households": "",
        "median_income": "",
        "ocean_proximity": ""
    }

    categorias_ocean = [
        "<1H OCEAN",
        "INLAND",
        "ISLAND",
        "NEAR BAY",
        "NEAR OCEAN"
    ]

    if request.method == "POST":
        try:
            for campo in valores:
                valores[campo] = request.form.get(campo, "")

            novo_dado = pd.DataFrame([{
                "longitude": float(valores["longitude"]),
                "latitude": float(valores["latitude"]),
                "housing_median_age": float(valores["housing_median_age"]),
                "total_rooms": float(valores["total_rooms"]),
                "total_bedrooms": float(valores["total_bedrooms"]),
                "population": float(valores["population"]),
                "households": float(valores["households"]),
                "median_income": float(valores["median_income"]),
                "ocean_proximity": valores["ocean_proximity"]
            }])

            predicao = pipeline.predict(novo_dado)[0]

            resultado = f"US$ {predicao:,.2f}"

        except ValueError:
            erro = "Preencha os campos numéricos com valores válidos."
        except Exception as e:
            erro = f"Erro ao processar a previsão: {str(e)}"

    return render_template(
        "index.html",
        resultado=resultado,
        erro=erro,
        valores=valores,
        categorias_ocean=categorias_ocean
    )


if __name__ == "__main__":
    app.run(debug=True)