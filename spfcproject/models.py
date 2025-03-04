from email.policy import default

from spfcproject import database, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_usuario = database.Column(database.String, default='default.jpg')
    atletas_cadastrados = database.Column(database.Integer, default=0)


class Atleta(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome_completo = database.Column(database.String, nullable=False)
    data_nascimento =database.Column(database.String, nullable=False)
    cpf = database.Column(database.String, nullable=False, unique=True)
    rg = database.Column(database.String, nullable=False, unique=True)
    sexo = database.Column(database.String, nullable=False)
    nacionalidade = database.Column(database.String, nullable=False)
    naturalidade = database.Column(database.String, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    ddd = database.Column(database.String, nullable=False)
    telefone = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    foto_atleta = database.Column(database.String, default='default.jpg')
    nome_responsavel = database.Column(database.String, default='')
    telefone_responsavel = database.Column(database.String, default='')
    ddd_responsavel = database.Column(database.String, default='')