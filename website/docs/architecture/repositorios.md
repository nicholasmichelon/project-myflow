---
title: Repositórios
sidebar_position: 1
description: Persistência SQLite e operações CRUD por entidade.
---

# Repositórios

O diretório `repository/` organiza a persistência em cinco classes. As operações de leitura devolvem objetos de domínio e as alterações executam SQL parametrizado.

## `UsuarioRepository`

`inserir`, `listar_todos`, `buscar_por_id`, `buscar_por_email`, `atualizar`, `excluir`, `contar_proprietarios`, `definir_proprietario` e `listar_para_administracao`. Gerencia o vínculo `curso_id`, os hashes de senha e o papel `is_owner`.

## `CursoRepository`

`inserir`, `listar_todos`, `buscar_por_id`, `buscar_por_nome`, `atualizar`, `excluir`. Salva cursos e sincroniza as disciplinas vinculadas, usando transações nas operações compostas.

## `DisciplinaRepository`

`inserir`, `listar_todos`, `listar_por_curso`, `buscar_por_id`, `buscar_por_codigo`, `atualizar` e `excluir`. Respeita o código da disciplina dentro do curso.

## `ProgressoDisciplinaRepository`

`buscar`, `listar_status_do_curso`, `salvar`, `calcular_progresso`. Persiste a conclusão pelo par `(usuario_id, disciplina_id)`.

## `TarefaRepository`

| Método | Responsabilidade |
|---|---|
| `criar(tarefa)` | Insere tarefa pessoal com validação opcional da disciplina |
| `listar_do_usuario(usuario_id, incluir_concluidas=True)` | Devolve tarefas do usuário, ordenadas para exibição |
| `buscar_por_id(tarefa_id, usuario_id)` | Consulta uma tarefa do próprio usuário |
| `atualizar(tarefa)` | Altera campos usando ID e proprietário |
| `excluir(tarefa_id, usuario_id)` | Remove tarefa do proprietário |
| `resumo_do_usuario(usuario_id)` | Retorna contagem total, concluídas e pendentes |

:::info Diferença importante
`TarefaRepository.listar_do_usuario()` define a **ordem de exibição**, enquanto `SugestorDeTarefas` define a **ordem de recomendação**; são lógicas distintas. A sugestão é feita sobre objetos `Tarefa` depois da consulta.
:::

### Isolamento de dados

A alteração e a exclusão de tarefas dependem de `usuario_id`; a associação a uma disciplina só é aceita quando ela pertence ao curso do titular. O catálogo de cursos e disciplinas continua compartilhado.
