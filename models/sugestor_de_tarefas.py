"""Regras simples para recomendar a próxima tarefa de estudo."""

from datetime import date


class SugestorDeTarefas:
    ORDEM_PRIORIDADE = {"alta": 0, "media": 1, "média": 1, "baixa": 2}

    def __init__(self, tempo_disponivel):
        if (
            not isinstance(tempo_disponivel, int)
            or isinstance(tempo_disponivel, bool)
            or tempo_disponivel <= 0
        ):
            raise ValueError("O tempo disponível deve ser um inteiro maior que zero.")
        self.tempo_disponivel = tempo_disponivel

    def filtrar_por_tempo(self, tarefas):
        return [
            tarefa for tarefa in tarefas
            if not tarefa.concluida
            and tarefa.duracao_estimada <= self.tempo_disponivel
        ]

    def sugerir_proxima_acao(self, tarefas, hoje=None):
        """Escolhe entre tarefas pendentes que cabem no tempo disponível.

        Prioriza tarefas atrasadas, depois prioridade declarada e prazo mais próximo.
        Em caso de empate, recomenda a tarefa mais curta.
        """
        hoje = hoje or date.today()
        candidatas = self.filtrar_por_tempo(tarefas)
        if not candidatas:
            return None

        def chave(tarefa):
            atrasada = tarefa.esta_atrasada(hoje)
            prazo = tarefa.prazo or "9999-12-31"
            prioridade = self.ORDEM_PRIORIDADE.get(tarefa.prioridade, 3)
            return (0 if atrasada else 1, prioridade, prazo, tarefa.duracao_estimada, tarefa.titulo.casefold())

        return sorted(candidatas, key=chave)[0]
