"""Migra usuarios.curso_id para permitir que vários usuários compartilhem cursos.

Preserva os IDs, os dados dos usuários e senha_hash, se já existir.
Execute apenas se o banco ainda tiver UNIQUE isolado em usuarios.curso_id.
"""

import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path(__file__).resolve().parent / "banco.db"


def coluna_curso_tem_unique(conexao):
    for indice in conexao.execute("PRAGMA index_list('usuarios')").fetchall():
        nome_indice = indice[1]
        unico = bool(indice[2])
        if not unico:
            continue

        colunas = conexao.execute(
            f'PRAGMA index_info("{nome_indice.replace(chr(34), chr(34) * 2)}")'
        ).fetchall()

        if [coluna[2] for coluna in colunas] == ["curso_id"]:
            return True

    return False


def migrar():
    if not CAMINHO_BANCO.exists():
        raise FileNotFoundError(
            f"Banco não encontrado: {CAMINHO_BANCO}. Inicialize-o antes."
        )

    conexao = sqlite3.connect(CAMINHO_BANCO)

    try:
        tabelas = {
            linha[0]
            for linha in conexao.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

        if "usuarios" not in tabelas or "cursos" not in tabelas:
            raise RuntimeError(
                "O banco não possui as tabelas usuarios e cursos. "
                "Confira database/schema.sql."
            )

        if not coluna_curso_tem_unique(conexao):
            print(
                "Banco já permite compartilhar cursos; nenhuma alteração necessária."
            )
            return

        colunas_atuais = {
            linha[1] for linha in conexao.execute("PRAGMA table_info(usuarios)")
        }
        expressao_senha = "senha_hash" if "senha_hash" in colunas_atuais else "NULL"

        conexao.execute("PRAGMA foreign_keys = OFF")
        conexao.execute("BEGIN")

        conexao.execute("""
            CREATE TABLE usuarios_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                jornada TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                tempo_disponivel INTEGER NOT NULL
                    CHECK (tempo_disponivel > 0),
                curso_id INTEGER,
                senha_hash TEXT,
                FOREIGN KEY (curso_id)
                    REFERENCES cursos(id)
                    ON DELETE SET NULL
            )
        """)

        conexao.execute(f"""
            INSERT INTO usuarios_nova (
                id, nome, email, jornada, objetivo,
                tempo_disponivel, curso_id, senha_hash
            )
            SELECT
                id, nome, email, jornada, objetivo,
                tempo_disponivel, curso_id, {expressao_senha}
            FROM usuarios
        """)

        conexao.execute("DROP TABLE usuarios")
        conexao.execute(
            "ALTER TABLE usuarios_nova RENAME TO usuarios"
        )

        problemas = conexao.execute("PRAGMA foreign_key_check").fetchall()
        if problemas:
            raise sqlite3.IntegrityError(
                f"Falha na verificação de chaves estrangeiras: {problemas}"
            )

        conexao.commit()
        print("Migração concluída. Vários usuários podem compartilhar um curso.")

    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.execute("PRAGMA foreign_keys = ON")
        conexao.close()


if __name__ == "__main__":
    migrar()
