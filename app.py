from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metabot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)


    with app.app_context():
        db.create_all()

@app.route('/')
def index():

    registros = Log.query.all()


    return render_template('index.html', registros=registros)

    menssage_log = []

    def agregar_message_log(texto):
        message_log.append(texto)

        nuevo_registro = Log(texto=texto)
        db.session.add(nuevo_registro)
        db.session.commit()

        agregar_message_log("El usuario ha ingresado a la página de inicio")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)