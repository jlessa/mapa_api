from model.Imagem import *


class ImagemDao:

    def __init__(self):
        db.connect()
        if not Imagem.table_exists():
            db.create_tables([Imagem])
        db.close()

    def imagem_save(self, imagem):
        db.connect()
        imagem.save()
        db.close()


    def imagem_get_by_id(self, id):
        db.connect()
        try:
            imagem = Imagem.get(Imagem.id == id)
        except Exception as e:
            print(e)
        else:
            db.close()
        return imagem

    def imagem_get_by_src(self, src):
        db.connect()
        imagem = Imagem.get(Imagem.src == src)
        db.close()
        return imagem

    def imagem_all_paginate(self, page, per_page):
        db.connect()
        listImagem = Imagem.select().order_by(Imagem.id).paginate(page, per_page)
        db.close()
        return listImagem