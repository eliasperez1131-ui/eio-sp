from flask import Flask, render_template, request

app = Flask(__name__)

# ==========================================
# EIO-SP v15
# 90 Reactivos (Construcción en bloques)
# ==========================================

preguntas = [

    # ======================================
    # 1️⃣ HONESTIDAD OPERATIVA (60%)
    # ======================================

    {"id": "p1", "texto": "Cumplo las normas aunque nadie me esté supervisando.", "dimension": "Honestidad Operativa", "invertida": False},
    {"id": "p2", "texto": "Reporto irregularidades aunque pueda generarme inconvenientes.", "dimension": "Honestidad Operativa", "invertida": False},
    {"id": "p3", "texto": "Mantengo integridad incluso bajo presión.", "dimension": "Honestidad Operativa", "invertida": False},
    {"id": "p4", "texto": "Si nadie se da cuenta, algunas faltas pueden justificarse.", "dimension": "Honestidad Operativa", "invertida": True},
    {"id": "p5", "texto": "Modificar un reporte puede ser aceptable en ciertas circunstancias.", "dimension": "Honestidad Operativa", "invertida": True},
    {"id": "p6", "texto": "Pequeñas omisiones no afectan realmente a la empresa.", "dimension": "Honestidad Operativa", "invertida": True},

]

@app.route("/")
def home():
    return "EIO-SP Plataforma Activa v15 - En Construcción"

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

            porcentaje = round((puntaje / (6*5)) * 100)
            dimensiones_resultado[dimension] = porcentaje

            if dimension == "Honestidad Operativa":
                umbral = 60
            else:
                umbral = 45

            if porcentaje < umbral:
                dim_critica = True

        if dim_critica:
            clasificacion = "No Recomendable"
            color = "red"
            dictamen = "NO APTO"
        else:
            clasificacion = "Recomendable"
            color = "green"
            dictamen = "APTO"

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
