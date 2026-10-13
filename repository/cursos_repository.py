"""
repository/curso_repository.py

Classe responsável por toda a persistência (acesso ao banco SQLite) dos
objetos Curso, incluindo a lista de disciplinas de cada curso.

Observações:
    - o nome do curso é único (sem diferenciar maiúsculas de minúsculas)
    - inserir grava o curso e todas as disciplinas da lista na mesma
      transação; os ids gerados são gravados nos próprios objetos
    - atualizar sincroniza a lista: disciplinas novas são inseridas, as
      existentes são atualizadas e as que saíram da lista ficam sem curso
      (curso_id = NULL) em vez de serem apagadas
    - excluir remove só o curso; suas disciplinas e usuários ficam sem curso
    - inserir e atualizar lançam ValueError se o banco recusar os dados
"""

import sqlite3

from database.conexao import obter_conexao
from models.cursos import Curso
from repository.disciplinas_repository import DisciplinaRepository


class CursoRepository:

    # ---------------------------------------------------------
    # Auxiliares (uso interno)
    # ---------------------------------------------------------
    def _salvar_disciplina(self, conexao, disciplina, id_curso):
        # Insere a disciplina (se ainda não tem id) ou atualiza e vincula
        # ao curso (se já tem id), usando a conexão recebida.
        if disciplina.id is None:
            cursor = conexao.execute(
                'INSERT INTO disciplinas '
                '(nome, codigo, carga_horaria, concluida, curso_id) '
                'VALUES (?, ?, ?, ?, ?)',
                (disciplina.nome, disciplina.codigo, disciplina.carga_horaria,
                 int(disciplina.concluida), id_curso),
            )
            disciplina.id = cursor.lastrowid
        else:
            conexao.execute(
                'UPDATE disciplinas SET nome = ?, codigo = ?, carga_horaria = ?, '
                'concluida = ?, curso_id = ? WHERE id = ?',
                (disciplina.nome, disciplina.codigo, disciplina.carga_horaria,
                 int(disciplina.concluida), id_curso, disciplina.id),
            )

    def _linha_para_objeto(self, conexao, linha):
        # Converte uma linha do banco em um objeto Curso já com suas disciplinas.
        curso = Curso(linha['nome'], linha['nivel'], id=linha['id'])
        linhas_disciplinas = conexao.execute(
            'SELECT * FROM disciplinas WHERE curso_id = ?', (linha['id'],)
        ).fetchall()
        curso.disciplinas = [
            DisciplinaRepository.linha_para_objeto(l) for l in linhas_disciplinas
        ]
        return curso

    # ---------------------------------------------------------
    # CRUD
    # ---------------------------------------------------------
    def inserir(self, curso):
        # Parâmetro: curso (objeto Curso já validado)
        # Retorno: o id (int) gerado pelo banco para o novo curso.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'INSERT INTO cursos (nome, nivel) VALUES (?, ?)',
                (curso.nome, curso.nivel),
            )
            id_curso = cursor.lastrowid
            for disciplina in curso.disciplinas:
                self._salvar_disciplina(conexao, disciplina, id_curso)
            conexao.commit()
            curso.id = id_curso
            return id_curso
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Não foi possível salvar o curso: {erro}') from erro
        finally:
            conexao.close()

    def listar_todos(self):
        # Retorno: lista de objetos Curso (vazia se não houver registros).
        conexao = obter_conexao()
        try:
            linhas = conexao.execute('SELECT * FROM cursos').fetchall()
            return [self._linha_para_objeto(conexao, linha) for linha in linhas]
        finally:
            conexao.close()

    def buscar_por_id(self, id_curso):
        # Parâmetro: id_curso (int)
        # Retorno: objeto Curso ou None se não existir.
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                'SELECT * FROM cursos WHERE id = ?', (id_curso,)
            ).fetchone()
            return self._linha_para_objeto(conexao, linha) if linha else None
        finally:
            conexao.close()

    def buscar_por_nome(self, nome):
        # Parâmetro: nome (str)
        # Retorno: objeto Curso ou None se não existir.
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                'SELECT * FROM cursos WHERE nome = ?', (nome,)
            ).fetchone()
            return self._linha_para_objeto(conexao, linha) if linha else None
        finally:
            conexao.close()

    def atualizar(self, curso):
        # Parâmetro: curso (objeto Curso já contendo um id válido)
        # Retorno: True se o curso foi atualizado, False caso contrário.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'UPDATE cursos SET nome = ?, nivel = ? WHERE id = ?',
                (curso.nome, curso.nivel, curso.id),
            )
            if cursor.rowcount == 0:
                return False

            for disciplina in curso.disciplinas:
                self._salvar_disciplina(conexao, disciplina, curso.id)

            ids_mantidos = [d.id for d in curso.disciplinas]
            if ids_mantidos:
                marcadores = ', '.join('?' for _ in ids_mantidos)
                conexao.execute(
                    f'UPDATE disciplinas SET curso_id = NULL '
                    f'WHERE curso_id = ? AND id NOT IN ({marcadores})',
                    [curso.id] + ids_mantidos,
                )
            else:
                conexao.execute(
                    'UPDATE disciplinas SET curso_id = NULL WHERE curso_id = ?',
                    (curso.id,),
                )
            conexao.commit()
            return True
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Não foi possível salvar o curso: {erro}') from erro
        finally:
            conexao.close()

    def excluir(self, id_curso):
        # Parâmetro: id_curso (int)
        # Retorno: True se alguma linha foi excluída, False caso contrário.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute('DELETE FROM cursos WHERE id = ?', (id_curso,))
            conexao.commit()
            return cursor.rowcount > 0
        finally:
            conexao.close()