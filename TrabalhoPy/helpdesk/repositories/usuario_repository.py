from models.usuario import Usuario
from database import db


class UsuarioRepository:

    def listar(self):
        return Usuario.query.all()

    def buscar_por_id(self, usuario_id):
        return db.session.get(Usuario, usuario_id)

    def buscar_por_email(self, email):
        return Usuario.query.filter_by(email=email).first()

    def criar(self, usuario):
        db.session.add(usuario)
        db.session.commit()

        return usuario

    def atualizar(self):
        db.session.commit()

    def excluir(self, usuario):
        db.session.delete(usuario)
        db.session.commit()

    def total(self):
        return Usuario.query.count()