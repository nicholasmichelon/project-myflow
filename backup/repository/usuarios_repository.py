"""
repository/usuario_repository.py

Classe responsável por toda a persistência (acesso ao banco SQLite) dos
objetos Usuario.

Observações:
    - o e-mail do usuário é único (sem diferenciar maiúsculas de minúsculas)
    - se o usuário tem curso, o curso precisa ter sido salvo antes
      (curso.id não pode ser None), senão é lançado ValueError
    - ao ler do banco, o curso do usuário volta carregado com suas disciplinas
    - inserir também grava o id gerado no próprio objeto Usuario
    - inserir e atualizar lançam ValueError se o banco recusar os dados
"""

import sqlite3

from database.conexao import obter_conexao
from models.usuarios import Usuario
from repository.cursos_repository import CursoRepository


class UsuarioRepository:

    # ---------------------------------------------------------
    # Auxiliares (uso interno)
    # ---------------------------------------------------------
    def _id_do_curso(self, usuario):
        if usuario.curso is None:
            return None
        if usuario.curso.id is None:
            raise ValueError(
                'O curso do usuário precisa ser salvo antes (curso.id é None)'
            )
        return usuario.curso.id

    def _linha_para_objeto(self, linha):
        usuario = Usuario(
            linha['nome'], linha['email'], linha['jornada'],
            linha['objetivo'], linha['tempo_disponivel'], id=linha['id'],
            senha_hash=(linha['senha_hash'] if 'senha_hash' in linha.keys() else None),
        )
        if linha['curso_id'] is not None:
            usuario.curso = CursoRepository().buscar_por_id(linha['curso_id'])
        return usuario

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------
    def inserir(self, usuario):
        # Parâmetro: usuario (objeto Usuario já validado)
        # Retorno: o id (int) gerado pelo banco para o novo usuário.
        id_curso = self._id_do_curso(usuario)
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'INSERT INTO usuarios '
                '(nome, email, jornada, objetivo, tempo_disponivel, curso_id, senha_hash) '
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (usuario.nome, usuario.email, usuario.jornada,
                 usuario.objetivo, usuario.tempo_disponivel, id_curso,
                 usuario.senha_hash),
            )
            conexao.commit()
            usuario.id = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Não foi possível salvar o usuário: {erro}') from erro
        finally:
            conexao.close()

    def listar_todos(self):
        # Retorno: lista de objetos Usuario (vazia se não houver registros).
        conexao = obter_conexao()
        try:
            linhas = conexao.execute('SELECT * FROM usuarios').fetchall()
        finally:
            conexao.close()
        return [self._linha_para_objeto(linha) for linha in linhas]

    def buscar_por_id(self, id_usuario):
        # Parâmetro: id_usuario (int)
        # Retorno: objeto Usuario ou None se não existir.
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                'SELECT * FROM usuarios WHERE id = ?', (id_usuario,)
            ).fetchone()
        finally:
            conexao.close()
        return self._linha_para_objeto(linha) if linha else None

    def buscar_por_email(self, email):
        # Parâmetro: email (str)
        # Retorno: objeto Usuario ou None se não existir.
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                'SELECT * FROM usuarios WHERE email = ?', (email,)
            ).fetchone()
        finally:
            conexao.close()
        return self._linha_para_objeto(linha) if linha else None

    def atualizar(self, usuario):
        # Parâmetro: usuario (objeto Usuario já contendo um id válido)
        # Retorno: True se alguma linha foi atualizada, False caso contrário.
        id_curso = self._id_do_curso(usuario)
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'UPDATE usuarios SET nome = ?, email = ?, jornada = ?, '
                'objetivo = ?, tempo_disponivel = ?, curso_id = ?, '
                'senha_hash = ? WHERE id = ?',
                (usuario.nome, usuario.email, usuario.jornada,
                 usuario.objetivo, usuario.tempo_disponivel, id_curso,
                 usuario.senha_hash, usuario.id),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Não foi possível salvar o usuário: {erro}') from erro
        finally:
            conexao.close()

    def excluir(self, id_usuario):
        # Parâmetro: id_usuario (int)
        # Retorno: True se alguma linha foi excluída, False caso contrário.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'DELETE FROM usuarios WHERE id = ?', (id_usuario,)
            )
            conexao.commit()
            return cursor.rowcount > 0
        finally:
            conexao.close()