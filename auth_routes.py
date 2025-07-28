from flask import request , Blueprint, jsonify 
from models import db,Banco, Filial,Admin,Servico

API = Blueprint("auth_routes",__name__)

@API.route("/admin/register", methods=["POST"])
def register_admin():
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    if Admin.query.filter_by(email=email).first():
        return jsonify({"error":"Esse administrador já existe!"}), 400

    novo_admin = Admin(nome=nome, email=email, senha=senha)
    db.session.add(novo_admin)
    db.session.commit()

    return jsonify({"sucesso":"Administrador registrado com sucesso!"})
    
 #login
@API.route("/admin/login", methods=["POST"])
def login_admin():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    admin = Admin.query.filter_by(email=email, senha=senha).first()

    if admin:
        return jsonify(mensagem="Login bem-sucedido"),200

    return jsonify({"erro":"Usuário ou senha incorretos!"}), 401
    
    
#add banco
@API.route("/bancos", methods=["POST"])
def adicionar_banco():
    try:
        dados = request.get_json()
        nome = dados.get("nome")
        localizacao_sede = dados.get("localizacao_sede")
        email_atendimento = dados.get("email_atendimento")
        telefone_sede = dados.get("telefone_sede")

        if not nome or not localizacao_sede or not email_atendimento or not telefone_sede:
            return jsonify({"erro": "preenche todos os camps"}), 400

        novo_banco = Banco(
            nome=nome,
            localizacao_sede=localizacao_sede,
            email_atendimento=email_atendimento,
            telefone_sede=telefone_sede
        )

        db.session.add(novo_banco)
        db.session.commit()

        return jsonify({"sucesso": "Banco adicionado", "banco_id": novo_banco.id}), 201

    except Exception as bug:
        return jsonify({"erro": "Erro ao registar banco", "detalhes": str(bug)}), 500
    
    
#add filial
@API.route("/bancos/<int:id>/filiais", methods=["POST"])
def adicionar_filial(id):
    try:
        banco = Banco.query.get(id)
        if not banco:
            return jsonify({"erro": "Banco não existe."}), 404

        dados = request.get_json()
        nome = dados.get("nome")
        localizacao = dados.get("localizacao")
        email = dados.get("email")
        telefone = dados.get("telefone")

        if not nome or not localizacao or not email or not telefone:
            return jsonify({"erro": "preenche todos os campos "}), 400

        nova_filial = Filial(
            nome=nome,
            localizacao=localizacao,
            email=email,
            telefone=telefone,
            banco_id=id
        )

        db.session.add(nova_filial)
        db.session.commit()

        return jsonify({"sucesso": "Filial adicionwda", "filial_id": nova_filial.id}), 201

    except Exception as bug:
        return jsonify({"erro": "Erro ao cadastrar ", "detalhes": str(bug)}), 500
    
    
# add service a filial
@API.route("/filiais/<int:id>/servicos", methods=["POST"])
def adicionar_servico(id):
    try:
        filial = Filial.query.get(id)
        if not filial:
            return jsonify({"erro": "Filial não existe"}), 404

        dados = request.get_json()
        tipo = dados.get("tipo")
        status_servico = dados.get("status_servico", "disponivel")

        if not tipo:
            return jsonify({"erro": "digite o tipo de serviço"}), 400

        novo_servico = Servico(
            tipo=tipo,
            status_servico=status_servico,
            filial_id=id,
            banco_id=filial.banco_id
        )

        db.session.add(novo_servico)
        db.session.commit()

        return jsonify({"sucesso": "Serviço registado ", "servico_id": novo_servico.id}), 201

    except Exception as bug:
        return jsonify({"erro": "Erro ao cadastrar serviço", "detalhes": str(bug)}), 500
    
@API.route('/servicos/<int:id>', methods=['PATCH'])
def atualizar_status_servico(id):
    servico = Servico.query.get(id)
    if not servico:
        return jsonify({"erro": "Serviço não encontrado"}), 404

    dados = request.json
    if "status_servico" in dados:
        servico.status_servico = dados["status_servico"]
        db.session.commit()
        return jsonify({"mensagem": "Status do serviço atualizado com sucesso", "servico": {"id": servico.id, "tipo": servico.tipo, "status_servico": servico.status_servico}}), 200

    return jsonify({"erro": "Nenhum status fornecido"}), 400
    
#endpoins delete
#delete one bank
@API.route("/bancos/<int:id>", methods=["DELETE"])
def remover_banco(id):
    try:
        banco = Banco.query.get(id)
        if not banco:
            return jsonify({"erro": "Banco não existe"}), 404

        db.session.delete(banco)
        db.session.commit()

        return jsonify({"sucesso": "Banco apafado"}), 200
    except Exception as bug:
        return jsonify({"erro":"não deu pra apagar o banco","detalhes": str(bug)}),500
    
#delete filial
@API.route("/filiais/<int:id>", methods=["DELETE"])
def remover_filial(id):
    try:
        filial = Filial.query.get(id)
        if not filial:
            return jsonify({"erro": "Filial não existe"}), 404

        db.session.delete(filial)
        db.session.commit()

        return jsonify({"sucesso": "Filial apagada"}), 200

    except Exception as bug:
        return jsonify({"erro": "Erro ao apagar", "detalhes": str(bug)}), 500
    
#delete service
@API.route("/servicos/<int:id>", methods=["DELETE"])
def remover_servico(id):
    try:
        servico = Servico.query.get(id)
        if not servico:
            return jsonify({"erro": "Serviço não existe"}), 404

        db.session.delete(servico)
        db.session.commit()

        return jsonify({"sucesso": "Serviço apagado"}), 200

    except Exception as bug:
        return jsonify({"erro": "Erro ao apagar", "detalhes": str(bug)}), 500
        