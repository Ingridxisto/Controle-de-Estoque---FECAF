from werkzeug.security import generate_password_hash
from db import db
from models_adm import Administrador
from app import app

# Configuração do aplicativo Flask
with app.app_context():
    db.create_all()  # Cria as tabelas se ainda não existirem

    # Detalhes do administrador que será criado
    nome = "admin1"
    senha = "65437910"
    perfil = "Administrador"

    # Verifica se o administrador já existe para evitar duplicação
    if not Administrador.query.filter_by(nome=nome).first():
        # Cria uma nova instância de Administrador
        novo_admin = Administrador(nome=nome, perfil=perfil)
        novo_admin.senha_hash = generate_password_hash(senha)

        # Adiciona o administrador ao banco de dados
        db.session.add(novo_admin)
        db.session.commit()
        print("Administrador criado com sucesso!")
    else:
        print("Administrador já existe no banco de dados.")

# comum- Ana 905472
# Ingrid Admin 240905