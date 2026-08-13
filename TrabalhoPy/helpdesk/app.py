from flask import Flask, jsonify

from database import db

from controllers.usuario_controller import usuario_bp
from controllers.chamado_controller import chamado_bp

from repositories.usuario_repository import UsuarioRepository
from repositories.chamado_repository import ChamadoRepository


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///helpdesk.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


app.register_blueprint(usuario_bp)
app.register_blueprint(chamado_bp)


usuario_repository = UsuarioRepository()
chamado_repository = ChamadoRepository()


@app.route("/estatisticas", methods=["GET"])
def estatisticas():

    return jsonify({
        "usuarios": usuario_repository.total(),
        "chamados": chamado_repository.total(),
        "abertos": chamado_repository.contar_por_status(
            "Aberto"
        ),
        "em_atendimento":
            chamado_repository.contar_por_status(
                "Em atendimento"
            ),
        "encerrados":
            chamado_repository.contar_por_status(
                "Encerrado"
            )
    }), 200


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)