"""
models/usuarios.py

Classe que representa um Usuário do MyFlow, criado a partir do cadastro
em três etapas (jornada, objetivo e tempo disponível).

O __init__ usa os SETTERS para atribuir os valores, então toda validação
acontece nas properties. Dados inválidos lançam ValueError.

Regras de negócio:
- curso NÃO é parâmetro do __init__:
  todo usuário nasce sem curso (curso = None)
- cada usuário tem apenas um curso
- jornada: onde o usuário está na vida de estudos
  (ex.: "Graduação", "Ensino Médio", "Estudo independente")
- email deve conter "@"
- tempo_disponivel é medido em minutos e deve ser um inteiro maior que zero
- definir_curso: se o usuário já tiver curso, retorna False e não
  altera nada; senão grava o curso e retorna True
- remover_curso: se o usuário não tiver curso, retorna False;
  senão volta curso para None e retorna True
- atualizar_tempo_disponivel: se o valor for inválido, retorna False e
  não altera nada; senão grava o novo valor e retorna True
"""

from models.cursos import Curso


class Usuario:
    def __init__(self, nome, email, jornada, objetivo, tempo_disponivel, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.jornada = jornada
        self.objetivo = objetivo
        self.tempo_disponivel = tempo_disponivel
        self.curso = None

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
    # Property: email
    # ---------------------------------------------------------
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('email não pode ser vazio')
        if '@' not in valor:
            raise ValueError('email deve conter "@"')
        self._email = valor.strip()

    # ---------------------------------------------------------
    # Property: jornada
    # ---------------------------------------------------------
    @property
    def jornada(self):
        return self._jornada

    @jornada.setter
    def jornada(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('jornada não pode ser vazia')
        self._jornada = valor.strip()

    # ---------------------------------------------------------
    # Property: objetivo
    # ---------------------------------------------------------
    @property
    def objetivo(self):
        return self._objetivo

    @objetivo.setter
    def objetivo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError('objetivo não pode ser vazio')
        self._objetivo = valor.strip()

    # ---------------------------------------------------------
    # Property: tempo_disponivel (em minutos)
    # ---------------------------------------------------------
    @property
    def tempo_disponivel(self):
        return self._tempo_disponivel

    @tempo_disponivel.setter
    def tempo_disponivel(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError('tempo_disponivel deve ser um inteiro maior que zero')
        self._tempo_disponivel = valor

    # ---------------------------------------------------------
    # Property: curso (None ou um objeto Curso)
    # ---------------------------------------------------------
    @property
    def curso(self):
        return self._curso

    @curso.setter
    def curso(self, valor):
        if valor is not None and not isinstance(valor, Curso):
            raise ValueError('curso deve ser None ou um objeto Curso')

        curso_atual = getattr(self, "_curso", None)
        if curso_atual is not None and valor is not None and valor is not curso_atual:
            raise ValueError(
                'O usuário já possui um curso. Use remover_curso() antes de trocar.'
            )

        self._curso = valor

    # ---------------------------------------------------------
    # Comportamentos
    # ---------------------------------------------------------
    def definir_curso(self, curso):
        if self.curso is not None:
            return False
        self.curso = curso
        return True

    def remover_curso(self):
        if self.curso is None:
            return False
        self.curso = None
        return True

    def atualizar_tempo_disponivel(self, minutos):
        try:
            self.tempo_disponivel = minutos
        except ValueError:
            return False
        return True

    def exibir_ficha(self):
        print(f'Usuário: {self.nome}')
        print(f'E-mail: {self.email}')
        print(f'Jornada: {self.jornada}')
        print(f'Objetivo: {self.objetivo}')
        print(f'Tempo disponível: {self.tempo_disponivel} min')
        print(f'Curso: {self.curso.nome if self.curso else "Sem curso"}')

    # ---------------------------------------------------------
    # Representação textual do objeto (usada em prints/debug)
    # ---------------------------------------------------------
    def __repr__(self):
        nome_curso = self.curso.nome if self.curso else None
        return (
            f'Usuario(id={self.id!r}, nome={self.nome!r}, email={self.email!r}, '
            f'jornada={self.jornada!r}, objetivo={self.objetivo!r}, '
            f'tempo_disponivel={self.tempo_disponivel!r}, curso={nome_curso!r})'
        )

    # ---------------------------------------------------------
    # Converte o objeto em um dicionário (útil para templates/JSON)
    # ---------------------------------------------------------
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'jornada': self.jornada,
            'objetivo': self.objetivo,
            'tempo_disponivel': self.tempo_disponivel,
            'curso': self.curso.to_dict() if self.curso else None,
        }