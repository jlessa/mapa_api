import ast

from dao.QuestaoDao import QuestaoDao
from model.Questao import Questao
from model.Imagem import Imagem
import json
from collections import namedtuple

class Mapper:

    def json_to_questao(self, json):
        data = str(json)[int(str(json).find('{')):int(str(json).find('}')) + 1]
        dict = ast.literal_eval(data)
        return self.questao_decoder(dict)

    def questao_decoder(self, dict):
        questao = Questao()
        questao.concurso = dict['concurso']
        questao.disciplina = dict['disciplina']
        questao.assunto = dict['assunto']
        questao.subassunto = dict['subassunto']
        questao.tipo = dict['tipo']
        questao.enunciado = dict['enunciado']
        questao.op1 = dict['op1']
        questao.op2 = dict['op2']
        questao.op3 = dict['op3']
        questao.op4 = dict['op4']
        questao.op5 = dict['op5']
        questao.gabarito = dict['gabarito']
        questao.ano = dict['ano']
        questao.banca = dict['banca']
        return questao


