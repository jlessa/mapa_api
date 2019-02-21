from model.Imagem import Imagem
from model.Questao import *


class QuestaoDao:

    def __init__(self):
        try:
            db.connect()
            if not Questao.table_exists():
                db.create_tables([Questao])
            # db.close()
        except Exception as e:
            print(e)
        finally:
            if not db.is_closed():
                db.close()

    def questao_save(self, questao_model):
        try:
            db.connect()
            if not Questao.table_exists():
                db.create_tables([Questao])
            questao_model.save()
        except Exception as e:
            print('e')
        finally:
            db.close()

    def remove_questao(self, questao):
        try:
            db.connect()
            query = Questao.delete().where(Questao.id == questao.id)
            query2 = Imagem.delete().where(Imagem.questao_id == questao.id)
            query.execute()
            query2.execute()
        except Exception as e:
            print('e')
        finally:
            db.close()

    def questao_get_by_concurso(self, concurso):
        try:
            db.connect()
            questao = Questao.get(Questao.concurso == concurso)
        except Exception as e:
            print('e')
        finally:
            db.close()
        return questao

    def questao_get_by_enunciado(self, enunciado):
        try:
            db.connect()
            questao = Questao.get(Questao.enunciado == enunciado)
        except Exception as e:
            print('e')
        finally:
            db.close()
        return questao

    def questao_get_by_site_id(self, site_id):
        try:
            db.connect()
            questao = Questao.get(Questao.site_id == site_id)
            return questao
        except Exception as e:
            print(e)
            return None
        finally:
            if not db.is_closed():
                db.close()


    def questao_paginate(self, page, per_page):
        try:
            db.connect()
            listQuestao = Questao.select().order_by(Questao.id).paginate(page, per_page)
        except Exception as e:
            print('e')
        finally:
            db.close()

        return listQuestao
