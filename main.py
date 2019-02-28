import os
from flask import Flask, request, jsonify, abort
from dao.ImagemDao import ImagemDao
from dao.QuestaoDao import QuestaoDao
from mapper.mapper import Mapper
from flask_cors import CORS
import ast
import json

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/questao', methods=['POST'])
def cria_questao():
    data = request.json['data']
    if len(ast.literal_eval(data)['enunciado']) == 0:
        output = {
            "error": "Questão Vazia",
            "url": request.url,
        }
        res = jsonify(output)
        res.status_code = 401
    else:
        if data:
            mapper = Mapper()
            questao = mapper.salva_questao(data)
            output = {
                "ok": "Sucesso",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 200
        else:
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
    return res

@app.route('/questao', methods=['GET'])
def get_questoes(page=1):
    if request.method == 'GET':
        per_page = 10
        questaoDao = QuestaoDao()
        questaoList = questaoDao.questao_paginate(page, per_page)
        data = [questao.serialize for questao in questaoList]
        if data:
            res = jsonify({
                'questao': data,
                'meta': {
                   'page': page,
                   'per_page': per_page,
                   'page_url': request.url}
                })
            res.status_code = 200
        else:
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

@app.route('/imagem/<int:image_id>', methods=['GET'])
def get_imagem(image_id):
    if request.method == 'GET':
        imagemDao = ImagemDao()
        imagem = imagemDao.imagem_get_by_id(int(image_id))
        data = imagem.serialize
        if data:
            res = jsonify({
                'imagem': data,
                'meta': {
                   'page_url': request.url}
                })
            res.status_code = 200
        else:
            output = {
                "error": "No results found. Check url again",
                "url": request.url,
            }
            res = jsonify(output)
            res.status_code = 404
        return res

@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # app.run(host='127.0.0.1', debug=True)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
# [END gae_python37_app]
