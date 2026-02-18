from flask import Flask, render_template, request

app = Flask(__name__)

# ======================================
# EIO-SP v9 - 54 Reactivos
# ======================================

preguntas = [

    # HONESTIDAD OPERATIVA
    {"id": "p1", "texto": "Cumplo las normas incluso cuando nadie me supervisa.", "dimension": "Honestidad Operativa", "invertida": False},
    {"id": "p2", "texto": "Considero que la honestidad es fundamental en el servicio de seguridad.", "dimension": "Honestidad Operativa", "invertida": False},
    {"id": "p3", "texto": "Prefiero reportar irregularidades aunque eso me genere problemas.", "dimension": "Honestidad Operativa", "invertida": False},
    {"id": "p4", "texto": "Tomar objetos pequeños del servicio no afecta realmente a la empresa.", "dimension": "Honestidad Operativa", "invertida": True},
    {"id": "p5", "texto": "Si nadie se da cuenta, algunas faltas no son importantes.", "dimension": "Honestidad Operativa", "invertida": True},
    {"id": "p6", "texto": "Alterar un reporte puede justificarse si ayuda al equipo.", "dimension": "Honestidad Operativa", "invertida": True},

    # CONDUCTA ANTE SOBORNOS
    {"id": "p7", "texto": "Rechazaría cualquier beneficio económico a cambio de ignorar una falta.", "dimension": "Conducta ante Sobornos", "invertida": False},
    {"id": "p8", "texto": "Reportaría un intento de soborno inmediatamente.", "dimension": "Conducta ante Sobornos", "invertida": False},
    {"id": "p9", "texto": "Mi integridad no depende del monto ofrecido.", "dimension": "Conducta ante Sobornos", "invertida": False},
    {"id": "p10", "texto": "Si el pago es alto, podría considerar hacer una excepción.", "dimension": "Conducta ante Sobornos", "invertida": True},
    {"id": "p11", "texto": "Aceptar un apoyo ocasional no perjudica a nadie.", "dimension": "Conducta ante Sobornos", "invertida": True},
    {"id": "p12", "texto": "Un soborno pequeño no representa un riesgo real.", "dimension": "Conducta ante Sobornos", "invertida": True},

    # APEGO A NORMAS
    {"id": "p13", "texto": "Sigo los protocolos aunque los considere excesivos.", "dimension": "Apego a Normas", "invertida": False},
    {"id": "p14", "texto": "Cumplir procedimientos es parte esencial del servicio.", "dimension": "Apego a Normas", "invertida": False},
    {"id": "p15", "texto": "Respeto la cadena de mando establecida.", "dimension": "Apego a Normas", "invertida": False},
    {"id": "p16", "texto": "Las reglas pueden ignorarse si la situación lo amerita.", "dimension": "Apego a Normas", "invertida": True},
    {"id": "p17", "texto": "Algunas normas son innecesarias y no siempre deben cumplirse.", "dimension": "Apego a Normas", "invertida": True},
    {"id": "p18", "texto": "Si tengo experiencia, no necesito seguir todos los procedimientos.", "dimension": "Apego a Normas", "invertida": True},

    # CONTROL DE IMPULSOS
    {"id": "p19", "texto": "Mantengo la calma ante provocaciones.", "dimension": "Control de Impulsos", "invertida": False},
    {"id": "p20", "texto": "Pienso antes de actuar en situaciones de tensión.", "dimension": "Control de Impulsos", "invertida": False},
    {"id": "p21", "texto": "Evito reaccionar de manera agresiva.", "dimension": "Control de Impulsos", "invertida": False},
    {"id": "p22", "texto": "Cuando me enojo, actúo sin pensar.", "dimension": "Control de Impulsos", "invertida": True},
    {"id": "p23", "texto": "Me cuesta controlar mis reacciones ante faltas de respeto.", "dimension": "Control de Impulsos", "invertida": True},
    {"id": "p24", "texto": "Si alguien me provoca, respondo inmediatamente.", "dimension": "Control de Impulsos", "invertida": True},

    # TOLERANCIA A LA FRUSTRACIÓN
    {"id": "p25", "texto": "Puedo continuar trabajando aunque las cosas no salgan como planeé.", "dimension": "Tolerancia a la Frustración", "invertida": False},
    {"id": "p26", "texto": "Manejo bien la presión operativa.", "dimension": "Tolerancia a la Frustración", "invertida": False},
    {"id": "p27", "texto": "Me adapto cuando cambian las instrucciones.", "dimension": "Tolerancia a la Frustración", "invertida": False},
    {"id": "p28", "texto": "Me desmotivo fácilmente cuando algo falla.", "dimension": "Tolerancia a la Frustración", "invertida": True},
    {"id": "p29", "texto": "Cuando cometo errores, me cuesta recuperarme.", "dimension": "Tolerancia a la Frustración", "invertida": True},
    {"id": "p30", "texto": "Si el turno es complicado, pierdo el interés en el servicio.", "dimension": "Tolerancia a la Frustración", "invertida": True},

    # ESTABILIDAD EMOCIONAL
    {"id": "p31", "texto": "Mantengo estabilidad emocional en situaciones críticas.", "dimension": "Estabilidad Emocional", "invertida": False},
    {"id": "p32", "texto": "Mi estado de ánimo no afecta mi desempeño.", "dimension": "Estabilidad Emocional", "invertida": False},
    {"id": "p33", "texto": "Puedo trabajar bajo estrés sin alterarme.", "dimension": "Estabilidad Emocional", "invertida": False},
    {"id": "p34", "texto": "Cambios pequeños me alteran más de lo normal.", "dimension": "Estabilidad Emocional", "invertida": True},
    {"id": "p35", "texto": "Me irrito fácilmente en el trabajo.", "dimension": "Estabilidad Emocional", "invertida": True},
    {"id": "p36", "texto": "Mi estado emocional influye mucho en mi rendimiento.", "dimension": "Estabilidad Emocional", "invertida": True},

    # TRABAJO EN EQUIPO
    {"id": "p37", "texto": "Coopero activamente con mis compañeros.", "dimension": "Trabajo en Equipo", "invertida": False},
    {"id": "p38", "texto": "Comparto información relevante con el equipo.", "dimension": "Trabajo en Equipo", "invertida": False},
    {"id": "p39", "texto": "Apoyo a mis compañeros cuando lo necesitan.", "dimension": "Trabajo en Equipo", "invertida": False},
    {"id": "p40", "texto": "Prefiero trabajar solo y evitar involucrarme con otros.", "dimension": "Trabajo en Equipo", "invertida": True},
    {"id": "p41", "texto": "No es mi responsabilidad apoyar a compañeros con problemas.", "dimension": "Trabajo en Equipo", "invertida": True},
    {"id": "p42", "texto": "Si un compañero falla, no es asunto mío.", "dimension": "Trabajo en Equipo", "invertida": True},

    # RIESGO CONDUCTUAL
    {"id": "p43", "texto": "Evito situaciones que puedan comprometer mi reputación.", "dimension": "Riesgo Conductual", "invertida": False},
    {"id": "p44", "texto": "Evalúo las consecuencias antes de asumir riesgos.", "dimension": "Riesgo Conductual", "invertida": False},
    {"id": "p45", "texto": "Mantengo conducta profesional dentro y fuera del servicio.", "dimension": "Riesgo Conductual", "invertida": False},
    {"id": "p46", "texto": "Disfruto asumir riesgos aunque puedan traer consecuencias.", "dimension": "Riesgo Conductual", "invertida": True},
    {"id": "p47", "texto": "Las reglas estrictas hacen el trabajo más interesante cuando se rompen.", "dimension": "Riesgo Conductual", "invertida": True},
    {"id": "p48", "texto": "A veces es necesario cruzar límites para obtener resultados.", "dimension": "Riesgo Conductual", "invertida": True},

    # CONDUCTA ANTE SUSTANCIAS
    {"id": "p49", "texto": "Considero inaceptable presentarse al servicio bajo efectos del alcohol.", "dimension": "Conducta ante Sustancias", "invertida": False},
    {"id": "p50", "texto": "El consumo de sustancias afecta la seguridad operativa.", "dimension": "Conducta ante Sustancias", "invertida": False},
    {"id": "p51", "texto": "Mantengo hábitos que no comprometen mi desempeño laboral.", "dimension": "Conducta ante Sustancias", "invertida": False},
    {"id": "p52", "texto": "Consumir alcohol en pequeñas cantidades no afecta el servicio.", "dimension": "Conducta ante Sustancias", "invertida": True},
    {"id": "p53", "texto": "El consumo recreativo fuera del turno no influye en el trabajo.", "dimension": "Conducta ante Sustancias", "invertida": True},
    {"id": "p54", "texto": "Mientras cumpla con mis funciones, lo que consuma es asunto personal.", "dimension": "Conducta ante Sustancias", "invertida": True},
]

@app.route("/")
def home():
    return "EIO-SP Plataforma Activa v9"

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():

    if request.method == "POST":

        resultados = {}
        total_general = 0
        total_preguntas = len(preguntas)

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

        maximo_posible = total_preguntas * 5
        igio = round((total_general / maximo_posible) * 100)

        dimensiones = {}
        dim_critica = False

        for dimension, puntaje in resultados.items():
            max_dim = 6 * 5
            porcentaje = round((puntaje / max_dim) * 100)
            dimensiones[dimension] = porcentaje

            if dimension in ["Honestidad Operativa", "Conducta ante Sobornos", "Conducta ante Sustancias"]:
                if porcentaje < 60:
                    dim_critica = True
            else:
                if porcentaje < 45:
                    dim_critica = True

        if dim_critica:
            clasificacion = "No Recomendable (Dimensión Crítica)"
            color = "red"
        elif igio >= 80:
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
            dimensiones=dimensiones,
            igio=igio,
            clasificacion=clasificacion,
            color=color
        )

    return render_template("test.html", preguntas=preguntas)

if __name__ == "__main__":
    app.run(debug=True)
