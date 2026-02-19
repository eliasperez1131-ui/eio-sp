from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# =============================
# CONEXIÓN POSTGRESQL RAILWAY
# =============================

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("DATABASE_URL no está configurada en Railway.")

# Ajuste por compatibilidad
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# =============================
# MODELO EMPRESA
# =============================

class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


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
    # ======================================
    # 9️⃣ APEGO A NORMAS (45%)
    # ======================================

    {"id": "p49", "texto": "Sigo los procedimientos establecidos aunque me parezcan estrictos.", "dimension": "Apego a Normas", "invertida": False},
    {"id": "p50", "texto": "Respeto la cadena de mando y los lineamientos internos.", "dimension": "Apego a Normas", "invertida": False},
    {"id": "p51", "texto": "Cumplir protocolos es parte fundamental del servicio.", "dimension": "Apego a Normas", "invertida": False},
    {"id": "p52", "texto": "Algunas reglas pueden ignorarse si la situación lo amerita.", "dimension": "Apego a Normas", "invertida": True},
    {"id": "p53", "texto": "Si tengo experiencia, no siempre necesito seguir todos los procedimientos.", "dimension": "Apego a Normas", "invertida": True},
    {"id": "p54", "texto": "Las normas pueden adaptarse según criterio personal.", "dimension": "Apego a Normas", "invertida": True},
    # ======================================
    # 🔟 CONTROL DE IMPULSOS (45%)
    # ======================================

    {"id": "p55", "texto": "Mantengo la calma incluso cuando me provocan.", "dimension": "Control de Impulsos", "invertida": False},
    {"id": "p56", "texto": "Pienso antes de actuar en situaciones de tensión.", "dimension": "Control de Impulsos", "invertida": False},
    {"id": "p57", "texto": "Evito reaccionar de manera impulsiva ante conflictos.", "dimension": "Control de Impulsos", "invertida": False},
    {"id": "p58", "texto": "Cuando me enojo, actúo sin pensar en las consecuencias.", "dimension": "Control de Impulsos", "invertida": True},
    {"id": "p59", "texto": "Me cuesta controlar mis reacciones ante faltas de respeto.", "dimension": "Control de Impulsos", "invertida": True},
    {"id": "p60", "texto": "Si alguien me provoca, respondo inmediatamente.", "dimension": "Control de Impulsos", "invertida": True},
    # ======================================
    # 1️⃣1️⃣ TOLERANCIA A LA FRUSTRACIÓN (45%)
    # ======================================

    {"id": "p61", "texto": "Continúo trabajando aunque las cosas no salgan como planeé.", "dimension": "Tolerancia a la Frustración", "invertida": False},
    {"id": "p62", "texto": "Me adapto cuando cambian las instrucciones de forma inesperada.", "dimension": "Tolerancia a la Frustración", "invertida": False},
    {"id": "p63", "texto": "Mantengo motivación incluso ante dificultades operativas.", "dimension": "Tolerancia a la Frustración", "invertida": False},
    {"id": "p64", "texto": "Me desmotivo fácilmente cuando algo falla.", "dimension": "Tolerancia a la Frustración", "invertida": True},
    {"id": "p65", "texto": "Cuando cometo errores, me cuesta recuperarme.", "dimension": "Tolerancia a la Frustración", "invertida": True},
    {"id": "p66", "texto": "Si el turno es complicado, pierdo interés en el servicio.", "dimension": "Tolerancia a la Frustración", "invertida": True},
    # ======================================
    # 1️⃣2️⃣ ESTABILIDAD EMOCIONAL (45%)
    # ======================================

    {"id": "p67", "texto": "Mantengo estabilidad emocional en situaciones críticas.", "dimension": "Estabilidad Emocional", "invertida": False},
    {"id": "p68", "texto": "Mi estado de ánimo no afecta mi desempeño laboral.", "dimension": "Estabilidad Emocional", "invertida": False},
    {"id": "p69", "texto": "Puedo trabajar bajo presión sin alterarme excesivamente.", "dimension": "Estabilidad Emocional", "invertida": False},
    {"id": "p70", "texto": "Cambios pequeños en el entorno me alteran más de lo normal.", "dimension": "Estabilidad Emocional", "invertida": True},
    {"id": "p71", "texto": "Me irrito con facilidad durante el servicio.", "dimension": "Estabilidad Emocional", "invertida": True},
    {"id": "p72", "texto": "Mis emociones influyen demasiado en mi rendimiento.", "dimension": "Estabilidad Emocional", "invertida": True},
    # ======================================
    # 1️⃣3️⃣ TRABAJO EN EQUIPO (45%)
    # ======================================

    {"id": "p73", "texto": "Coopero activamente con mis compañeros durante el servicio.", "dimension": "Trabajo en Equipo", "invertida": False},
    {"id": "p74", "texto": "Comparto información relevante con el equipo de manera oportuna.", "dimension": "Trabajo en Equipo", "invertida": False},
    {"id": "p75", "texto": "Apoyo a mis compañeros cuando enfrentan dificultades operativas.", "dimension": "Trabajo en Equipo", "invertida": False},
    {"id": "p76", "texto": "Prefiero trabajar solo y evitar involucrarme con otros.", "dimension": "Trabajo en Equipo", "invertida": True},
    {"id": "p77", "texto": "No es mi responsabilidad apoyar a compañeros con problemas.", "dimension": "Trabajo en Equipo", "invertida": True},
    {"id": "p78", "texto": "Si un compañero comete un error, no es asunto mío.", "dimension": "Trabajo en Equipo", "invertida": True},
    # ======================================
    # 1️⃣4️⃣ RIESGO CONDUCTUAL (45%)
    # ======================================

    {"id": "p79", "texto": "Evalúo las consecuencias antes de tomar decisiones importantes.", "dimension": "Riesgo Conductual", "invertida": False},
    {"id": "p80", "texto": "Evito conductas que puedan comprometer mi empleo.", "dimension": "Riesgo Conductual", "invertida": False},
    {"id": "p81", "texto": "Considero los posibles impactos negativos antes de actuar.", "dimension": "Riesgo Conductual", "invertida": False},
    {"id": "p82", "texto": "A veces asumo riesgos innecesarios sin medir consecuencias.", "dimension": "Riesgo Conductual", "invertida": True},
    {"id": "p83", "texto": "No siempre analizo las posibles repercusiones de mis actos.", "dimension": "Riesgo Conductual", "invertida": True},
    {"id": "p84", "texto": "Tomar decisiones impulsivas puede ser beneficioso en ciertos casos.", "dimension": "Riesgo Conductual", "invertida": True},
    # ======================================
    # 1️⃣5️⃣ SEGURIDAD DE LA INFORMACIÓN (45%)
    # ======================================

    {"id": "p85", "texto": "Protejo la información confidencial a la que tengo acceso.", "dimension": "Seguridad de la Información", "invertida": False},
    {"id": "p86", "texto": "Evito compartir datos sensibles sin autorización.", "dimension": "Seguridad de la Información", "invertida": False},
    {"id": "p87", "texto": "Respeto los protocolos de manejo de bases de datos.", "dimension": "Seguridad de la Información", "invertida": False},
    {"id": "p88", "texto": "Compartir información interna no siempre representa un riesgo.", "dimension": "Seguridad de la Información", "invertida": True},
    {"id": "p89", "texto": "Si la información parece inofensiva, puede difundirse sin problema.", "dimension": "Seguridad de la Información", "invertida": True},
    {"id": "p90", "texto": "No es grave divulgar ciertos datos si no se usan con mala intención.", "dimension": "Seguridad de la Información", "invertida": True},

]

