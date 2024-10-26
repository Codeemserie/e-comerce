# loja/blueprints/filtro_pesquisa.py

from flask import Blueprint, render_template, request
from loja.ext.models import Products

# Criar um blueprint
filtro_pesquisa_bp = Blueprint('filtro_pesquisa', __name__)

@filtro_pesquisa_bp.route('/pesquisar', methods=['GET'])
def pesquisa():
    query = request.args.get('q', '')
    results = []
    if query:
        results = Products.query.filter(Products.name.contains(query)).all()  # Filtragem
    return render_template('resultado_pesquisa.html', results=results)