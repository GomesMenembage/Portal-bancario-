from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Banco(db.Model):
    __tablename__ = "bancos"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    localizacao_sede = db.Column(db.String(255), nullable=False)
    email_atendimento = db.Column(db.String(70), nullable=False)
    telefone_sede = db.Column(db.String(13), nullable=False)

    filiais = db.relationship('Filial', backref='banco', lazy=True)
    servicos = db.relationship('Servico', backref='banco', lazy=True)

class Filial(db.Model):
    __tablename__ = "filiais"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    localizacao = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    telefone = db.Column(db.String(13), nullable=False)

    banco_id = db.Column(db.Integer, db.ForeignKey('bancos.id'), nullable=False)
    servicos = db.relationship('Servico', backref='filial', lazy=True)

class Servico(db.Model):
    __tablename__ = "servicos"
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    status_servico = db.Column(db.String(12), nullable=False, default='disponivel')

    banco_id = db.Column(db.Integer, db.ForeignKey('bancos.id'), nullable=False)
    filial_id = db.Column(db.Integer, db.ForeignKey('filiais.id'), nullable=False)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False, unique=True)
    senha = db.Column(db.String(128), nullable=False)