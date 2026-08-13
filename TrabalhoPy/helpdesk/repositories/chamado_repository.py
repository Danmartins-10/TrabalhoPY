from models.chamado import Chamado
from database import db


class ChamadoRepository:

    def listar(self):
        return Chamado.query.all()

    def buscar_por_id(self, chamado_id):
        return db.session.get(Chamado, chamado_id)

    def criar(self, chamado):
        db.session.add(chamado)
        db.session.commit()

        return chamado

    def atualizar(self):
        db.session.commit()

    def excluir(self, chamado):
        db.session.delete(chamado)
        db.session.commit()

    def listar_por_usuario(self, usuario_id):
        return Chamado.query.filter_by(
            usuario_id=usuario_id
        ).all()

    def listar_abertos(self):
        return Chamado.query.filter_by(
            status="Aberto"
        ).all()

    def listar_prioridade_alta(self):
        return Chamado.query.filter_by(
            prioridade="Alta"
        ).all()

    def contar_por_status(self, status):
        return Chamado.query.filter_by(
            status=status
        ).count()

    def total(self):
        return Chamado.query.count()

    def contar_chamados_nao_encerrados(self, usuario_id):
        return Chamado.query.filter(
            Chamado.usuario_id == usuario_id,
            Chamado.status != "Encerrado"
        ).count()