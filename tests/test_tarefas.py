"""Testes isolados dos modelos e repositórios de tarefas usando SQLite temporário."""

import tempfile
import unittest
from pathlib import Path

import database.conexao as conexao_db
from models.cursos import Curso
from models.disciplinas import Disciplina
from models.sugestor_de_tarefas import SugestorDeTarefas
from models.tarefa import Tarefa
from models.usuarios import Usuario
from repository.cursos_repository import CursoRepository
from repository.tarefas_repository import TarefaRepository
from repository.usuarios_repository import UsuarioRepository


class TestTarefas(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.caminho_original = conexao_db.CAMINHO_BANCO
        conexao_db.CAMINHO_BANCO = Path(self.temp.name) / "teste.db"
        conexao_db.inicializar_banco()

        self.curso_repo = CursoRepository()
        curso = Curso("Negócios Digitais", "Graduação")
        curso.adicionar_disciplina(Disciplina("POO", "POO-01", 60))
        self.curso_repo.inserir(curso)
        self.curso = self.curso_repo.buscar_por_id(curso.id)

        self.usuario_repo = UsuarioRepository()
        self.usuario = Usuario(
            "Ana", "ana@example.com", "Graduação", "Aprender POO", 45,
            senha_hash="hash-de-teste",
        )
        self.usuario.definir_curso(self.curso)
        self.usuario_repo.inserir(self.usuario)

        self.outro_usuario = Usuario(
            "Bruno", "bruno@example.com", "Graduação", "Aprender POO", 25,
            senha_hash="hash-de-teste",
        )
        self.outro_usuario.definir_curso(self.curso)
        self.usuario_repo.inserir(self.outro_usuario)
        self.repo = TarefaRepository()

    def tearDown(self):
        conexao_db.CAMINHO_BANCO = self.caminho_original
        self.temp.cleanup()

    def test_tarefa_e_isolamento_por_usuario(self):
        tarefa = Tarefa(
            usuario_id=self.usuario.id,
            disciplina_id=self.curso.disciplinas[0].id,
            titulo="Revisar POO",
            prazo="2026-10-28",
            prioridade="alta",
            duracao_estimada=30,
        )
        self.repo.criar(tarefa)
        self.assertEqual(len(self.repo.listar_do_usuario(self.usuario.id)), 1)
        self.assertEqual(len(self.repo.listar_do_usuario(self.outro_usuario.id)), 0)
        self.assertIsNone(self.repo.buscar_por_id(tarefa.id, self.outro_usuario.id))

    def test_sugestor_respeita_tempo_disponivel(self):
        curta = Tarefa(
            usuario_id=self.usuario.id, titulo="Revisão rápida",
            prioridade="media", duracao_estimada=20,
        )
        longa = Tarefa(
            usuario_id=self.usuario.id, titulo="Leitura longa",
            prioridade="alta", duracao_estimada=60,
        )
        sugestao = SugestorDeTarefas(30).sugerir_proxima_acao([curta, longa])
        self.assertEqual(sugestao.titulo, "Revisão rápida")

    def test_conclusao_resumo_e_exclusao(self):
        tarefa = Tarefa(
            usuario_id=self.usuario.id, titulo="Entrega de atividade",
            duracao_estimada=40,
        )
        self.repo.criar(tarefa)
        tarefa.titulo = "Entrega revisada"
        self.assertTrue(self.repo.atualizar(tarefa))
        tarefa = self.repo.buscar_por_id(tarefa.id, self.usuario.id)
        self.assertEqual(tarefa.titulo, "Entrega revisada")
        tarefa.concluir()
        self.assertTrue(self.repo.atualizar(tarefa))
        self.assertEqual(
            self.repo.resumo_do_usuario(self.usuario.id),
            {"total": 1, "concluidas": 1, "pendentes": 0},
        )
        self.assertTrue(self.repo.excluir(tarefa.id, self.usuario.id))
        self.assertEqual(self.repo.resumo_do_usuario(self.usuario.id)["total"], 0)

    def test_validacao_de_prazo_e_duracao(self):
        with self.assertRaises(ValueError):
            Tarefa(usuario_id=self.usuario.id, titulo="Prazo inválido", prazo="ontem")
        with self.assertRaises(ValueError):
            Tarefa(usuario_id=self.usuario.id, titulo="Duração inválida", duracao_estimada=0)


if __name__ == "__main__":
    unittest.main()
