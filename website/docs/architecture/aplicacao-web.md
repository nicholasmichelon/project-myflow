---
title: Rotas e interface web
sidebar_position: 5
description: Endpoints Flask, métodos HTTP e páginas de template.
---

# Rotas e interface web

As rotas são declaradas em `app.py`; a interface é renderizada com Jinja a partir de `templates/`.

## Mapa de rotas

| Rota | Métodos | Template / comportamento |
|---|---|---|
| `/` | `GET`, `POST` | `cadastro.html`; exibe e processa cadastro de conta |
| `/login` | `GET`, `POST` | `login.html`; valida e-mail e senha |
| `/sair` | `POST` | Limpa sessão e redireciona para login |
| `/curso` | `GET`, `POST` | `cadastro_curso.html`; apresenta/associa curso ao usuário autenticado |
| `/disciplinas` | `GET`, `POST` | `cadastro_disciplinas.html`; lista, cadastra, conclui ou reabre disciplinas |

## Proteção de páginas

As rotas de curso e disciplinas verificam `session['usuario_id']`. Se não houver sessão, redirecionam para `/login`. Se o ID não corresponder a um usuário, a sessão é limpa. A rota de disciplinas também exige que o usuário tenha um curso associado.

## Formulários de disciplinas

O `POST /disciplinas` distingue a ação pelo campo `acao`:

- `concluir`: marca o progresso individual como concluído;
- `reabrir`: devolve a disciplina ao estado pendente;
- sem essas ações, tenta cadastrar uma nova disciplina com `nome`, `codigo` e `carga_horaria`.

Quando a pessoa conclui ou reabre uma disciplina, o app verifica se ela pertence ao curso atual antes de salvar o progresso.

## Mensagens e redirecionamentos

Mensagens de sucesso são armazenadas temporariamente na sessão (`mensagem_disciplinas`) para serem exibidas após redirecionamento. Erros de validação retornam o formulário com mensagem e código HTTP adequado; solicitações inválidas de progresso são redirecionadas à lista.

## Templates e estilos

- `templates/cadastro.html` — criação de conta.
- `templates/login.html` — autenticação.
- `templates/cadastro_curso.html` — associação/criação de curso.
- `templates/cadastro_disciplinas.html` — cadastro e acompanhamento individual.
- `static/styles.css` — estilos compartilhados da aplicação Flask.

O portal de documentação (`website/`) possui CSS e componentes próprios; seus estilos não alteram as páginas Flask.
