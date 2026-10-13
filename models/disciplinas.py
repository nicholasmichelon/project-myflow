"""
models/disciplinas.py

Classe que representa uma Disciplina de um curso no MyFlow.

O __init__ usa os SETTERS para atribuir os valores, então toda validação
acontece nas properties. Dados inválidos lançam ValueError.

Regras de negócio:
- concluida NÃO é parâmetro do __init__:
  toda disciplina nasce em andamento (concluida = False)
- codigo identifica a disciplina dentro do curso (ex.: "POO-2026")
- carga_horaria é medida em horas e deve ser um inteiro maior que zero
- concluir: se já estiver concluída, retorna False e não altera nada;
  senão marca concluida = True e retorna True
- reabrir: se não estiver concluída, retorna False e não altera nada;
  senão volta concluida para False e retorna True
- sem atributo professor por enquanto
"""


class Disciplina:
    def __init__(self, nome, codigo, carga_horaria, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.carga_horaria = carga_horaria
        self.concluida = False

    # ---------------------------------------------------------
    # Property: id (None até o repositório atribuir um valor)
    # ---------------------------------------------------------
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if valor is not None and (
            not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0
        ):
            raise ValueError('id deve ser None ou um inteiro positivo')
        self._id = valor

    # ---------------------------------------------------------
    # Property: nome
    # ---------------------------------------------------------
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('nome não pode ser vazio')
        self._nome = valor.strip()

    # ---------------------------------------------------------
    # Property: codigo
    # ---------------------------------------------------------
    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('codigo não pode ser vazio')
        self._codigo = valor.strip()

    # ---------------------------------------------------------
    # Property: carga_horaria
    # ---------------------------------------------------------
    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError('carga_horaria deve ser um inteiro maior que zero')
        self._carga_horaria = valor

    # ---------------------------------------------------------
    # Property: concluida
    # ---------------------------------------------------------
    @property
    def concluida(self):
        return self._concluida

    @concluida.setter
    def concluida(self, valor):
        if not isinstance(valor, bool):
            raise ValueError('concluida deve ser True ou False')
        self._concluida = valor

    # ---------------------------------------------------------
    # Comportamentos
    # ---------------------------------------------------------
    def concluir(self):
        if self.concluida:
            return False
        self.concluida = True
        return True

    def reabrir(self):
        if not self.concluida:
            return False
        self.concluida = False
        return True

    def exibir_ficha(self):
        situacao = 'Concluída' if self.concluida else 'Em andamento'
        print(f'Disciplina: {self.nome}')
        print(f'Código: {self.codigo}')
        print(f'Carga horária: {self.carga_horaria}h')
        print(f'Situação: {situacao}')

    # ---------------------------------------------------------
    # Representação textual do objeto (usada em prints/debug)
    # ---------------------------------------------------------
    def __repr__(self):
        return (
            f'Disciplina(id={self.id!r}, nome={self.nome!r}, '
            f'codigo={self.codigo!r}, carga_horaria={self.carga_horaria!r}, '
            f'concluida={self.concluida!r})'
        )

    # ---------------------------------------------------------
    # Converte o objeto em um dicionário (útil para templates/JSON)
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'carga_horaria': self.carga_horaria,
            'concluida': self.concluida,
        }