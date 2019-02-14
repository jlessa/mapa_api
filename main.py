# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, request, jsonify, abort


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
from dao.QuestaoDao import QuestaoDao

app = Flask(__name__)

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


@app.route('/')
def hello():
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
