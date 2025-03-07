from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///metabot.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)


with app.app_context():
    db.create_all()


def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)


@app.route("/")
def index():

    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template("index.html", registros=registros_ordenados)
messages_log = []


def agregar_messages_log(texto):
    messages_log.append(texto)

    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit()


TOKEN_SYSTEMDEVELOPERS = "SYSTEMDEVELOPERS"


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        challenge = verify_token(request)
        return challenge
    elif request.method == "POST":
        reponse = recibir_mensajes(request)
        return reponse


def verify_token(req):
    token=req.args.get("hub.verify_token")
    challenge=req.args.get("hub.challenge")

    if challenge and token == TOKEN_SYSTEMDEVELOPERS:
        return challenge
    else:
        return jsonify({"error": "Token Invalido"}),401


def recibir_mensajes(req):
    req = request.get_json()
    agregar_messages_log(req)

    return jsonify({"message": "EVENT_RECEIVED"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
