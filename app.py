from flask import Flask, render_template, request

app = Flask(__name__)

preguntas = []

dimensiones = [
    "Honestidad Operativa",
    "Conducta ante Sobornos",
    "Conducta ante Sustancias",
    "Prevención de Violencia General",
    "Violencia Sexual y Conducta Inapropiada",
    "Seguridad Laboral",
    "Uso Proporcional de la Fuerza",
    "Responsabilidad Proactiva",
    "Apego a Normas",
    "Control de Impulsos",
    "Tolerancia a la Frustración",
    "Estabilidad Emocional",
    "Trabajo en Equipo",
    "Riesgo Conductual",
    "Seguridad de la Información"
]

contador = 1

for dim in dimensiones:
    for i in range(3):
        preguntas.append({
            "id": f"p{contador}",
            "texto": f"{dim} - Reactivo positivo {i+1}",
            "dimension": dim,
            "invertida": False
        })
        contador += 1

    for i in range(3):
        preguntas.append({
            "id": f"p{contador}",
            "texto": f"{dim} - Reactivo invertido {i+1}",
            "dimension": dim,
            "invertida": True
        })
        contador += 1


@app.route("/")
def home():
    return "EIO-SP Plataforma Activa v15 - 90 Reactivos"


@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():

    if request.method == "POST":

        resultados = {}
        total_general = 0

        for pregunta in preguntas:
            respuesta = int(request.form.get(pregunta["id"], 0))

            if pregunta["invertida"]:
                valor = 6 - respuesta
            else:
                valor = respuesta

            dim = pregunta["dimension"]

            total_general += valor

            if dim not in resultados:
                resultados[dim] = 0

            resultados[dim] += valor

        maximo_posible = len(preguntas) * 5
        igio = round((total_general / maximo_posible) * 100)

        dimensiones_resultado = {}
        dim_critica = False

        for dimension, puntaje in resultados.items():

            porcentaje = round((puntaje / 30) * 100)
            dimensiones_resultado[dimension] = porcentaje

            if dimension in [
                "Honestidad Operativa",
                "Conducta ante Sobornos",
                "Conducta ante Sustancias",
                "Prevención de Violencia General",
                "Violencia Sexual y Conducta Inapropiada"
            ]:
                umbral = 60

            elif dimension in [
                "Seguridad Laboral",
                "Uso Proporcional de la Fuerza",
                "Responsabilidad Proactiva"
            ]:
                umbral = 50

            else:
                umbral = 45

            if porcentaje < umbral:
                dim_critica = True

        if dim_critica:
            clasificacion = "No Recomendable (Dimensión Crítica)"
            color = "red"
            dictamen = "NO APTO"
        elif igio >= 80:
            clasificacion = "Recomendable"
            color = "green"
            dictamen = "APTO"
        elif igio >= 65:
            clasificacion = "Riesgo Medio"
            color = "orange"
            dictamen = "APTO CON RESERVA"
        else:
            clasificacion = "No Recomendable"
            color = "red"
            dictamen = "NO APTO"

        return render_template(
            "resultado.html",
            dimensiones=dimensiones_resultado,
            igio=igio,
            clasificacion=clasificacion,
            color=color,
            dictamen=dictamen
        )

    return render_template("test.html", preguntas=preguntas)


if __name__ == "__main__":
    app.run(debug=True)
