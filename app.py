from flask import Flask, render_template, request

app = Flask(__name__)

# Reactivos EIO-SP (ejemplo base)
preguntas = [
    {
        "id": "p1",
        "texto": "Tomar un objeto pequeño del servicio no es algo grave.",
        "dimension": "Honestidad",
        "invertida": True
    },
    {
        "id": "p2",
        "texto": "Me irrito fácilmente cuando las cosas no salen como planeé.",
        "dimension": "Estabilidad",
        "invertida": True
    }
]

@app.route("/")
def home():
    return "EIO-SP Plataforma Activa v6"

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():

    if request.method == "POST":
        resultados = {}
        total_general = 0
        total_preguntas = len(preguntas)

        for pregunta in preguntas:
            respuesta = int(request.form.get(pregunta["id"], 0))

            # 🔁 Inversión correcta de reactivos de riesgo
            if pregunta["invertida"]:
                valor = 6 - respuesta
            else:
                valor = respuesta

            dim = pregunta["dimension"]

            total_general += valor

            if dim not in resultados:
                resultados[dim] = 0

            resultados[dim] += valor

        # 📊 IGIO normalizado a 100
        maximo_posible = total_preguntas * 5
        igio = round((total_general / maximo_posible) * 100)

        # 🚦 Clasificación automática
        if igio >= 80:
            clasificacion = "Recomendable"
            color = "green"
        elif igio >= 60:
            clasificacion = "Riesgo Medio"
            color = "orange"
        else:
            clasificacion = "No Recomendable"
            color = "red"

        return render_template(
            "resultado.html",
            resultados=resultados,
            igio=igio,
            clasificacion=clasificacion,
            color=color
        )

    return render_template("test.html", preguntas=preguntas)


if __name__ == "__main__":
    app.run(debug=True)
