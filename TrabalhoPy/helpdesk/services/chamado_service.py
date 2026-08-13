from models.chamado import Chamado
from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository


class ChamadoService:

    PRIORIDADES_VALIDAS = [
        "Baixa",
        "Média",
        "Alta"
    ]

    STATUS_VALIDOS = [
        "Aberto",
        "Em atendimento",
        "Encerrado"
    ]

    def __init__(self):
        self.chamado_repository = ChamadoRepository()
        self.usuario_repository = UsuarioRepository()

    def listar(self):
        return self.chamado_repository.listar()

    def buscar_por_id(self, chamado_id):
        return self.chamado_repository.buscar_por_id(
            chamado_id
        )

    def criar(self, dados):

        titulo = dados.get("titulo")
        descricao = dados.get("descricao")
        prioridade = dados.get("prioridade")
        tecnico = dados.get("tecnico")
        usuario_id = dados.get("usuario_id")

        if not titulo:
            raise ValueError("O título é obrigatório.")

        if len(titulo) < 5:
            raise ValueError(
                "O título deve possuir pelo menos 5 caracteres."
            )

        if not descricao:
            raise ValueError("A descrição é obrigatória.")

        if len(descricao) < 10:
            raise ValueError(
                "A descrição deve possuir pelo menos 10 caracteres."
            )

        if prioridade not in self.PRIORIDADES_VALIDAS:
            raise ValueError(
                "A prioridade deve ser Baixa, Média ou Alta."
            )

        usuario = self.usuario_repository.buscar_por_id(
            usuario_id
        )

        if not usuario:
            raise ValueError(
                "O usuário informado não existe."
            )

        quantidade = (
            self.chamado_repository
            .contar_chamados_nao_encerrados(usuario_id)
        )

        if quantidade >= 5:
            raise ValueError(
                "O usuário já possui 5 chamados que não estão encerrados."
            )

        chamado = Chamado(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            tecnico=tecnico,
            usuario_id=usuario_id,
            status="Aberto"
        )

        return self.chamado_repository.criar(chamado)

    def atualizar(self, chamado_id, dados):

        chamado = self.chamado_repository.buscar_por_id(
            chamado_id
        )

        if not chamado:
            raise ValueError("Chamado não encontrado.")

        titulo = dados.get("titulo")
        descricao = dados.get("descricao")
        prioridade = dados.get("prioridade")
        tecnico = dados.get("tecnico")

        if titulo is not None:

            if len(titulo) < 5:
                raise ValueError(
                    "O título deve possuir pelo menos 5 caracteres."
                )

            chamado.titulo = titulo

        if descricao is not None:

            if len(descricao) < 10:
                raise ValueError(
                    "A descrição deve possuir pelo menos 10 caracteres."
                )

            chamado.descricao = descricao

        if prioridade is not None:

            if prioridade not in self.PRIORIDADES_VALIDAS:
                raise ValueError(
                    "A prioridade deve ser Baixa, Média ou Alta."
                )

            chamado.prioridade = prioridade

        if tecnico is not None:
            chamado.tecnico = tecnico

        self.chamado_repository.atualizar()

        return chamado

    def excluir(self, chamado_id):

        chamado = self.chamado_repository.buscar_por_id(
            chamado_id
        )

        if not chamado:
            raise ValueError("Chamado não encontrado.")

        self.chamado_repository.excluir(chamado)

    def iniciar(self, chamado_id):

        chamado = self.chamado_repository.buscar_por_id(
            chamado_id
        )

        if not chamado:
            raise ValueError("Chamado não encontrado.")

        if chamado.status != "Aberto":
            raise ValueError(
                "Apenas chamados abertos podem ser iniciados."
            )

        chamado.status = "Em atendimento"

        self.chamado_repository.atualizar()

        return chamado

    def encerrar(self, chamado_id):

        chamado = self.chamado_repository.buscar_por_id(
            chamado_id
        )

        if not chamado:
            raise ValueError("Chamado não encontrado.")

        if chamado.status != "Em atendimento":
            raise ValueError(
                "Apenas chamados em atendimento podem ser encerrados."
            )

        chamado.status = "Encerrado"

        self.chamado_repository.atualizar()

        return chamado

    def listar_abertos(self):
        return self.chamado_repository.listar_abertos()

    def listar_prioridade_alta(self):
        return (
            self.chamado_repository
            .listar_prioridade_alta()
        )

    def estatisticas(self):

        return {
            "chamados": self.chamado_repository.total(),
            "abertos": (
                self.chamado_repository
                .contar_por_status("Aberto")
            ),
            "em_atendimento": (
                self.chamado_repository
                .contar_por_status("Em atendimento")
            ),
            "encerrados": (
                self.chamado_repository
                .contar_por_status("Encerrado")
            )
        }