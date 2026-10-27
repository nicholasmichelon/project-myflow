"""Conexão SQLite e migrações incrementais do MyFlow."""

import sqlite3
from pathlib import Path


PASTA_DATABASE = Path(__file__).resolve().parent
CAMINHO_BANCO = PASTA_DATABASE / "banco.db"
CAMINHO_SCHEMA = PASTA_DATABASE / "schema.sql"


def obter_conexao():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def inicializar_banco():
    """Cria tabelas novas e migra bancos antigos sem apagar dados."""
    conexao = obter_conexao()

    try:
        with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as arquivo:
            script = arquivo.read()

        conexao.executescript(script)

        # Acrescenta senha_hash às contas criadas antes do login.
        colunas_usuarios = {
            linha["name"]
            for linha in conexao.execute("PRAGMA table_info(usuarios)").fetchall()
        }
        if "senha_hash" not in colunas_usuarios:
            conexao.execute("ALTER TABLE usuarios ADD COLUMN senha_hash TEXT")

        # Migração única do status antigo que ficava na própria Disciplina.
        # Preserva a conclusão antiga para os usuários já vinculados ao curso.
        versao = "progresso_individual_v1"
        migracao = conexao.execute(
            "SELECT 1 FROM schema_migrations WHERE versao = ?",
            (versao,),
        ).fetchone()

        if migracao is None:
            colunas_disciplinas = {
                linha["name"]
                for linha in conexao.execute(
                    "PRAGMA table_info(disciplinas)"
                ).fetchall()
            }

            if "concluida" in colunas_disciplinas:
                conexao.execute(
                    """
                    INSERT OR IGNORE INTO progresso_disciplinas
                        (usuario_id, disciplina_id, concluida)
                    SELECT u.id, d.id, COALESCE(d.concluida, 0)
                    FROM usuarios u
                    JOIN disciplinas d ON d.curso_id = u.curso_id
                    """
                )

            conexao.execute(
                "INSERT INTO schema_migrations (versao) VALUES (?)",
                (versao,),
            )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


if __name__ == "__main__":
    inicializar_banco()
    print("Banco de dados inicializado com sucesso!")
