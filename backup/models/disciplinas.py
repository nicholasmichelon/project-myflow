"""Classe que representa uma disciplina do catálogo de um curso.

O estado de conclusão não pertence à Disciplina, porque um mesmo curso e
suas disciplinas podem ser compartilhados por vários usuários. A conclusão
individual fica em models.progresso_disciplina.ProgressoDisciplina.
"""


class Disciplina:
    def __init__(self, nome, codigo, carga_horaria, id=None):
        self.id = id
        self.nome = nome
        self.codigo = codigo
        self.carga_horaria = carga_horaria

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if valor is not None and (
            not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0
        ):
            raise ValueError("id deve ser None ou um inteiro positivo")
        self._id = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("nome não pode ser vazio")
        self._nome = valor.strip()

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("codigo não pode ser vazio")
        self._codigo = valor.strip()

    @property
    def carga_horaria(self):
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        if (
            not isinstance(valor, int)
            or isinstance(valor, bool)
            or valor <= 0
        ):
            raise ValueError(
                "carga_horaria deve ser um inteiro maior que zero"
            )
        self._carga_horaria = valor

    def exibir_ficha(self):
        print(f"Disciplina: {self.nome}")
        print(f"Código: {self.codigo}")
        print(f"Carga horária: {self.carga_horaria}h")

    def __repr__(self):
        return (
            f"Disciplina(id={self.id!r}, nome={self.nome!r}, "
            f"codigo={self.codigo!r}, "
            f"carga_horaria={self.carga_horaria!r})"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "codigo": self.codigo,
            "carga_horaria": self.carga_horaria,
        }
