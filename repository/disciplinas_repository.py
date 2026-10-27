"""
repository/disciplina_repository.py

Classe responsável por toda a persistência (acesso ao banco SQLite) dos
objetos Disciplina.

Observações:
    - o código da disciplina é único dentro de cada curso (sem diferenciar
      maiúsculas de minúsculas); por isso, buscar_por_codigo pode receber curso_id
    - inserir e atualizar lançam ValueError se o banco recusar os dados
      (por exemplo, código repetido)
    - inserir também grava o id gerado no próprio objeto Disciplina
    - o vínculo com o curso (curso_id) é gerenciado pelo CursoRepository
"""

import sqlite3

from database.conexao import obter_conexao
from models.disciplinas import Disciplina


class DisciplinaRepository:

    @staticmethod
    def linha_para_objeto(linha):
        # Converte uma linha do banco em um objeto Disciplina.
        disciplina = Disciplina(
            linha['nome'], linha['codigo'], linha['carga_horaria'], id=linha['id']
        )
        return disciplina

    def inserir(self, disciplina, curso_id=None):
        # Parâmetros: disciplina (objeto Disciplina já validado) e curso_id
        #   (opcional, id do curso ao qual a disciplina pertence).
        # Retorno: o id (int) gerado pelo banco para o novo registro.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'INSERT INTO disciplinas '
                '(nome, codigo, carga_horaria, curso_id) '
                'VALUES (?, ?, ?, ?)',
                (disciplina.nome, disciplina.codigo, disciplina.carga_horaria,
                 curso_id),
            )
            conexao.commit()
            disciplina.id = cursor.lastrowid
            return cursor.lastrowid
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Não foi possível salvar a disciplina: {erro}') from erro
        finally:
            conexao.close()

    def listar_todos(self):
        # Retorno: lista de objetos Disciplina (vazia se não houver registros).
        conexao = obter_conexao()
        try:
            linhas = conexao.execute('SELECT * FROM disciplinas').fetchall()
        finally:
            conexao.close()
        return [self.linha_para_objeto(linha) for linha in linhas]

    def listar_por_curso(self, id_curso):
        # Parâmetro: id_curso (int)
        # Retorno: lista de Disciplina do curso (vazia se não houver).
        conexao = obter_conexao()
        try:
            linhas = conexao.execute(
                'SELECT * FROM disciplinas WHERE curso_id = ?', (id_curso,)
            ).fetchall()
        finally:
            conexao.close()
        return [self.linha_para_objeto(linha) for linha in linhas]

    def buscar_por_id(self, id_disciplina):
        # Parâmetro: id_disciplina (int)
        # Retorno: objeto Disciplina ou None se não existir.
        conexao = obter_conexao()
        try:
            linha = conexao.execute(
                'SELECT * FROM disciplinas WHERE id = ?', (id_disciplina,)
            ).fetchone()
        finally:
            conexao.close()
        return self.linha_para_objeto(linha) if linha else None

    def buscar_por_codigo(self, codigo, curso_id=None):
        # O código é único por curso. Informe curso_id quando o contexto
        # do curso for conhecido; sem ele, retorna a primeira correspondência.
        conexao = obter_conexao()
        try:
            if curso_id is None:
                linha = conexao.execute(
                    'SELECT * FROM disciplinas WHERE codigo = ? ORDER BY id LIMIT 1',
                    (codigo,),
                ).fetchone()
            else:
                linha = conexao.execute(
                    'SELECT * FROM disciplinas WHERE codigo = ? AND curso_id = ?',
                    (codigo, curso_id),
                ).fetchone()
        finally:
            conexao.close()
        return self.linha_para_objeto(linha) if linha else None

    def atualizar(self, disciplina):
        # Parâmetro: disciplina (objeto Disciplina já contendo um id válido)
        # Retorno: True se alguma linha foi atualizada, False caso contrário.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'UPDATE disciplinas SET nome = ?, codigo = ?, '
                'carga_horaria = ? WHERE id = ?',
                (disciplina.nome, disciplina.codigo, disciplina.carga_horaria,
                 disciplina.id),
            )
            conexao.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError as erro:
            raise ValueError(f'Não foi possível salvar a disciplina: {erro}') from erro
        finally:
            conexao.close()

    def excluir(self, id_disciplina):
        # Parâmetro: id_disciplina (int)
        # Retorno: True se alguma linha foi excluída, False caso contrário.
        conexao = obter_conexao()
        try:
            cursor = conexao.execute(
                'DELETE FROM disciplinas WHERE id = ?', (id_disciplina,)
            )
            conexao.commit()
            return cursor.rowcount > 0
        finally:
            conexao.close()