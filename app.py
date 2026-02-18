from flask import Flask, render_template, request

app = Flask(__name__)

preguntas = [
    {
        "id": "p1",
        "texto": "Tomar un objeto pequeño del servicio no es algo grave.",
        "dimension": "Honestidad"
    },
    {
        "id": "p2",
        "texto": "Me irrito fácilmente cuando las cosas no salen como planeé.",
        "dimension": "Estabilidad"
    }
]

@app.route("/")
def home():
    return "EIO-SP Plataforma Activa v5"

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():

    if request.method == "POST":
        resultados = {}
        total_general = 0
        total_preguntas = len(preguntas)

        for pregunta in preguntas:
            valor = int(request.form.get(pregunta["id"], 0))
            dim = pregunta["dimension"]

            total_general += valor

            if dim not in resultados:
                resultados[dim] = 0

            resultados[dim] += valor

        # IGIO normalizado a 100
        maximo_posible = total_preguntas * 5
        igio = round((total_general / maximo_posible) * 100)

        # Clasificación automática
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
