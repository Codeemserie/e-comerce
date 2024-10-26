from flask import Flask
from loja.ext.extensions import db, migrate, login_manager
from loja.ext.routes import main_blueprint
from loja.ext.models import User

def create_app():
    app = Flask(__name__)

    # Filtro personalizado para formatar números como moeda
    @app.template_filter('number_format')
    def number_format(value):
        try:
            return f"R$ {float(value):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except (ValueError, TypeError):
            return value

    # Configurações da aplicação
    app.config.from_object('config.Config')

    # Inicializa as extensões
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Definir a rota padrão de login
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'  # Mensagem de login

    # Adicionar o user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Busca o usuário pelo ID

    # Registrar blueprints (rotas)
    app.register_blueprint(main_blueprint, url_prefix='/')


    return app