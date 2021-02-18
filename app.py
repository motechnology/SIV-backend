# -*- coding: utf-8 -*-

from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
cors = CORS(app)

ENV = 'nodev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
else: 
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQL_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Vegetal(db.Model):
    __tablename__ = 'vegetal'
    nome = db.Column(db.String(200), primary_key=True)
    tempideal = db.Column(db.Float)
    umidadeideal = db.Column(db.Float)

    def __init__(self, nome, tempideal, umidadeideal):
        self.nome = nome
        self.tempideal = tempideal
        self.umidadeideal = umidadeideal

class Vaso(db.Model):
    __tablename__ = 'vaso'
    id = db.Column(db.Integer, primary_key=True)
    nomevegetal = db.Column(db.String(200))
    bomba = db.Column(db.Integer)
    tempo = db.Column(db.Integer)
    status = db.Column(db.Integer)
    ultimabomba = db.Column(db.String(200))


    def __init__(self, nomevegetal, bomba, tempo, status, ultimabomba):
        self.nomevegetal = nomevegetal
        self.bomba = bomba
        self.tempo = tempo
        self.status = status
        self.ultimabomba = ultimabomba
        
class Informacao(db.Model):
    __table__name = 'informacao'

    id = db.Column(db.Integer, primary_key=True)
    nomevegetal = db.Column(db.String(200))
    umidade = db.Column(db.Float)
    temperatura = db.Column(db.Float)
    idvaso = db.Column(db.Integer)
    data = db.Column(db.String(200))


    def __init__(self, nomeVegetal, umidade, temperatura, idVaso, data):
        self.nomevegetal = nomeVegetal
        self.umidade = umidade
        self.temperatura = temperatura
        self.idvaso = idVaso
        self.data = data


# App mobile realiza para obter lista de vegetais cadastrados
@app.route('/', methods=['GET'])
def index():
    return 'Projeto SIV'


# App mobile realiza para obter lista de vegetais cadastrados
@app.route('/vegetal', methods=['GET'])
def obtem_vegetal():
    
    # Lista de vegetais
    lista_vegetais = []
    
    try:
        for vegetal in db.session.query(Vegetal).all():
            lista_vegetais.append({"nome": vegetal.nome, "tempIdeal": vegetal.tempideal, 
                "umidadeIdeal": vegetal.umidadeideal})
        return jsonify({'lista_vegetais': lista_vegetais})
    except:
        return make_response(jsonify('Erro ao retornar lista de vegetal!'), 406)


# App mobile realiza para cadastrar novo vegetal
@app.route('/vegetal', methods=['POST'])
def cadastra_vegetal():
    
    # Leitura dos parâmetros recebidos
    nome = request.json.get('nome')
    tempIdeal = request.json.get('tempIdeal')
    umidadeIdeal = request.json.get('umidadeIdeal')

    try:
        vegetal = Vegetal(nome, tempIdeal, umidadeIdeal)
        db.session.add(vegetal)
        db.session.commit()
        return make_response(jsonify('Vegetal cadastrado!'), 201)
    except:
        return make_response(jsonify('Vegetal não cadastrado!'), 406)


# App mobile realiza para alterar vegetal cadastrado
@app.route('/vegetal', methods=['PUT'])
def altera_vegetal():

     # Leitura dos parâmetros recebidos
    nome = request.json.get('nome')
    tempIdeal = request.json.get('tempIdeal')
    umidadeIdeal = request.json.get('umidadeIdeal')

    try:
        db.session.query(Vegetal).filter(Vegetal.nome == nome).update({"umidadeideal": umidadeIdeal, "tempideal": tempIdeal})
        db.session.commit()
        return make_response(jsonify('Vegetal atualizado!'), 201)
    except Exception as e:
        return make_response(jsonify('Vegetal não atualizado!'), 406)


# App mobile realiza para deletar vegetal cadastrado
@app.route('/vegetal', methods=['DELETE'])
def deleta_vegetal():

    # Leitura dos parâmetros recebidos
    nome = request.json.get('nome')
    
    try:
        db.session.query(Vegetal).filter(Vegetal.nome == nome).delete()
        db.session.commit()
        return make_response(jsonify('Vegetal excluído!'), 200)
    except Exception as e:
        return make_response(jsonify('Não foi possível excluir o vegetal!'), 406)


# App mobile realiza para obter o estado dos vasos
@app.route('/vaso', methods=['GET'])
def obtem_vaso():

    # Lista de vegetais
    lista_vasos = []

    try:
        for vaso in db.session.query(Vaso).order_by(Vaso.id.desc()):
            lista_vasos.append({"id": vaso.id, "status": vaso.status, "bomba": vaso.bomba,
                                "tempo": vaso.tempo, "ultimaBomba": vaso.ultimabomba, "vegetal": vaso.nomevegetal})

        return jsonify({'lista_vasos': lista_vasos})
    except:
        return make_response(jsonify('Erro ao retornar lista de vasos!'), 406)


