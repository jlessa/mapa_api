from flask import Flask, request, jsonify, abort
from dao.ImagemDao import ImagemDao
from dao.QuestaoDao import QuestaoDao
from mapper.mapper import Mapper

app = Flask(__name__)

@app.route('/questao', methods=['POST'])
def cria_questao():
    questaoDao = QuestaoDao()
    data = request.data
    if data:
        mapper = Mapper()
        questao = mapper.json_to_questao(data)
        # questaoDao.questao_save(questao)
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
    app.run(host='127.0.0.1', debug=True)
# [END gae_python37_app]
