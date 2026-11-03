"""Modelo de tarefa individual de um usuário do MyFlow."""

from datetime import date


class Tarefa:
    PRIORIDADES = {"alta", "media", "baixa"}

    def __init__(
        self,
        usuario_id,
        titulo,
        descricao="",
        prazo=None,
        prioridade="media",
        duracao_estimada=30,
        disciplina_id=None,
        concluida=False,
        id=None,
        criado_em=None,
        disciplina_nome=None,
    ):
        self.id = id
        self.usuario_id = usuario_id
        self.disciplina_id = disciplina_id
        self.titulo = titulo
        self.descricao = descricao
        self.prazo = prazo
        self.prioridade = prioridade
        self.duracao_estimada = duracao_estimada
        self.concluida = concluida
        self.criado_em = criado_em
        self.disciplina_nome = disciplina_nome

    @staticmethod
    def _validar_id(valor, nome, permitir_none=False):
        if permitir_none and valor is None:
            return
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError(f"{nome} deve ser um inteiro positivo")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        self._validar_id(valor, "id", permitir_none=True)
        self._id = valor

    @property
    def usuario_id(self):
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor):
        self._validar_id(valor, "usuario_id")
        self._usuario_id = valor

    @property
    def disciplina_id(self):
        return self._disciplina_id

    @disciplina_id.setter
    def disciplina_id(self, valor):
        self._validar_id(valor, "disciplina_id", permitir_none=True)
        self._disciplina_id = valor

    @property
    def titulo(self):
        return self._titulo

    @titulo.setter
    def titulo(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O título da tarefa não pode ficar vazio.")
        self._titulo = valor.strip()

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        if valor is None:
            valor = ""
        if not isinstance(valor, str):
            raise ValueError("A descrição deve ser um texto.")
        self._descricao = valor.strip()

    @property
    def prazo(self):
        return self._prazo

    @prazo.setter
    def prazo(self, valor):
        if valor in (None, ""):
            self._prazo = None
            return
        if not isinstance(valor, str):
            raise ValueError("O prazo deve ser uma data no formato AAAA-MM-DD.")
        try:
            date.fromisoformat(valor)
        except ValueError as erro:
            raise ValueError("Informe um prazo válido no formato AAAA-MM-DD.") from erro
        self._prazo = valor

    @property
    def prioridade(self):
        return self._prioridade

    @prioridade.setter
    def prioridade(self, valor):
        if not isinstance(valor, str):
            raise ValueError("Selecione uma prioridade válida.")
        normalizada = valor.strip().casefold()
        if normalizada == "média":
            normalizada = "media"
        if normalizada not in self.PRIORIDADES:
            raise ValueError("A prioridade deve ser alta, média ou baixa.")
        self._prioridade = normalizada

    @property
    def duracao_estimada(self):
        return self._duracao_estimada

    @duracao_estimada.setter
    def duracao_estimada(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("A duração estimada deve ser um inteiro maior que zero.")
        self._duracao_estimada = valor

    @property
    def concluida(self):
        return self._concluida

    @concluida.setter
    def concluida(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("concluida deve ser True ou False.")
        self._concluida = valor

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

    def esta_atrasada(self, data_atual=None):
        if self.concluida or self.prazo is None:
            return False
        data_atual = data_atual or date.today()
        if isinstance(data_atual, str):
            data_atual = date.fromisoformat(data_atual)
        return date.fromisoformat(self.prazo) < data_atual

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "disciplina_id": self.disciplina_id,
            "disciplina_nome": self.disciplina_nome,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "prazo": self.prazo,
            "prioridade": self.prioridade,
            "duracao_estimada": self.duracao_estimada,
            "concluida": self.concluida,
            "criado_em": self.criado_em,
        }

    def __repr__(self):
        return (
            f"Tarefa(id={self.id!r}, usuario_id={self.usuario_id!r}, "
            f"titulo={self.titulo!r}, prazo={self.prazo!r}, "
            f"prioridade={self.prioridade!r}, concluida={self.concluida!r})"
        )