# App mobile realiza para alterar o estado dos vasos (Informa o vegetal)
@app.route('/vaso', methods=['PUT'])
def altera_vaso():
    
    # Leitura dos parâmetros recebidos
    idVaso = request.json.get('idVaso')
    nomeVegetal = request.json.get('nomeVegetal')

    try:
        db.session.query(Vaso).filter(Vaso.id == idVaso).update({"nomevegetal": nomeVegetal, "status": 1})
        db.session.commit()
        return make_response(jsonify('Vaso atualizado!'), 201)
    except Exception as e:
        return make_response(jsonify('Vaso não atualizado!'), 406)


# App mobile realiza para desligar os vasos
@app.route('/vaso', methods=['DELETE'])
def desliga_vaso():
    
    # Leitura dos parâmetros recebidos
    idVaso = request.json.get('idVaso')

    try:
        db.session.query(Vaso).filter(Vaso.id == idVaso).update({"nomevegetal": None, "status": 0})
        db.session.commit()
        return make_response(jsonify('Vaso desligado!'), 201)
    except Exception as e:
        return make_response(jsonify('Não foi possível desligar o vaso!'), 406)


# App mobile realiza para ligar a bomba dos vasos
@app.route('/bomba', methods=['PUT'])
def ativa_bomba():
    
    # Leitura dos parâmetros recebidos
    idVaso = request.json.get('idVaso')
    tempo = request.json.get('tempo')
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
  
    try:
        db.session.query(Vaso).filter(Vaso.id == idVaso).update({"tempo": tempo, "bomba": "1", "ultimabomba": data})
        db.session.commit()
        return make_response(jsonify('A bomba será ativada!'), 201)
    except Exception as e:
        return make_response(jsonify('Erro ao ativar bomba!'), 406)


# App mobile realiza para obter dados do banco
@app.route('/informacao', methods=['GET'])
def obtem_info():

    # Lista de informação
    lista_info = []

    try:
        for info in db.session.query(Informacao).order_by(Informacao.id.desc()).all():
            lista_info.append({"idVaso": info.idvaso, "nomeVegetal": info.nomevegetal, 
                "temperatura": info.temperatura, "umidade": info.umidade, "data": info.data})
        return jsonify({'lista_info': lista_info})
    except:
        return make_response(jsonify('Erro ao retornar lista de informações!'), 406)


# Nodemcu realiza para verificar se deve ligar a bomba
@app.route('/bomba', methods=['GET'])
def liga_bomba():
   
    # Consultando os dois objetos Vaso no banco
    vasos = db.session.query(Vaso).order_by(Vaso.id.desc()).all()
    vaso1 = vasos[1]
    vaso2 = vasos[0]

    res = {"tempo1": vaso1.tempo, "ultimaBomba1": vaso1.ultimabomba, 
                    "tempo2": vaso2.tempo, "ultimaBomba2": vaso2.ultimabomba}

    # Atualizando o banco
    db.session.query(Vaso).update({"tempo": "0", "bomba": "0"})
    db.session.commit()

    return jsonify(res)


# Nodemcu realiza para verificar qual vaso está ativo
@app.route('/ativo', methods=['GET'])
def vaso_ativo():
 
    # Consultando os dois objetos Vaso no banco
    vasos = db.session.query(Vaso).order_by(Vaso.id.desc()).all()
    vaso1 = vasos[1]
    vaso2 = vasos[0]

    return jsonify({"idVaso1": vaso1.status, "idVaso2": vaso2.status})


# Nodemcu realiza para inserir informação no banco
@app.route('/informacao', methods=['POST'])
def add_info():

    # Leitura dos parâmetros recebidos
    idVaso = request.json.get('idVaso')
    temperatura = request.json.get('t')
    umidade = request.json.get('u')
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Consultando o Vaso no banco
    consulta = db.session.query(Vaso).filter(Vaso.id == idVaso)
    vaso = consulta[0]

    if vaso.status == 1:  # O vegetal do vaso deve existir
        # Criando objeto Informacao
        info = Informacao(vaso.nomevegetal, umidade, temperatura, idVaso, data)
        
        if verifica_medidas(idVaso, temperatura, umidade, vaso.nomevegetal, data):  # Analisando situação do vegetal
            db.session.add(info)
            db.session.commit()
            return make_response(jsonify('Objeto cadastrado, a bomba será acionada!'), 200)
        else:
            db.session.add(info)
            db.session.commit()
            return make_response(jsonify('Objeto cadastrado!'), 200)
    else:
        return make_response(jsonify('O Vaso não está ativo!'), 406)


# Verifica se precisa acionar a bomba e adiciona na lista de bomba
def verifica_medidas(idVaso, temperatura, umidade, nomeVegetal, data):
    
    res = False
 
    # Consultando o Vaso no banco
    consulta = db.session.query(Vegetal).filter(Vegetal.nome == nomeVegetal)
    vegetal = consulta[0]

    if float(temperatura) > 2 * float(vegetal.tempideal) and float(umidade) < 0.8 * float(vegetal.umidadeideal):
        db.session.query(Vaso).filter(Vaso.id == idVaso).update({"tempo": "5", "bomba": "1", "ultimabomba": data})
        db.session.commit()
        res = True

    return res


if __name__ == "__main__":
    app.debug = True
    app.run()


    

    
