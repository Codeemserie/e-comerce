import os
from crypt import methods

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, login_required, current_user, logout_user
from loja.ext.models import User, Products
from loja.ext.extensions import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError, OperationalError
from werkzeug.exceptions import BadRequest

main_blueprint = Blueprint('main', __name__)

# Rota inicial
@main_blueprint.route('/')
def home():
    user = current_user.username if current_user.is_authenticated else None
    return render_template('index.html', user=user)

# Rota para a conta
@main_blueprint.route('/conta')
@login_required
def conta():
    try:
        # Obtém informações do usuário atual
        user = current_user
        admin = user.is_admin  # Valor 0 ou 1 vindo do banco
        print(f"admin: {admin}")

        # Renderiza o template e passa o valor de 'admin' para a view
        return render_template('conta.html', user=user, admin=admin)
    except Exception as e:
        flash("Erro ao acessar os dados da conta. Tente novamente.", "danger")
        return redirect(url_for('main.home'))



@main_blueprint.route('/edit_account', methods=['GET', 'POST'])
@login_required
def edit_account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Atualiza as informações do usuário
        user = current_user
        user.username = username
        user.email = email

        if password:
            user.set_password(password)  # Atualiza a senha apenas se uma nova for fornecida

        try:
            db.session.commit()
            flash("Informações da conta atualizadas com sucesso!", "success")
            return redirect(url_for('main.conta'))  # Redireciona após a atualização
        except Exception as e:
            db.session.rollback()
            flash("Erro ao atualizar as informações. Tente novamente.", "danger")
    else:
        # Se for um GET, renderiza o formulário de edição
        return render_template('edit_conta.html', user=current_user)  # Certifique-se de criar esse template


@main_blueprint.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user

    try:
        # Exclui o usuário do banco de dados
        db.session.delete(user)
        db.session.commit()
        flash("Conta excluída com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao excluir a conta. Tente novamente.", "danger")

    logout_user()  # Desloga o usuário após a exclusão
    return redirect(url_for('main.login'))

# Rota para a página de login
@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('senha')

        # Buscando o usuário pelo e-mail
        user = User.query.filter_by(email=email).first()

        # Verificando a senha
        if user and user.check_password(password):
            login_user(user)  # Inicia a sessão do usuário
            flash("Login bem-sucedido!", "success")
            return redirect(url_for('main.home', user_id=user.id))
        else:
            flash("Usuário ou senha inválidos", "danger")

    return render_template('login.html')

# Rota para realizar logout
@main_blueprint.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash("Logout bem-sucedido!", "success")
    return redirect(url_for('main.login'))

# Rota para a página de cadastro
@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('nome')
        email = request.form.get('email')
        password = request.form.get('senha')
        is_admin = '0'

        # Verificando se o usuário ou e-mail já existem
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Usuário ou e-mail já existe", "danger")
            return redirect(url_for('main.register'))

        # Criando novo usuário
        try:
            new_user = User(username=username, email=email, is_admin=is_admin)
            new_user.set_password(password)  # Gera o hash da senha
            db.session.add(new_user)
            db.session.commit()

            flash("Cadastro bem-sucedido! Faça login.", "success")
            return redirect(url_for('main.login'))

        except IntegrityError:
            db.session.rollback()
            flash("Erro: o e-mail ou nome de usuário já existe.", "danger")
            print("Erro de integridade: tentativa de duplicação de email ou nome de usuário.")

        except OperationalError:
            db.session.rollback()
            flash("Erro de conexão com o banco de dados. Tente novamente mais tarde.", "danger")
            print("Erro operacional: verifique a conexão com o banco de dados.")

        except BadRequest:
            db.session.rollback()
            flash("Erro de dados: alguns campos obrigatórios estão ausentes ou inválidos.", "danger")
            print("Erro de solicitação: campos obrigatórios ausentes ou inválidos.")

        except Exception as e:
            db.session.rollback()
            flash("Erro inesperado. Tente novamente mais tarde.", "danger")
            print(f"Erro inesperado: {e}")

    return render_template('register.html')

@main_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin == 1:  # Comparação correta com inteiro
        products = Products.query.all()
        users = User.query.all()
        return render_template('admin.html', products=products, users=users)
    else:
        flash("Usuário não autorizado.", "danger")
        return redirect(url_for("main.conta"))


@main_blueprint.route('/add_product', methods=['POST'])
@login_required
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')
    image = request.files.get('image')  # Obtém o arquivo da imagem
    user_id = current_user.id if current_user.is_authenticated else None

    if not name or not price or not image:
        flash("Nome, preço e imagem são obrigatórios!", "danger")
        return redirect(url_for('main.admin'))

    # Processa a imagem
    if image:
        # Garante que o nome do arquivo seja seguro
        filename = secure_filename(image.filename)
        # Define o caminho onde a imagem será salva
        image_path = os.path.join(current_app.root_path, 'static/img/products', filename)
        # Salva a imagem no diretório
        image.save(image_path)

        # Cria o novo produto com o caminho da imagem
        new_product = Products(name=name, price=price, description=description, image=filename, user_id=user_id)
        db.session.add(new_product)

        try:
            db.session.commit()
            flash("Produto adicionado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao adicionar o produto. Tente novamente. {e}", "danger")
            print(f"Erro ao adicionar o produto. Tente novamente. {e}")

    return redirect(url_for('main.admin'))



@main_blueprint.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Products.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name', product.name)
        product.price = request.form.get('price', product.price)
        product.description = request.form.get('description', product.description)

        try:
            db.session.commit()
            flash("Produto editado com sucesso!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Erro ao editar o produto. Tente novamente.", "danger")

        return redirect(url_for('main.admin'))

    return render_template('edit_product.html', product=product)


@main_blueprint.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Products.query.get_or_404(product_id)

    db.session.delete(product)

    try:
        db.session.commit()
        flash("Produto excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao excluir o produto. Tente novamente.", "danger")

    return redirect(url_for('main.admin'))

@main_blueprint.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)

    try:
        db.session.commit()
        flash("Usuário excluído com sucesso!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Erro ao excluir o usuário. Tente novamente.", "danger")

    return redirect(url_for('main.admin'))


@main_blueprint.route('/search')
def pesquisa():
    query = request.args.get('query', '').strip()
    page = request.args.get('page', 1, type=int)  # Suporte a paginação
    per_page = 10  # Número de resultados por página

    results = []
    if query:
        try:
            # Filtragem case-insensitive e sem duplicações
            results = Products.query.filter(
                Products.name.ilike(f"%{query}%")
            ).distinct().paginate(page=page, per_page=per_page)
        except SQLAlchemyError as e:
            flash("Erro ao realizar a busca. Tente novamente mais tarde.", "error")
            return redirect(url_for('main.home'))

    return render_template(
        'resultado_pesquisa.html',
        results=results,
        query=query
    )