from model.Questao import Questao
from model.BaseModel import *


class Imagem(BaseModel):
    id = PrimaryKeyField()
    src = TextField(null=True)
    src_site = TextField(null=True)
    tipo = TextField(null=True)
    questao_id = ForeignKeyField(Questao, backref='questao', null=True)

    @property
    def serialize(self):
        data = {
            'id': self.id,
            'src': str(self.src).strip(),
            'src_site': str(self.src_site).strip(),
            'tipo': str(self.tipo).strip(),
            # 'questao_id': self.questao_id.serialize,
        }

        return data

    def __repr__(self):
        return "{}, {}, {}, {}, {}".format(
            self.id,
            self.src,
            self.src_site,
            self.tipo,
            self.questao_id
        )
