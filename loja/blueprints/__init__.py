from flask import Blueprint

# Importar o blueprint
from .filtro_pesquisa import filtro_pesquisa_bp

# Criar um blueprint principal
main_blueprint = Blueprint('main', __name__)

# Registrar o blueprint de pesquisa
main_blueprint.register_blueprint(filtro_pesquisa_bp)