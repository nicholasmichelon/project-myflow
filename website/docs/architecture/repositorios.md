---
title: Repositórios
sidebar_position: 3
description: Operações de persistência e retorno das classes em repository/.
---

# Repositórios

Os repositórios encapsulam o acesso ao SQLite. Eles transformam linhas do banco em objetos, executam consultas e controlam `commit`, `rollback` e fechamento de conexão.

## `UsuarioRepository`

Arquivo: `repository/usuarios_repository.py`.

| Método | Resultado / uso |
|---|---|
| `inserir(usuario)` | Insere usuário e devolve o ID; o objeto recebe o ID gerado |
| `listar_todos()` | Lista objetos `Usuario` |
| `buscar_por_id(id_usuario)` | Retorna `Usuario` ou `None` |
| `buscar_por_email(email)` | Retorna `Usuario` ou `None` |
| `atualizar(usuario)` | Retorna `True` se uma linha foi atualizada; `False` caso contrário |
| `excluir(id_usuario)` | Retorna `True` quando exclui uma linha |

O repositório resolve o ID do curso associado e carrega os dados do curso quando reconstrói um usuário. Erros de integridade são convertidos em `ValueError` nas operações de escrita.

## `CursoRepository`

Arquivo: `repository/cursos_repository.py`.

| Método | Resultado / uso |
|---|---|
| `inserir(curso)` | Salva o curso e disciplinas presentes na mesma transação; retorna o ID do curso |
| `listar_todos()` | Lista cursos com suas disciplinas carregadas |
| `buscar_por_id(id_curso)` | Retorna `Curso` ou `None` |
| `buscar_por_nome(nome)` | Busca nome sem diferenciar capitalização, inclusive com suporte a letras acentuadas pela comparação em Python |
| `atualizar(curso)` | Atualiza o curso e sincroniza sua lista de disciplinas; retorna booleano |
| `excluir(id_curso)` | Exclui o curso e retorna booleano |

Ao atualizar a lista de disciplinas, as disciplinas removidas da lista do objeto ficam sem vínculo com o curso (`curso_id = NULL`), em vez de serem apagadas. As operações compostas usam transação. Os IDs de novas disciplinas são atribuídos aos objetos depois do `commit`.

## `DisciplinaRepository`

Arquivo: `repository/disciplinas_repository.py`.

| Método | Resultado / uso |
|---|---|
| `inserir(disciplina, curso_id=None)` | Insere disciplina e devolve seu ID |
| `listar_todos()` | Lista todas as disciplinas |
| `listar_por_curso(id_curso)` | Lista disciplinas de um curso |
| `buscar_por_id(id_disciplina)` | Retorna `Disciplina` ou `None` |
| `buscar_por_codigo(codigo, curso_id=None)` | Busca pelo código, opcionalmente dentro de um curso |
| `atualizar(disciplina)` | Atualiza dados da disciplina e retorna booleano |
| `excluir(id_disciplina)` | Exclui e retorna booleano |

O vínculo de uma disciplina ao curso é gerenciado principalmente por `CursoRepository`. O código da disciplina é único dentro do curso conforme a restrição composta do banco.

## `ProgressoDisciplinaRepository`

Arquivo: `repository/progresso_disciplina_repository.py`.

| Método | Resultado / uso |
|---|---|
| `buscar(usuario_id, disciplina_id)` | Retorna o progresso ou `None` |
| `listar_status_do_curso(usuario_id, curso_id)` | Retorna um dicionário `{disciplina_id: bool}`; ausências são tratadas como pendentes |
| `salvar(progresso)` | Valida o vínculo usuário-curso-disciplina e insere/atualiza o estado |
| `calcular_progresso(usuario_id, curso_id)` | Retorna percentual de conclusão (`float`) |

## Convenções importantes

- Os valores de usuário entram nas consultas SQL por parâmetros, não por concatenação da string SQL.
- Os métodos de consulta fecham conexões mesmo em caso de erro (`finally`).
- O modelo cuida da validação do objeto; o repositório cuida do armazenamento e de regras que dependem do banco.
- `ValueError` comunica dados rejeitados ou conflitos de integridade em operações de escrita.
