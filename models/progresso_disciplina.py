"""Modelo de progresso de uma disciplina para um usuário específico.

O progresso é separado do cadastro da disciplina, pois vários usuários podem
compartilhar o mesmo curso sem compartilhar suas conclusões.
"""


class ProgressoDisciplina:
    def __init__(self, usuario_id, disciplina_id, concluida=False):
        self.usuario_id = usuario_id
        self.disciplina_id = disciplina_id
        self.concluida = concluida

    @staticmethod
    def _validar_id(valor, nome):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError(f"{nome} deve ser um inteiro positivo")

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
        self._validar_id(valor, "disciplina_id")
        self._disciplina_id = valor

    @property
    def concluida(self):
        return self._concluida

    @concluida.setter
    def concluida(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("concluida deve ser True ou False")
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

    def to_dict(self):
        return {
            "usuario_id": self.usuario_id,
            "disciplina_id": self.disciplina_id,
            "concluida": self.concluida,
        }

    def __repr__(self):
        return (
            f"ProgressoDisciplina(usuario_id={self.usuario_id!r}, "
            f"disciplina_id={self.disciplina_id!r}, "
            f"concluida={self.concluida!r})"
        )
