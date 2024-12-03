from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models_usuario import Usuario
from models_produto import Produto
from models_estoque import MovimentacaoEstoque
from cadastro_usuario import cadastro_bp
from db import db
import hashlib
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chavesecreta'
lm = LoginManager(app)
lm.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:oharacatherine@localhost/controle_estoque"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(cadastro_bp, url_prefix='/cadastro')


def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()


def senha_valida(senha):
    return bool(re.fullmatch(r"[A-Za-z0-9@#$%^&+=]{6,}", senha))


def get_produtos_baixo_estoque():
    return Produto.query.filter(Produto.quantidade <= Produto.quantidade_minima).all()


@lm.user_loader
def user_loader(id):
    user = Usuario.query.get(int(id))
    return user


@app.route('/')
@login_required
def home():
    if current_user.perfil == 'Administrador':
        return render_template('home.html', is_admin=True)
    elif current_user.perfil == 'Comum':
        return render_template('home.html', is_admin=False)
    else:
        flash('Acesso negado!', 'danger')
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nomeForm']
        senha = request.form['senhaForm']
        perfil_selecionado = request.form['perfil']

        user = Usuario.query.filter_by(nome=nome).first()

        if user and user.verificar_senha(senha):
            if user.perfil != perfil_selecionado:
                flash(f'Perfil incorreto! Você está registrado como "{user.perfil}".', 'danger')
                return redirect(url_for('login'))

            login_user(user)
            return redirect(url_for('home'))

        flash('Nome ou senha incorreto!', 'danger')
        return render_template('login.html', error='Nome ou senha incorreto!')

    return render_template('login.html')


@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if current_user.perfil != 'Administrador':
        flash('Acesso negado: somente administradores podem cadastrar usuários', 'danger')
        return redirect(url_for('ver_estoque'))

    if request.method == 'POST':
        nome = request.form['nomeForm']
        senha_hash = request.form['senhaForm']
        perfil = request.form['perfil']

        if len(senha_hash) < 6:
            flash('Senha deve ter no mínimo 6 números.', 'danger')
            return render_template('cadastrar_usuario.html')

        if not senha_valida(senha_hash):
            flash("A senha deve conter apenas números.")
            return redirect(url_for("cadastro.cadastrar_usuario"))

        novo_usuario = Usuario(nome=nome, perfil=perfil)

        if not novo_usuario.validar_perfil():
            flash('Perfil inválido! O perfil deve ser "Administrador" ou "Comum".', 'danger')
            return render_template('cadastrar_usuario.html')
        novo_usuario.set_senha(senha_hash)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastro.cadastrar_usuario'))

    return render_template('cadastrar_usuario.html')


@app.route('/cadastrar_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if current_user.perfil != 'Administrador':
        flash('Acesso negado: somente administradores podem cadastrar produtos', 'danger')
        return redirect(url_for('ver_estoque'))

    if request.method == 'POST':
        nome = request.form['nome']
        valor = round(float(request.form['valor']), 2)
        quantidade = int(request.form['quantidade'])
        quantidade_minima = int(request.form['quantidade_minima'])
        descricao = request.form['descricao']

        novo_produto = Produto(nome=nome,
                               valor=valor, quantidade=quantidade,
                               quantidade_minima=quantidade_minima,
                               descricao=descricao)
        db.session.add(novo_produto)
        db.session.commit()

        movimentacao = MovimentacaoEstoque(
            produto_id=novo_produto.id,
            quantidade=quantidade,
            tipo='entrada',
            usuario_id=current_user.id
        )
        db.session.add(movimentacao)
        db.session.commit()

        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('ver_estoque'))

    return render_template('cadastrar_produto.html')


@app.route('/estoque')
@login_required
def ver_estoque():
    produtos = Produto.query.all()

    is_admin = current_user.perfil == 'Administrador'

    return render_template('ver_estoque.html', produtos=produtos, is_admin=is_admin)


@app.route('/movimentacao/<tipo>/<int:produto_id>', methods=['POST'])
@login_required
def movimentar_estoque(tipo, produto_id):
    if current_user.perfil != 'Administrador':
        flash('Acesso negado: apenas administradores podem realizar essa ação', 'danger')
        return redirect(url_for('ver_estoque'))

    produto = Produto.query.get(produto_id)
    if not produto:
        flash('Produto não encontrado!', 'error')
        return redirect(url_for('ver_estoque'))

    if tipo == 'entrada':
        quantidade = int(request.form['quantidade'])
        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            quantidade=quantidade,
            tipo='entrada',
            usuario_id=current_user.id
        )

        db.session.add(movimentacao)
        produto.quantidade += quantidade
        flash(f'Produto {produto.nome} adicionado ao estoque com sucesso!', 'success')

    elif tipo == 'saida':
        quantidade = int(request.form['quantidade'])
        if produto.quantidade < quantidade:
            flash('Estoque insuficiente!', 'danger')
            return redirect(url_for('ver_estoque'))

        movimentacao = MovimentacaoEstoque(
            produto_id=produto.id,
            quantidade=quantidade,
            tipo='saida',
            usuario_id=current_user.id
        )
        db.session.add(movimentacao)
        produto.quantidade -= quantidade  # Atualiza a quantidade no estoque
        flash(f'Uma unidade de {produto.nome} foi retirada do estoque!', 'success')

    db.session.commit()
    return redirect(url_for('ver_estoque'))


@app.route('/editar_produto/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_produto(id):
    if current_user.perfil != 'Administrador':
        flash('Acesso negado: somente administradores podem editar produtos', 'danger')
        return redirect(url_for('ver_estoque'))

    produto = Produto.query.get(id)
    if not produto:
        flash('Produto não encontrado!', 'error')

    if request.method == 'POST':
        produto.nome = request.form['nomeForm']
        produto.descricao = request.form['descricaoForm']
        produto.valor = float(request.form['valorForm'])
        produto.quantidade_minima = int(request.form['quantidademinimaForm'])

        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('ver_estoque'))

    return render_template('editar_produto.html', produto=produto)


@app.route('/excluir_produto/<int:id>', methods=['GET', 'POST'])
@login_required
def excluir_produto(id):
    if current_user.perfil != 'Administrador':
        flash('Acesso negado: somente administradores podem excluir produtos!', 'danger')
        return redirect(url_for('ver_estoque'))

    produto = Produto.query.get_or_404(id)
    movimentacoes = MovimentacaoEstoque.query.filter_by(produto_id=produto.id).all()
    for movimentacao in movimentacoes:
        db.session.delete(movimentacao)

    db.session.delete(produto)
    db.session.commit()

    flash('Produto e suas movimentações associadas foram excluídos com sucesso', 'success')
    return redirect(url_for('ver_estoque'))


@app.route('/produtos_baixo_estoque')
@login_required
def produtos_baixo_estoque():
    produtos = get_produtos_baixo_estoque()
    return render_template('produtos_baixo_estoque.html', produtos=produtos)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
