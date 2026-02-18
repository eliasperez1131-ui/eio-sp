from flask import Flask, render_template, request

app = Flask(__name__)

# Reactivos EIO-SP versión básica
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
    return "EIO-SP Plataforma Activa v4"

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():

    if request.method == "POST":
        resultados = {}

        for pregunta in preguntas:
            valor = int(request.form.get(pregunta["id"], 0))
            dim = pregunta["dimension"]

            if dim not in resultados:
                resultados[dim] = 0

            resultados[dim] += valor

        return render_template("resultado.html", resultados=resultados)

    return render_template("test.html", preguntas=preguntas)
