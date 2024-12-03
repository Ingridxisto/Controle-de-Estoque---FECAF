from werkzeug.security import generate_password_hash
from db import db
from models_usuario import Usuario
from app import app

# Configuração do aplicativo Flask
with app.app_context():
    db.create_all()  # Cria as tabelas se ainda não existirem

    # Detalhes do administrador que será criado
    nome = "admin1"
    senha = "65437910"
    perfil = "Administrador"

    # Verifica se o administrador já existe para evitar duplicação
    if not Usuario.query.filter_by(nome=nome).first():
        # Cria uma nova instância de Administrador
        novo_usuario = Usuario(nome=nome, perfil=perfil)
        novo_usuario.senha_hash = generate_password_hash(senha)

        # Adiciona o administrador ao banco de dados
        db.session.add(novo_usuario)
        db.session.commit()
        print("Administrador criado com sucesso!")
    else:
        print("Administrador já existe no banco de dados.")

# Usuarios Comuns criados:
# Ana - 905472
# Livia - 654376

# Administradores criados:
# Ingrid Admin 240905