@app.route("/")
def home():
    return "EIO-SP Plataforma Activa v15 - En Construcción"
@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():

    if request.method == "POST":

        # VALIDACIÓN
        for pregunta in preguntas:
            if pregunta["id"] not in request.form:
                return "Error: Debe responder todos los reactivos antes de enviar la evaluación."

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

            # Ajusta el 6 si cada dimensión tiene 6 reactivos
            porcentaje = round((puntaje / (6 * 5)) * 100)
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
            clasificacion = "No Recomendable"
            dictamen = "NO APTO"
        elif igio >= 80:
            clasificacion = "Recomendable"
            dictamen = "APTO"
        elif igio >= 65:
            clasificacion = "Aceptable"
            dictamen = "APTO"
        else:
            clasificacion = "No Recomendable"
            dictamen = "NO APTO"

        # ===============================
        # GENERACIÓN DE RESUMEN AUTOMÁTICO
        # ===============================

        fortalezas = []
        medias = []
        debiles = []

        for dimension, porcentaje in dimensiones_resultado.items():
            if porcentaje >= 75:
                fortalezas.append(dimension)
            elif porcentaje >= 50:
                medias.append(dimension)
            else:
                debiles.append(dimension)

        resumen_partes = []

        if fortalezas:
            resumen_partes.append(
                "El elemento presenta fortalezas claras en " +
                ", ".join(fortalezas) +
                ", lo que indica consistencia en su desempeño operativo."
            )

        if medias:
            resumen_partes.append(
                "Se identifican áreas que pueden fortalecerse mediante supervisión y capacitación en " +
                ", ".join(medias) + "."
            )

        if debiles:
            resumen_partes.append(
                "Se detectan debilidades significativas en " +
                ", ".join(debiles) +
                ", que requieren intervención o análisis complementario."
            )

        if not resumen_partes:
            resumen_partes.append(
                "El perfil evaluado refleja estabilidad conductual y alineación general con los estándares de integridad operativa."
            )

        resumen = " ".join(resumen_partes)

        return render_template(
            "resultado.html",
            dimensiones=dimensiones_resultado,
            igio=igio,
            dictamen=dictamen,
            resumen=resumen
        )

    # ALEATORIZACIÓN
    import random
    preguntas_aleatorias = preguntas.copy()
    random.shuffle(preguntas_aleatorias)

    return render_template("test.html", preguntas=preguntas_aleatorias)
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import io

@app.route("/descargar_pdf")
def descargar_pdf():

    igio = request.args.get("igio", "")
    dictamen = request.args.get("dictamen", "")
    resumen = request.args.get("resumen", "")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("EIO-SP Evaluación de Integridad Operativa", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"Índice Global (IGIO): {igio}%", styles["Normal"]))
    elements.append(Paragraph(f"Dictamen Final: {dictamen}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph("Resumen Ejecutivo:", styles["Heading2"]))
    elements.append(Paragraph(resumen, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Resultado_EIO_SP.pdf",
        mimetype="application/pdf"
    )

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
