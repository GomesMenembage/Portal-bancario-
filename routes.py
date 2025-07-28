from flask import request, Blueprint, jsonify 
from models import db,Banco,Servico,Admin, Filial
import google.generativeai as gemini

api = Blueprint("routes",__name__)

#ver todos os bancos
@api.route("/bancos", methods=["GET"])
def listar_bancos():
    try:
        bancos = Banco.query.all()
        resultado = [
            {
                "id": banco.id,
                "nome": banco.nome,
                "localizacao_sede": banco.localizacao_sede,
                "telefone": banco.telefone_sede,
                "email": banco.email_atendimento
            }
            for banco in bancos
        ]

        return jsonify({"bancos": resultado}), 200
    except Exception as bug:
        return jsonify({"erro": "Erro ao consultar bancos", "detalhes": str(bug)}), 500
        
#informaçoes de um banco

@api.route("/bancos/<int:id>", methods=["GET"])
def buscar_banco(id):
    try:
        banco = Banco.query.get(id)
        if not banco:
            return jsonify({"erro": "Esse banco não existe!"}), 404
        resultado = {
            "id": banco.id,
            "nome": banco.nome,
            "localizacao_sede": banco.localizacao_sede,
            "telefone": banco.telefone_sede,
            "email": banco.email_atendimento
        }

        return jsonify(resultado), 200

    except Exception as bug:
        return jsonify({"erro": "Erro ao consultar banco", "detalhes": str(bug)}), 500
        
#listar a filias de um determinado banco 

@api.route("/bancos/<int:id>/filiais", methods=["GET"])
def listar_filiais(id):
    try:
        banco = Banco.query.get(id)
        if not banco:
            return jsonify({"erro": "esse banco não existe"}), 404
        filiais = Filial.query.filter_by(banco_id=id).all()
        resultado = [
            {
                "id": filial.id,
                "nome": filial.nome,
                "localizacao": filial.localizacao,
                "telefone": filial.telefone,
                "email": filial.email
            }
            for filial in filiais
        ]

        return jsonify({"filiais": resultado}), 200
    except Exception as bug:
        return jsonify({"erro": "Erro ao consultar filiais", "detalhes": str(bug)}), 500
        
        
#detalhe de determinads filial
@api.route("/filiais/<int:id>", methods=["GET"])
def buscar_filial(id):
    try:
        filial = Filial.query.get(id)
        if not filial:
            return jsonify({"erro":"filial nao existe!!"}),404
        resultado = {
            "id": filial.id,
            "nome": filial.nome,
            "localizacao": filial.localizacao,
            "telefone":filial.telefone,
            "email": filial.email
            }
        return jsonify({"detalhes": resultado})
    except Exception as bug:
            return jsonify({"erro":"erro ao buscar detalhes", "detalhes do bug": str (bug)}),500
            
            
#ver serviços de uma filial 
@api.route("/filiais/<int:id>/servicos", methods = ["GET"])
def exibir_servicos(id):
    try:
        filial = Filial.query.get(id)
        if not filial:
            return jsonify({"erro":"essa filial nao existe"}), 404
        servicos = Servico.query.filter_by(filial_id=id).all()
        resultado = [
            {
                "id": servico.id,
                "tipo":servico.tipo
            }
            for servico in servicos
        ]
        return jsonify({"servicos": resultado})
    except Exception as bug:
        return jsonify({"erro":"erro ao obter os servicos","detalhes": str (bug)}),500
        
@api.route('/servico/status', methods=['POST'])
def get_status_servico():
    dados = request.get_json()
    if not dados or 'tipo' not in dados:
        return jsonify({'erro': 'O campo "tipo" é obrigatório'}), 400

    servico = Servico.query.filter_by(tipo=dados['tipo']).first()
    if not servico:
        return jsonify({'erro': 'Serviço não encontrado'}), 404
        
        return jsonify({'tipo': servico.tipo, 'status_servico': servico.status_servico}),200
        
 # rota do geminu
"""@api.route("/ia/apoio", methods=["POST"])
def apoio_cliente():
    try:
        dados = request.get_json()
        pergunta = dados.get("pergunta")

        if not pergunta:
            return jsonify({"erro": "Pergunta não fornecida"}), 400
            
        modelo = gemini.GenerativeModel("gemini-1.5-flash")
        response = modelo.generate_content(pergunta)

        return jsonify({"resposta": response.text}), 200

    except Exception as bug:
        return jsonify({"erro": "Erro ao processar a pergunta", "detalhes": str(bug)}), 500"""""""
        
@app.route("/ia/apoio", methods=["POST"])
def apoio_cliente():
    try:
        dados = request.get_json()
        pergunta = dados.get("Pergunta")

        if not pergunta:
            return jsonify({"erro": "Pergunta não fornecida"}), 400

        banco_nome = pergunta.lower().replace("quais serviços estão disponíveis agora no banco ", "").strip()

        banco = db.session.query(Banco).filter(Banco.nome.ilike(banco_nome)).first()

        if not banco:
            return jsonify({"erro": f"O banco '{banco_nome}' não foi encontrado no sistema."}), 404

        servicos_disponiveis = (
            db.session.query(Servico.tipo)
.filter(Servico.banco_id == banco.id, Servico.status_servico.ilike("disponivel"))
.all()
)

        if not servicos_disponiveis:
            return jsonify({"mensagem": f"Não há serviços disponíveis no banco {banco_nome}."}), 404

        lista_servicos = [servico.tipo for servico in servicos_disponiveis]
        servicos_formatados = ", ".join(lista_servicos)

        modelo = gemini.GenerativeModel("gemini-1.5-flash")
        resposta_ia = modelo.generate_content(
            f"Os seguintes serviços estão disponíveis no banco {banco_nome}: {servicos_formatados}."
)

        return jsonify({
            "banco": banco_nome,
            "servicos_disponiveis": lista_servicos,
            "resposta_ia": resposta_ia.text
}), 200

    except Exception as bug:
        return jsonify({"erro": "Erro ao processar a pergunta", "detalhes": str(bug)}), 500