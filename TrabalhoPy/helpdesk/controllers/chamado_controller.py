from flask import Blueprint, request, jsonify
from services.chamado_service import ChamadoService


chamado_bp = Blueprint(
    "chamados",
    __name__
)

chamado_service = ChamadoService()


@chamado_bp.route("/chamados", methods=["GET"])
def listar_chamados():

    chamados = chamado_service.listar()

    return jsonify(
        [chamado.to_dict() for chamado in chamados]
    ), 200


@chamado_bp.route("/chamados/<int:id>", methods=["GET"])
def buscar_chamado(id):

    chamado = chamado_service.buscar_por_id(id)

    if not chamado:
        return jsonify(
            {"erro": "Chamado não encontrado."}
        ), 404

    return jsonify(
        chamado.to_dict()
    ), 200


@chamado_bp.route("/chamados", methods=["POST"])
def criar_chamado():

    try:

        dados = request.get_json()

        if not dados:
            return jsonify(
                {"erro": "Dados não informados."}
            ), 400

        chamado = chamado_service.criar(dados)

        return jsonify(
            chamado.to_dict()
        ), 201

    except ValueError as erro:

        return jsonify(
            {"erro": str(erro)}
        ), 400


@chamado_bp.route("/chamados/<int:id>", methods=["PUT"])
def atualizar_chamado(id):

    try:

        dados = request.get_json()

        if not dados:
            return jsonify(
                {"erro": "Dados não informados."}
            ), 400

        chamado = chamado_service.atualizar(
            id,
            dados
        )

        return jsonify(
            chamado.to_dict()
        ), 200

    except ValueError as erro:

        mensagem = str(erro)

        if mensagem == "Chamado não encontrado.":
            return jsonify(
                {"erro": mensagem}
            ), 404

        return jsonify(
            {"erro": mensagem}
        ), 400


@chamado_bp.route("/chamados/<int:id>", methods=["DELETE"])
def excluir_chamado(id):

    try:

        chamado_service.excluir(id)

        return jsonify(
            {
                "mensagem":
                "Chamado excluído com sucesso."
            }
        ), 200

    except ValueError as erro:

        return jsonify(
            {"erro": str(erro)}
        ), 404


@chamado_bp.route(
    "/chamados/<int:id>/iniciar",
    methods=["PATCH"]
)
def iniciar_chamado(id):

    try:

        chamado = chamado_service.iniciar(id)

        return jsonify(
            chamado.to_dict()
        ), 200

    except ValueError as erro:

        mensagem = str(erro)

        if mensagem == "Chamado não encontrado.":
            return jsonify(
                {"erro": mensagem}
            ), 404

        return jsonify(
            {"erro": mensagem}
        ), 400


@chamado_bp.route(
    "/chamados/<int:id>/encerrar",
    methods=["PATCH"]
)
def encerrar_chamado(id):

    try:

        chamado = chamado_service.encerrar(id)

        return jsonify(
            chamado.to_dict()
        ), 200

    except ValueError as erro:

        mensagem = str(erro)

        if mensagem == "Chamado não encontrado.":
            return jsonify(
                {"erro": mensagem}
            ), 404

        return jsonify(
            {"erro": mensagem}
        ), 400


@chamado_bp.route(
    "/chamados/abertos",
    methods=["GET"]
)
def chamados_abertos():

    chamados = chamado_service.listar_abertos()

    return jsonify(
        [chamado.to_dict() for chamado in chamados]
    ), 200


@chamado_bp.route(
    "/chamados/prioridade/alta",
    methods=["GET"]
)
def chamados_prioridade_alta():

    chamados = (
        chamado_service.listar_prioridade_alta()
    )

    return jsonify(
        [chamado.to_dict() for chamado in chamados]
    ), 200