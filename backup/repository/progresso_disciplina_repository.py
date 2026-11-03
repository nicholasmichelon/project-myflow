"""Repositório para armazenar progresso individual por usuário e disciplina."""

import sqlite3

from database.conexao import obter_conexao
from models.progresso_disciplina import ProgressoDisciplina


class ProgressoDisciplinaRepository:
    def buscar(self, usuario_id, disciplina_id):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                "SELECT usuario_id, disciplina_id, concluida "
                "FROM progresso_disciplinas "
                "WHERE usuario_id = ? AND disciplina_id = ?",
                (usuario_id, disciplina_id),
            ).fetchone()
            if linha is None:
                return None

            return ProgressoDisciplina(
                usuario_id=linha["usuario_id"],
                disciplina_id=linha["disciplina_id"],
                concluida=bool(linha["concluida"]),
            )
        finally:
            conexao.close()

    def listar_status_do_curso(self, usuario_id, curso_id):
        """Retorna {disciplina_id: bool}; disciplinas sem registro começam pendentes."""
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                """
                SELECT d.id AS disciplina_id,
                       COALESCE(p.concluida, 0) AS concluida
                FROM disciplinas d
                JOIN usuarios u
                  ON u.curso_id = d.curso_id
                 AND u.id = ?
                LEFT JOIN progresso_disciplinas p
                  ON p.disciplina_id = d.id
                 AND p.usuario_id = u.id
                WHERE d.curso_id = ?
                ORDER BY d.id
                """,
                (usuario_id, curso_id),
            ).fetchall()
            return {
                linha["disciplina_id"]: bool(linha["concluida"])
                for linha in linhas
            }
        finally:
            conexao.close()

    def salvar(self, progresso):
        """Cria ou atualiza o status somente se a disciplina pertencer ao curso do usuário."""
        conexao = obter_conexao()
        try:
            permitido = conexao.execute(
                """
                SELECT 1
                FROM usuarios u
                JOIN disciplinas d ON d.curso_id = u.curso_id
                WHERE u.id = ? AND d.id = ?
                """,
                (progresso.usuario_id, progresso.disciplina_id),
            ).fetchone()

            if permitido is None:
                raise ValueError(
                    "A disciplina não pertence ao curso associado a este usuário."
                )

            conexao.execute(
                """
                INSERT INTO progresso_disciplinas
                    (usuario_id, disciplina_id, concluida)
                VALUES (?, ?, ?)
                ON CONFLICT(usuario_id, disciplina_id)
                DO UPDATE SET
                    concluida = excluded.concluida,
                    atualizado_em = CURRENT_TIMESTAMP
                """,
                (
                    progresso.usuario_id,
                    progresso.disciplina_id,
                    int(progresso.concluida),
                ),
            )
            conexao.commit()
            return True
        except sqlite3.IntegrityError as erro:
            raise ValueError(f"Não foi possível salvar o progresso: {erro}") from erro
        finally:
            conexao.close()

    def calcular_progresso(self, usuario_id, curso_id):
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                """
                SELECT
                    COUNT(d.id) AS total,
                    SUM(
                        CASE WHEN COALESCE(p.concluida, 0) = 1
                             THEN 1 ELSE 0 END
                    ) AS concluidas
                FROM disciplinas d
                JOIN usuarios u
                  ON u.curso_id = d.curso_id
                 AND u.id = ?
                LEFT JOIN progresso_disciplinas p
                  ON p.disciplina_id = d.id
                 AND p.usuario_id = u.id
                WHERE d.curso_id = ?
                """,
                (usuario_id, curso_id),
            ).fetchone()

            total = linha["total"] or 0
            concluidas = linha["concluidas"] or 0

            if total == 0:
                return 0.0

            return concluidas / total * 100
        finally:
            conexao.close()
