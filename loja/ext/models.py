from enum import unique

from loja import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # Importa o UserMixin do Flask-Login


class User(db.Model, UserMixin):  # Herda de UserMixin para implementar os métodos obrigatórios do Flask-Login
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # Armazena o hash da senha
    is_admin = db.Column(db.Integer, nullable=False, unique=True)


    def set_password(self, password):
        """Gera o hash da senha."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado."""
        return check_password_hash(self.password_hash, password)


class Products(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Chave estrangeira que referencia a tabela 'users'