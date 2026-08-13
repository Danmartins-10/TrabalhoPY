from flask import Blueprint, request, jsonify
from services.usuario_service import UsuarioService
from repositories.chamado_repository import ChamadoRepository


usuario_bp = Blueprint(
    "usuarios",
    __name__
)

usuario_service = UsuarioService()
chamado_repository = ChamadoRepository()


@usuario_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():

    usuarios = usuario_service.listar()

    return jsonify(
        [usuario.to_dict() for usuario in usuarios]
    ), 200


@usuario_bp.route("/usuarios/<int:id>", methods=["GET"])
def buscar_usuario(id):

    usuario = usuario_service.buscar_por_id(id)

    if not usuario:
        return jsonify(
            {"erro": "Usuário não encontrado."}
        ), 404

    return jsonify(
        usuario.to_dict()
    ), 200


@usuario_bp.route("/usuarios", methods=["POST"])
def criar_usuario():

    try:

        dados = request.get_json()

        if not dados:
            return jsonify(
                {"erro": "Dados não informados."}
            ), 400

        usuario = usuario_service.criar(dados)

        return jsonify(
            usuario.to_dict()
        ), 201

    except ValueError as erro:

        return jsonify(
            {"erro": str(erro)}
        ), 400


@usuario_bp.route("/usuarios/<int:id>", methods=["PUT"])
def atualizar_usuario(id):

    try:

        dados = request.get_json()

        if not dados:
            return jsonify(
                {"erro": "Dados não informados."}
            ), 400

        usuario = usuario_service.atualizar(
            id,
            dados
        )

        return jsonify(
            usuario.to_dict()
        ), 200

    except ValueError as erro:

        mensagem = str(erro)

        if mensagem == "Usuário não encontrado.":
            return jsonify(
                {"erro": mensagem}
            ), 404

        return jsonify(
            {"erro": mensagem}
        ), 400


@usuario_bp.route("/usuarios/<int:id>", methods=["DELETE"])
def excluir_usuario(id):

    try:

        usuario_service.excluir(id)

        return jsonify(
            {
                "mensagem":
                "Usuário excluído com sucesso."
            }
        ), 200

    except ValueError as erro:

        mensagem = str(erro)

        if mensagem == "Usuário não encontrado.":
            return jsonify(
                {"erro": mensagem}
            ), 404

        return jsonify(
            {"erro": mensagem}
        ), 400


@usuario_bp.route(
    "/usuarios/<int:id>/chamados",
    methods=["GET"]
)
def listar_chamados_usuario(id):

    usuario = usuario_service.buscar_por_id(id)

    if not usuario:
        return jsonify(
            {"erro": "Usuário não encontrado."}
        ), 404

    chamados = chamado_repository.listar_por_usuario(id)

    return jsonify(
        [chamado.to_dict() for chamado in chamados]
    ), 200