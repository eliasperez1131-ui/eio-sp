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
    # ======================================
    # 4️⃣ PREVENCIÓN DE VIOLENCIA GENERAL (60%)
    # ======================================

    {"id": "p19", "texto": "Mantengo trato respetuoso incluso en situaciones de tensión.", "dimension": "Prevención de Violencia General", "invertida": False},
    {"id": "p20", "texto": "Evito responder de manera agresiva ante provocaciones.", "dimension": "Prevención de Violencia General", "invertida": False},
    {"id": "p21", "texto": "Prioritizo la solución pacífica de conflictos.", "dimension": "Prevención de Violencia General", "invertida": False},
    {"id": "p22", "texto": "En algunos casos, la agresividad es necesaria para mantener control.", "dimension": "Prevención de Violencia General", "invertida": True},
    {"id": "p23", "texto": "Si alguien provoca, es normal responder de forma contundente.", "dimension": "Prevención de Violencia General", "invertida": True},
    {"id": "p24", "texto": "Algunas confrontaciones físicas pueden justificarse fácilmente.", "dimension": "Prevención de Violencia General", "invertida": True},
    # ======================================
    # 5️⃣ VIOLENCIA SEXUAL Y CONDUCTA INAPROPIADA (60%)
    # ======================================

    {"id": "p25", "texto": "Mantengo conducta profesional evitando comentarios o insinuaciones inapropiadas.", "dimension": "Violencia Sexual y Conducta Inapropiada", "invertida": False},
    {"id": "p26", "texto": "Respeto los límites personales y profesionales de los demás.", "dimension": "Violencia Sexual y Conducta Inapropiada", "invertida": False},
    {"id": "p27", "texto": "Reportaría inmediatamente cualquier conducta de acoso sexual observada.", "dimension": "Violencia Sexual y Conducta Inapropiada", "invertida": False},
    {"id": "p28", "texto": "Algunos comentarios sobre apariencia pueden tomarse como broma sin mayor problema.", "dimension": "Violencia Sexual y Conducta Inapropiada", "invertida": True},
    {"id": "p29", "texto": "Las insinuaciones no siempre deben considerarse una falta formal.", "dimension": "Violencia Sexual y Conducta Inapropiada", "invertida": True},
    {"id": "p30", "texto": "Si existe aparente consentimiento, no es necesario involucrar a la empresa.", "dimension": "Violencia Sexual y Conducta Inapropiada", "invertida": True},
    # ======================================
    # 6️⃣ SEGURIDAD LABORAL (50%)
    # ======================================

    {"id": "p31", "texto": "Utilizo el equipo de protección personal aunque no haya supervisión directa.", "dimension": "Seguridad Laboral", "invertida": False},
    {"id": "p32", "texto": "Reporto condiciones inseguras antes de que se conviertan en accidentes.", "dimension": "Seguridad Laboral", "invertida": False},
    {"id": "p33", "texto": "Cumplir protocolos de seguridad previene riesgos innecesarios.", "dimension": "Seguridad Laboral", "invertida": False},
    {"id": "p34", "texto": "Si el riesgo parece bajo, no siempre es necesario seguir todos los protocolos.", "dimension": "Seguridad Laboral", "invertida": True},
    {"id": "p35", "texto": "El equipo de protección a veces estorba y puede omitirse.", "dimension": "Seguridad Laboral", "invertida": True},
    {"id": "p36", "texto": "Los accidentes menores no requieren reporte formal.", "dimension": "Seguridad Laboral", "invertida": True},
    # ======================================
    # 7️⃣ USO PROPORCIONAL DE LA FUERZA (50%)
    # ======================================

    {"id": "p37", "texto": "Evalúo la situación antes de intervenir físicamente.", "dimension": "Uso Proporcional de la Fuerza", "invertida": False},
    {"id": "p38", "texto": "Utilizo la fuerza solo cuando es estrictamente necesaria.", "dimension": "Uso Proporcional de la Fuerza", "invertida": False},
    {"id": "p39", "texto": "Prioritizo el diálogo antes de recurrir a medidas físicas.", "dimension": "Uso Proporcional de la Fuerza", "invertida": False},
    {"id": "p40", "texto": "En situaciones tensas es mejor actuar físicamente sin evaluar demasiado.", "dimension": "Uso Proporcional de la Fuerza", "invertida": True},
    {"id": "p41", "texto": "Mostrar autoridad física evita futuros conflictos.", "dimension": "Uso Proporcional de la Fuerza", "invertida": True},
    {"id": "p42", "texto": "Una respuesta contundente siempre es la mejor forma de control.", "dimension": "Uso Proporcional de la Fuerza", "invertida": True},
    # ======================================
    # 8️⃣ RESPONSABILIDAD PROACTIVA (50%)
    # ======================================

    {"id": "p43", "texto": "Actúo cuando detecto una situación irregular aunque no sea mi turno directo.", "dimension": "Responsabilidad Proactiva", "invertida": False},
    {"id": "p44", "texto": "Prefiero intervenir preventivamente antes de que un problema crezca.", "dimension": "Responsabilidad Proactiva", "invertida": False},
    {"id": "p45", "texto": "Informo anomalías aunque no me afecten personalmente.", "dimension": "Responsabilidad Proactiva", "invertida": False},
    {"id": "p46", "texto": "Si un problema no me corresponde directamente, no es mi responsabilidad intervenir.", "dimension": "Responsabilidad Proactiva", "invertida": True},
    {"id": "p47", "texto": "Mientras cumpla mis funciones mínimas, lo demás no es asunto mío.", "dimension": "Responsabilidad Proactiva", "invertida": True},
    {"id": "p48", "texto": "No vale la pena involucrarse en situaciones que podrían complicarse.", "dimension": "Responsabilidad Proactiva", "invertida": True},

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
