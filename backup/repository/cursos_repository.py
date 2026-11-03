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
        # ao curso. Retorna o id sem alterar o objeto antes do commit.
        if disciplina.id is None:
            cursor = conexao.execute(
                'INSERT INTO disciplinas '
                '(nome, codigo, carga_horaria, curso_id) '
                'VALUES (?, ?, ?, ?)',
                (disciplina.nome, disciplina.codigo, disciplina.carga_horaria,
                 id_curso),
            )
            return cursor.lastrowid

        registro = conexao.execute(
            'SELECT curso_id FROM disciplinas WHERE id = ?',
            (disciplina.id,),
        ).fetchone()

        if registro is None:
            raise ValueError(
                f'A disciplina com id {disciplina.id} não existe no banco.'
            )

        if registro['curso_id'] not in (None, id_curso):
            raise ValueError(
                'A disciplina já está vinculada a outro curso.'
            )

        cursor = conexao.execute(
            'UPDATE disciplinas SET nome = ?, codigo = ?, carga_horaria = ?, '
            'curso_id = ? WHERE id = ?',
            (disciplina.nome, disciplina.codigo, disciplina.carga_horaria,
             id_curso, disciplina.id),
        )

        if cursor.rowcount == 0:
            raise ValueError(
                f'Não foi possível atualizar a disciplina {disciplina.id}.'
            )

        return disciplina.id

    def _linha_para_objeto(self, conexao, linha):
        # Converte uma linha do banco em um objeto Curso já com suas disciplinas.
        curso = Curso(linha['nome'], linha['nivel'], id=linha['id'])
        linhas_disciplinas = conexao.execute(
            'SELECT * FROM disciplinas WHERE curso_id = ? ORDER BY id',
            (linha['id'],),
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
        existente = self.buscar_por_nome(curso.nome)
        if existente is not None:
            raise ValueError('Já existe um curso com esse nome.')

        conexao = obter_conexao()
        disciplinas_pendentes = []
        try:
            cursor = conexao.execute(
                'INSERT INTO cursos (nome, nivel) VALUES (?, ?)',
                (curso.nome, curso.nivel),
            )
            id_curso = cursor.lastrowid

            for disciplina in curso.disciplinas:
                id_original = disciplina.id
                id_disciplina = self._salvar_disciplina(
                    conexao, disciplina, id_curso
                )
                if id_original is None:
                    disciplinas_pendentes.append((disciplina, id_disciplina))

            conexao.commit()

            # Só atribui os IDs aos objetos depois que a transação foi salva.
            curso.id = id_curso
            for disciplina, id_disciplina in disciplinas_pendentes:
                disciplina.id = id_disciplina

            return id_curso
        except sqlite3.IntegrityError as erro:
            conexao.rollback()
            raise ValueError(f'Não foi possível salvar o curso: {erro}') from erro
        except Exception:
            conexao.rollback()
            raise
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
        # A comparação é feita com casefold() do Python para reconhecer
        # letras acentuadas em diferentes capitalizações (SQLite NOCASE
        # trata apenas caracteres ASCII por padrão).
        if not isinstance(nome, str):
            return None

        nome_normalizado = nome.strip().casefold()
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                'SELECT * FROM cursos ORDER BY id'
            ).fetchall()

            for linha in linhas:
                if linha['nome'].casefold() == nome_normalizado:
                    return self._linha_para_objeto(conexao, linha)

            return None
        finally:
            conexao.close()

    def atualizar(self, curso):
        # Parâmetro: curso (objeto Curso já contendo um id válido)
        # Retorno: True se o curso foi atualizado, False caso contrário.
        existente = self.buscar_por_nome(curso.nome)
        if existente is not None and existente.id != curso.id:
            raise ValueError('Já existe outro curso com esse nome.')

        conexao = obter_conexao()
        disciplinas = curso.disciplinas
        disciplinas_pendentes = []
        try:
            cursor = conexao.execute(
                'UPDATE cursos SET nome = ?, nivel = ? WHERE id = ?',
                (curso.nome, curso.nivel, curso.id),
            )
            if cursor.rowcount == 0:
                return False

            ids_mantidos = []
            for disciplina in disciplinas:
                id_original = disciplina.id
                id_disciplina = self._salvar_disciplina(
                    conexao, disciplina, curso.id
                )
                ids_mantidos.append(id_disciplina)
                if id_original is None:
                    disciplinas_pendentes.append((disciplina, id_disciplina))

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

            # Evita deixar IDs na memória caso a transação falhe.
            for disciplina, id_disciplina in disciplinas_pendentes:
                disciplina.id = id_disciplina

            return True
        except sqlite3.IntegrityError as erro:
            conexao.rollback()
            raise ValueError(f'Não foi possível salvar o curso: {erro}') from erro
        except Exception:
            conexao.rollback()
            raise
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