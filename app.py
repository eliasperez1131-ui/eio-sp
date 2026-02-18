from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "EIO-SP Plataforma Activa"

@app.route("/evaluacion", methods=["GET", "POST"])
def evaluacion():
    if request.method == "POST":
        p1 = int(request.form.get("p1", 0))
        p2 = int(request.form.get("p2", 0))

        total = p1 + p2

        return f"Puntaje total: {total}"

    return render_template("test.html")
