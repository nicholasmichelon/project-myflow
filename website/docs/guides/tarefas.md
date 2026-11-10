---
title: Tarefas e prioridades
sidebar_position: 1
description: Criação e acompanhamento de tarefas pessoais no MyFlow.
---

# Tarefas e prioridades

A página `/tarefas` reúne tarefas **do usuário autenticado**. Cada tarefa pode estar vinculada a uma disciplina do curso, mas o vínculo é opcional.

## Campos da tarefa

| Campo | Regra |
|---|---|
| `titulo` | Texto obrigatório e não vazio |
| `descricao` | Texto opcional |
| `prazo` | Opcional, no formato `AAAA-MM-DD`, validado como data |
| `prioridade` | `alta`, `media` ou `baixa` (também aceita “média” na entrada do modelo) |
| `duracao_estimada` | Inteiro positivo em **minutos** |
| `disciplina_id` | ID opcional, restrito às disciplinas do curso do usuário |
| `concluida` | Estado booleano iniciado como `False` |

## Ações na interface

1. **Cadastrar** em `GET/POST /tarefas` preenchendo os campos.
2. **Editar** em `GET/POST /tarefas/<id>/editar`, alterando atributos e a disciplina associada.
3. **Concluir, reabrir ou excluir** via `POST /tarefas/<id>/acao` com campo `acao`.
4. **Consultar a agenda** em `/agenda` para encontrar tarefas pelos prazos.

Os métodos do `TarefaRepository` incluem `usuario_id` nos filtros de busca, alteração e exclusão; o ID da tarefa sozinho não dá acesso a tarefas de outra pessoa.

## Conclusão e prazo

Uma tarefa atrasada é uma tarefa **pendente** cujo prazo é anterior à data atual. Tarefas concluídas e tarefas sem prazo não são consideradas atrasadas. O progresso de uma disciplina é independente da conclusão de tarefas vinculadas a ela.

:::tip Próximo passo
Consulte [Como funciona o sugestor](./sugestor.md) para entender por que uma tarefa pode ser sugerida antes de outra.
:::
