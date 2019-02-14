from model.BaseModel import *


class Questao(BaseModel):
    id = PrimaryKeyField()
    site_id = TextField(null=True)
    concurso = TextField(null=True)
    disciplina = TextField(null=True)
    assunto = TextField(null=True)
    subassunto = TextField(null=True)
    tipo = TextField(null=True)
    codigo = TextField(null=True)
    enunciado = TextField(null=True)
    op1 = TextField(null=True)
    op2 = TextField(null=True)
    op3 = TextField(null=True)
    op4 = TextField(null=True)
    op5 = TextField(null=True)
    gabarito = TextField(null=True)
    ano = TextField(null=True)
    banca = TextField(null=True)
    texto_opcoes = TextField(null=True)

    def set_opcoes(self, lista_opcoes, gabarito, cespe=False):
        self.gabarito = gabarito
        self.texto_opcoes = ''

        if gabarito.upper().strip() == 'X':
            self.texto_opcoes = 'ANULADO'
            gabarito = 'A'
        else:
            for opcoes in lista_opcoes:
                self.texto_opcoes += opcoes + '##$##'

        if not cespe:
            # gabarito sempre na primeira posicao
            indice = ['A', 'B', 'C', 'D', 'E'].index(gabarito.upper().strip())
            if indice >= len(lista_opcoes):
                # Gabarito incorreto no site
                indice = 0
                self.gabarito = 'N'

            self.op1 = lista_opcoes[indice]
            lista_opcoes.pop(indice)
            for i, item in enumerate(lista_opcoes):
                if i == 0:
                    self.op2 = lista_opcoes[i]
                if i == 1:
                    self.op3 = lista_opcoes[i]
                if i == 2:
                    self.op4 = lista_opcoes[i]
                if i == 3:
                    self.op5 = lista_opcoes[i]

        else:
            if gabarito == 'C':
                self.op1 = lista_opcoes[0]
                self.op2 = lista_opcoes[1]
            else:
                self.op1 = lista_opcoes[1]
                self.op2 = lista_opcoes[0]

    @property
    def serialize(self):
        data = {
            'site_id': self.site_id,
            'concurso': str(self.concurso).strip(),
            'disciplina': str(self.disciplina).strip(),
            'assunto': str(self.assunto).strip(),
            'subassunto': str(self.subassunto).strip(),
            'tipo': str(self.tipo).strip(),
            'codigo': str(self.codigo).strip(),
            'enunciado': str(self.enunciado).strip(),
            'op1': str(self.op1).strip(),
            'op2': str(self.op2).strip(),
            'op3': str(self.op3).strip(),
            'op4': str(self.op4).strip(),
            'op5': str(self.op5).strip(),
            'gabarito': str(self.gabarito).strip(),
            'ano': str(self.ano).strip(),
            'banca': str(self.banca).strip(),
            'texto_opcoes': str(self.texto_opcoes).strip(),
        }

        return data

    def __repr__(self):
        return "{}, {}, {}, {}, {},{}, {}, {}, {}, {},{}, {}, {}, {}, {},{}, {}, {}".format(
            self.id,
            self.site_id,
            self.concurso,
            self.disciplina,
            self.assunto,
            self.subassunto,
            self.tipo,
            self.codigo,
            self.enunciado,
            self.op1,
            self.op2,
            self.op3,
            self.op4,
            self.op5,
            self.gabarito,
            self.ano,
            self.banca,
            self.texto_opcoes
        )
