from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from repositories.chamado_repository import ChamadoRepository


class UsuarioService:

    def __init__(self):
        self.usuario_repository = UsuarioRepository()
        self.chamado_repository = ChamadoRepository()

    def listar(self):
        return self.usuario_repository.listar()

    def buscar_por_id(self, usuario_id):
        return self.usuario_repository.buscar_por_id(usuario_id)

    def criar(self, dados):

        nome = dados.get("nome")
        email = dados.get("email")
        setor = dados.get("setor")

        if not nome:
            raise ValueError("O nome é obrigatório.")

        if not email:
            raise ValueError("O e-mail é obrigatório.")

        usuario_existente = (
            self.usuario_repository.buscar_por_email(email)
        )

        if usuario_existente:
            raise ValueError(
                "Já existe um usuário cadastrado com este e-mail."
            )

        usuario = Usuario(
            nome=nome,
            email=email,
            setor=setor
        )

        return self.usuario_repository.criar(usuario)

    def atualizar(self, usuario_id, dados):

        usuario = self.usuario_repository.buscar_por_id(
            usuario_id
        )

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        nome = dados.get("nome")
        email = dados.get("email")
        setor = dados.get("setor")

        if nome is not None:

            if not nome:
                raise ValueError("O nome não pode ser vazio.")

            usuario.nome = nome

        if email is not None:

            if not email:
                raise ValueError("O e-mail não pode ser vazio.")

            usuario_com_email = (
                self.usuario_repository.buscar_por_email(email)
            )

            if (
                usuario_com_email
                and usuario_com_email.id != usuario.id
            ):
                raise ValueError(
                    "Já existe um usuário com este e-mail."
                )

            usuario.email = email

        if setor is not None:
            usuario.setor = setor

        self.usuario_repository.atualizar()

        return usuario

    def excluir(self, usuario_id):

        usuario = self.usuario_repository.buscar_por_id(
            usuario_id
        )

        if not usuario:
            raise ValueError("Usuário não encontrado.")

        chamados = (
            self.chamado_repository.listar_por_usuario(usuario_id)
        )

        if chamados:
            raise ValueError(
                "Não é possível excluir um usuário que possui chamados."
            )

        self.usuario_repository.excluir(usuario)

    def total(self):
        return self.usuario_repository.total()