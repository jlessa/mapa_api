import ast

from dao.QuestaoDao import QuestaoDao
from model.Questao import Questao
from model.Imagem import Imagem
import json
from collections import namedtuple
from bs4 import BeautifulSoup

class Mapper:

    def json_to_questao(self, jsonData):
        dict = ast.literal_eval(jsonData)
        return self.questao_decoder(dict)

    def questao_decoder(self, dict):
        questao = Questao()
        questao.concurso = dict['concurso']
        questao.disciplina = dict['disciplina']
        questao.assunto = dict['assunto']
        questao.subassunto = dict['subassunto']
        questao.tipo = dict['tipo']
        questao.enunciado = self.verifica_html(dict['enunciado'])
        questao.op1 = self.verifica_html(dict['op1'])
        questao.op2 = self.verifica_html(dict['op2'])
        questao.op3 = self.verifica_html(dict['op3'])
        questao.op4 = self.verifica_html(dict['op4'])
        questao.op5 = self.verifica_html(dict['op5'])
        questao.gabarito = dict['gabarito']
        questao.ano = dict['ano']
        questao.banca = dict['banca']
        return questao

    def verifica_html(self, texto):
        valor = texto
        if len(texto) > 0:
            if bool(BeautifulSoup(texto, "html.parser").find()):
                return valor
        else:
            return valor
