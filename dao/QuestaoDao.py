from model.Imagem import Imagem
from model.Questao import *


class QuestaoDao:

    def __init__(self):
        db.connect()
        if not Questao.table_exists():
            db.create_tables([Questao])
        db.close()

    def questao_save(self, questao_model):
        db.connect()
        if not Questao.table_exists():
            db.create_tables([Questao])
        questao_model.save()
        db.close()

    def remove_questao(self, questao):
        db.connect()
        query = Questao.delete().where(Questao.id == questao.id)
        query2 = Imagem.delete().where(Imagem.questao_id == questao.id)
        query.execute()
        query2.execute()
        db.close()

    def questao_get_by_concurso(self, concurso):
        db.connect()
        questao = Questao.get(Questao.concurso == concurso)
        db.close()
        return questao

    def questao_get_by_enunciado(self, enunciado):
        db.connect()
        questao = Questao.get(Questao.enunciado == enunciado)
        db.close()
        return questao

    def questao_get_by_site_id(self, site_id):
        try:
            db.connect()
            questao = Questao.get(Questao.site_id == site_id)
            db.close()
            return questao
        except Exception as e:
            if not db.is_closed():
                db.close()
            return None

    def questao_paginate(self, page, per_page):
        db.connect()
        listQuestao = Questao.select().order_by(Questao.id).paginate(page, per_page)
        db.close()
        return listQuestao
