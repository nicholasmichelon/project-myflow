"""
models/cursos.py

Classe que representa um Curso de um usuário no MyFlow.

O __init__ usa os SETTERS para atribuir os valores, então toda validação
acontece nas properties. Dados inválidos lançam ValueError.

Regras de negócio:
- disciplinas NÃO é parâmetro do __init__:
  todo curso nasce sem disciplinas (disciplinas = [])
- nivel: "Fundamental", "Médio", "Graduação", "Pós-graduação",
  "Curso livre", "Certificação" etc.
- um curso pode ter várias disciplinas, guardadas em uma lista
- o getter de disciplinas devolve uma CÓPIA da lista: para incluir ou
  retirar disciplinas use adicionar_disciplina e remover_disciplina
- adicionar_disciplina: se já existir disciplina com o mesmo código,
  retorna False e não altera nada; senão adiciona e retorna True
- remover_disciplina: se não encontrar o código, retorna False;
  senão remove da lista e retorna True
- buscar_disciplina: retorna a Disciplina com o código informado
  ou None se não existir
- calcular_carga_horaria_total: soma a carga horária de todas as
  disciplinas do curso
- o progresso não pertence ao Curso; é individual e fica em
  ProgressoDisciplina / ProgressoDisciplinaRepository
"""

from models.disciplinas import Disciplina


class Curso:
    def __init__(self, nome, nivel, id=None):
        self.id = id
        self.nome = nome
        self.nivel = nivel
        self.disciplinas = []

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
    # Property: nivel
    # ---------------------------------------------------------
    @property
    def nivel(self):
        return self._nivel

    @nivel.setter
    def nivel(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('nivel não pode ser vazio')
        self._nivel = valor.strip()

    # ---------------------------------------------------------
    # Property: disciplinas (lista de objetos Disciplina)
    # ---------------------------------------------------------
    @property
    def disciplinas(self):
        return list(self._disciplinas)

    @disciplinas.setter
    def disciplinas(self, valor):
        if not isinstance(valor, list) or not all(
            isinstance(item, Disciplina) for item in valor
        ):
            raise ValueError('disciplinas deve ser uma lista de Disciplina')
        self._disciplinas = list(valor)

    # ---------------------------------------------------------
    # Comportamentos
    # ---------------------------------------------------------
    def adicionar_disciplina(self, disciplina):
        if not isinstance(disciplina, Disciplina):
            raise ValueError('disciplina deve ser um objeto Disciplina')
        if self.buscar_disciplina(disciplina.codigo) is not None:
            return False
        self._disciplinas.append(disciplina)
        return True

    def remover_disciplina(self, codigo):
        disciplina = self.buscar_disciplina(codigo)
        if disciplina is None:
            return False
        self._disciplinas.remove(disciplina)
        return True

    def buscar_disciplina(self, codigo):
        # O banco usa COLLATE NOCASE; a busca em memória segue a mesma regra.
        if not isinstance(codigo, str):
            return None

        codigo_normalizado = codigo.strip().casefold()

        for disciplina in self._disciplinas:
            if disciplina.codigo.casefold() == codigo_normalizado:
                return disciplina
        return None

    def calcular_carga_horaria_total(self):
        return sum(d.carga_horaria for d in self._disciplinas)

    def exibir_ficha(self):
        print(f'Curso: {self.nome}')
        print(f'Nível: {self.nivel}')
        print(f'Disciplinas: {len(self._disciplinas)}')
        print(f'Carga horária total: {self.calcular_carga_horaria_total()}h')
        for disciplina in self._disciplinas:
            print(f'  - {disciplina.codigo} | {disciplina.nome}')

    # ---------------------------------------------------------
    # Representação textual do objeto (usada em prints/debug)
    # ---------------------------------------------------------
    def __repr__(self):
        return (
            f'Curso(id={self.id!r}, nome={self.nome!r}, nivel={self.nivel!r}, '
            f'disciplinas={len(self._disciplinas)})'
        )

    # ---------------------------------------------------------
    # Converte o objeto em um dicionário (útil para templates/JSON)
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'nivel': self.nivel,
            'disciplinas': [d.to_dict() for d in self._disciplinas],
            'carga_horaria_total': self.calcular_carga_horaria_total(),
        }