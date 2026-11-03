"""Persistência das tarefas individuais dos usuários."""

import sqlite3

from database.conexao import obter_conexao
from models.tarefa import Tarefa


class TarefaRepository:
    def _linha_para_objeto(self, linha):
        tarefa = Tarefa(
            id=linha["id"],
            usuario_id=linha["usuario_id"],
            disciplina_id=linha["disciplina_id"],
            titulo=linha["titulo"],
            descricao=linha["descricao"] or "",
            prazo=linha["prazo"],
            prioridade=linha["prioridade"],
            duracao_estimada=linha["duracao_estimada"],
            concluida=bool(linha["concluida"]),
            criado_em=linha["criado_em"],
            disciplina_nome=linha["disciplina_nome"],
        )
        return tarefa

    def _validar_disciplina_do_usuario(self, conexao, usuario_id, disciplina_id):
        if disciplina_id is None:
            return
        linha = conexao.execute(
            """
            SELECT 1
            FROM usuarios u
            JOIN disciplinas d ON d.curso_id = u.curso_id
            WHERE u.id = ? AND d.id = ?
            """,
            (usuario_id, disciplina_id),
        ).fetchone()
        if linha is None:
            raise ValueError("Selecione uma disciplina do seu curso.")

    def criar(self, tarefa):
        conexao = obter_conexao()
        try:
            self._validar_disciplina_do_usuario(
                conexao, tarefa.usuario_id, tarefa.disciplina_id
            )
            cursor = conexao.execute(
                """
                INSERT INTO tarefas (
                    usuario_id, disciplina_id, titulo, descricao, prazo,
                    prioridade, duracao_estimada, concluida
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tarefa.usuario_id,
                    tarefa.disciplina_id,
                    tarefa.titulo,
                    tarefa.descricao,
                    tarefa.prazo,
                    tarefa.prioridade,
                    tarefa.duracao_estimada,
                    int(tarefa.concluida),
                ),
            )
            conexao.commit()
            tarefa.id = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError(f"Não foi possível salvar a tarefa: {erro}") from erro
        finally:
            conexao.close()

    def listar_do_usuario(self, usuario_id, incluir_concluidas=True):
        conexao = obter_conexao()
        try:
            sql = """
                SELECT t.*, d.nome AS disciplina_nome
                FROM tarefas t
                LEFT JOIN disciplinas d ON d.id = t.disciplina_id
                WHERE t.usuario_id = ?
            """
            parametros = [usuario_id]
            if not incluir_concluidas:
                sql += " AND t.concluida = 0"
            sql += " ORDER BY CASE WHEN t.concluida = 1 THEN 1 ELSE 0 END, " \
                   "CASE WHEN t.prazo IS NULL THEN 1 ELSE 0 END, t.prazo, " \
                   "CASE t.prioridade WHEN 'alta' THEN 0 WHEN 'media' THEN 1 ELSE 2 END, t.id DESC"
            linhas = conexao.execute(sql, parametros).fetchall()
            return [self._linha_para_objeto(linha) for linha in linhas]
        finally:
            conexao.close()

    def buscar_por_id(self, tarefa_id, usuario_id):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                """
                SELECT t.*, d.nome AS disciplina_nome
                FROM tarefas t
                LEFT JOIN disciplinas d ON d.id = t.disciplina_id
                WHERE t.id = ? AND t.usuario_id = ?
                """,
                (tarefa_id, usuario_id),
            ).fetchone()
            return self._linha_para_objeto(linha) if linha else None
        finally:
            conexao.close()

    def atualizar(self, tarefa):
        conexao = obter_conexao()
        try:
            self._validar_disciplina_do_usuario(
                conexao, tarefa.usuario_id, tarefa.disciplina_id
            )
            cursor = conexao.execute(
                """
                UPDATE tarefas
                SET disciplina_id = ?, titulo = ?, descricao = ?, prazo = ?,
                    prioridade = ?, duracao_estimada = ?, concluida = ?
                WHERE id = ? AND usuario_id = ?
                """,
                (
                    tarefa.disciplina_id,
                    tarefa.titulo,
                    tarefa.descricao,
                    tarefa.prazo,
                    tarefa.prioridade,
                    tarefa.duracao_estimada,
                    int(tarefa.concluida),
                    tarefa.id,
                    tarefa.usuario_id,
                ),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            raise ValueError(f"Não foi possível atualizar a tarefa: {erro}") from erro
        finally:
            conexao.close()

    def excluir(self, tarefa_id, usuario_id):
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
                (tarefa_id, usuario_id),
            )
            conexao.commit()
            return cursor.rowcount > 0
        finally:
            conexao.close()

    def resumo_do_usuario(self, usuario_id):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                """
                SELECT COUNT(*) AS total,
                       SUM(CASE WHEN concluida = 1 THEN 1 ELSE 0 END) AS concluidas,
                       SUM(CASE WHEN concluida = 0 THEN 1 ELSE 0 END) AS pendentes
                FROM tarefas WHERE usuario_id = ?
                """,
                (usuario_id,),
            ).fetchone()
            return {
                "total": linha["total"] or 0,
                "concluidas": linha["concluidas"] or 0,
                "pendentes": linha["pendentes"] or 0,
            }
        finally:
            conexao.close()
