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
    # ======================================
    # 2️⃣ CONDUCTA ANTE SOBORNOS (60%)
    # ======================================

    {"id": "p7", "texto": "Rechazaría cualquier incentivo económico indebido.", "dimension": "Conducta ante Sobornos", "invertida": False},
    {"id": "p8", "texto": "Reportaría inmediatamente un intento de soborno.", "dimension": "Conducta ante Sobornos", "invertida": False},
    {"id": "p9", "texto": "Mi desempeño no depende de beneficios externos.", "dimension": "Conducta ante Sobornos", "invertida": False},
    {"id": "p10", "texto": "Si el beneficio es considerable, podría analizar la situación.", "dimension": "Conducta ante Sobornos", "invertida": True},
    {"id": "p11", "texto": "Aceptar pequeños regalos no representa un problema real.", "dimension": "Conducta ante Sobornos", "invertida": True},
    {"id": "p12", "texto": "Algunas excepciones pueden justificarse si no perjudican directamente.", "dimension": "Conducta ante Sobornos", "invertida": True},
    # ======================================
    # 3️⃣ CONDUCTA ANTE SUSTANCIAS (60%)
    # ======================================

    {"id": "p13", "texto": "Es inaceptable presentarse al servicio bajo efectos de alcohol.", "dimension": "Conducta ante Sustancias", "invertida": False},
    {"id": "p14", "texto": "El consumo de sustancias afecta la seguridad operativa.", "dimension": "Conducta ante Sustancias", "invertida": False},
    {"id": "p15", "texto": "Mantengo hábitos que no comprometen mi desempeño laboral.", "dimension": "Conducta ante Sustancias", "invertida": False},
    {"id": "p16", "texto": "Consumir en pequeñas cantidades no afecta el servicio.", "dimension": "Conducta ante Sustancias", "invertida": True},
    {"id": "p17", "texto": "Lo que haga fuera del turno no influye en mi rendimiento.", "dimension": "Conducta ante Sustancias", "invertida": True},
    {"id": "p18", "texto": "Mientras cumpla con mis funciones, el consumo no es relevante.", "dimension": "Conducta ante Sustancias", "invertida": True},

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
