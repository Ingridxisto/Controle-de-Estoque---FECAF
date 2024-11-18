from flask import flash, Blueprint, render_template, request, redirect, url_for
from models_usuario import Usuario
from models_adm import Administrador
from db import db
from flask_login import login_required, current_user
import re

cadastro_bp = Blueprint('cadastro', __name__)


def senha_valida(senha):
    return bool(re.fullmatch(r"\d{6}", senha))


@cadastro_bp.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if current_user.perfil != 'Administrador':
        flash('Acesso negado: apenas administradores podem cadastrar novos usuários', 'danger')
        return redirect(url_for('ver_estoque'))

    if request.method == 'POST':
        nome = request.form['nomeForm']
        senha_hash = request.form['senhaForm']
        perfil = request.form['perfil']

        if perfil == 'Administrador' and Administrador.query.filter_by(nome=nome).first():
            flash('Administrador com esse nome já existe!', 'error')
            return redirect(url_for('cadastro.cadastrar_usuario'))

        if perfil == 'Comum' and Usuario.query.filter_by(nome=nome).first():
            flash('Usuário com esse nome já existe!', 'error')
            return redirect(url_for('cadastro.cadastrar_usuario'))

        # Valida a senha
        if not senha_valida(senha_hash):
            flash('A senha deve ter no mínimo 6 números!', 'error')
            return redirect(url_for('cadastro.cadastrar_usuario'))

        # Verifica se o perfil é válido
        if perfil not in ['Comum', 'Administrador']:
            flash('Perfil selecionado inválido. Selecione um perfil válido.', 'error')
            return redirect(url_for('cadastro.cadastrar_usuario'))

        # Cria o usuário na tabela correspondente
        if perfil == 'Administrador':
            novo_usuario = Administrador(nome=nome, perfil=perfil)
        else:
            novo_usuario = Usuario(nome=nome, perfil=perfil)

        # Define a senha do usuário
        novo_usuario.set_senha(senha_hash)
        db.session.add(novo_usuario)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastro.cadastrar_usuario'))

    return render_template('cadastrar_usuario.html')
