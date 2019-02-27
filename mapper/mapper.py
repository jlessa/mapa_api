import ast
import os
import errno
import uuid
import dropbox
from dropbox.files import WriteMode
from dao.ImagemDao import ImagemDao
from dao.QuestaoDao import QuestaoDao
from model.Questao import Questao
from model.Imagem import Imagem
import re
import json
from collections import namedtuple
from bs4 import BeautifulSoup
import base64


class Mapper:

    def salva_questao(self, jsonData):
        questao_dict = ast.literal_eval(jsonData)
        questao = Questao()
        questaoDao = QuestaoDao()
        questaoDao.questao_save(questao)
        self.preenche_questao(questao_dict, questao)
        questaoDao.questao_save(questao)

    def preenche_questao(self, dict, questao):
        questao.concurso = dict['concurso']
        questao.disciplina = dict['disciplina']
        questao.assunto = dict['assunto']
        questao.subassunto = dict['subassunto']
        questao.tipo = dict['tipo']
        questao.enunciado = self.preenche_html(dict['enunciado'], questao, tipo='enunciado')
        questao.op1 = self.preenche_html(dict['op1'], questao)
        questao.op2 = self.preenche_html(dict['op2'], questao)
        questao.op3 = self.preenche_html(dict['op3'], questao)
        questao.op4 = self.preenche_html(dict['op4'], questao)
        questao.op5 = self.preenche_html(dict['op5'], questao)
        questao.gabarito = dict['gabarito']
        questao.ano = dict['ano']
        questao.banca = dict['banca']
        return questao

    def preenche_html(self, texto, questao, tipo='opcao'):
        if len(texto) > 0:
            soap = BeautifulSoup(texto, "html.parser")
            if bool(soap.find()):
                if self.teste_imagem(soap):
                    return self.pega_texto_com_imagem(soap, questao, tipo)
                else:
                    return self.pega_texto(soap)
            else:
                return texto
        else:
            return texto

    def teste_imagem(self, html):
        if html.find("img"):
            return True
        else:
            return False

    def pega_texto(self, html):
        return html.text.strip()

    def pega_texto_com_imagem(self, html, questao, tipo):
        texto = html.prettify()
        # regex_img_tag = '<img(.|\n)*?\/>'
        imagens = html.findAll('img')
        for imagem in imagens:
            texto = texto.replace(imagem.prettify(), self.pega_imagem(imagem, questao, tipo))
        return BeautifulSoup(texto).text.strip().replace('\n\n\n', '\n').replace('\n\n', '\n')

    def pega_imagem(self, html, questao, tipo):
        # imagens = html.findAll('img')
        valor = ''
        caminho = '.\\imagem\\Criadas\\'
        # for imagemHtml in imagens:
        imagemDao = ImagemDao()
        imagem = Imagem()
        # if 'data:image' in imagemHtml['src']:
        if 'data:image' in html.prettify():
        #     head, data = imagemHtml['src'].split(',', 1)
            head, data = html['src'].split(',', 1)
            file_ext = head.split(';')[0].split('/')[1]
            nome_arquivo = str(uuid.uuid4()) + '.' + file_ext
        # self.cria_imagem(caminho + nome_arquivo, imagemHtml['src'])
        self.cria_imagem(caminho + nome_arquivo, html['src'])
        imagem.src_site = caminho + nome_arquivo
        imagem.src = self.upload_dropbox(caminho + nome_arquivo)
        imagem.questao_id = questao
        imagem.tipo = tipo
        imagemDao.imagem_save(imagem)
        valor = '##imagem:$' + str(imagem.id) + "$##"
        return valor



    def cria_imagem(self, nome_arquivo, url):
        if not os.path.exists(os.path.dirname(nome_arquivo)):
            try:
                os.makedirs(os.path.dirname(nome_arquivo))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        if 'data:image' in url:
            head, data = url.split(',', 1)
            # Get the file extension (gif, jpeg, png)
            file_ext = head.split(';')[0].split('/')[1]
            # Decode the image data
            plain_data = base64.b64decode(data)
            # Write the image to a file
            with open(nome_arquivo, 'wb') as f:
                f.write(plain_data)

    def upload_dropbox(self, file_path):
        access_token = 'uQcheOwxdcAAAAAAAAAAI1x6fd-1DxAVsfWAXKFOWxhwd32wH-liWmJuB6JeUQV8'
        dbx = dropbox.Dropbox(access_token)
        # print('linked account: ', dbx.users_get_account())
        print('###### Fazendo Upload da imagem: ' + file_path)
        f = open(file_path, 'rb')
        upload = dbx.files_upload(f.read(), file_path[1:].replace('\\', '/'), mode=WriteMode('overwrite'))
        try:
            link = dbx.sharing_create_shared_link_with_settings(upload.path_lower)
        except Exception as e:
            link = 'teste'
        print('#### Link de Upload: ' + link.url)
        return link.url
