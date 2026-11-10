---
title: Rotas e interface web
sidebar_position: 1
description: Mapa atualizado de páginas, endpoints e permissões Flask.
---

# Rotas e interface web

As rotas definidas em `app.py` renderizam templates HTML/Jinja e usam sessão para identificar o usuário.

## Autenticação e conta

| Rota | Métodos | Descrição |
|---|---|---|
| `/` | GET, POST | Cadastro |
| `/login` | GET, POST | Login |
| `/sair` | POST | Encerrar sessão |
| `/perfil` | GET, POST | Alterar perfil e credenciais |
| `/esqueci-senha` | GET, POST | Solicitar link de redefinição (depende de tabela ausente) |
| `/redefinir-senha/<token>` | GET, POST | Validar token e trocar senha (depende de tabela ausente) |

## Estudo e produtividade

| Rota | Métodos | Descrição |
|---|---|---|
| `/curso` | GET, POST | Criar/reutilizar e associar curso |
| `/disciplinas` | GET, POST | Cadastrar disciplinas e alterar progresso individual |
| `/dashboard` | GET | Resumo de curso, tarefas e próxima ação |
| `/tarefas` | GET, POST | Listar e criar tarefas |
| `/tarefas/<int:tarefa_id>/editar` | GET, POST | Editar tarefa |
| `/tarefas/<int:tarefa_id>/acao` | POST | Concluir, reabrir ou excluir tarefa |
| `/agenda` | GET | Agenda baseada nos prazos |

## Administração

| Rota | Métodos | Descrição |
|---|---|---|
| `/configurar-proprietario` | GET, POST | Ativar primeiro proprietário mediante token |
| `/admin/usuarios` | GET | Listar contas (somente proprietário) |
| `/admin/usuarios/<int:id_usuario>/excluir` | POST | Excluir conta comum |
| `/admin/usuarios/<int:id_usuario>/papel` | POST | Promover/rebaixar papel |
| `/admin/usuarios/<int:id_usuario>/senha` | POST | Definir senha de conta comum |

As rotas de administração conferem o proprietário via `UsuarioRepository`, não apenas pela presença de links no menu. O app exige token CSRF em todas as requisições POST por formulário.

## Principais templates

`cadastro.html`, `login.html`, `cadastro_curso.html`, `cadastro_disciplinas.html`, `dashboard.html`, `tarefas.html`, `editar_tarefa.html`, `agenda.html`, `perfil.html`, `esqueci_senha.html`, `redefinir_senha.html`, `configurar_proprietario.html`, `admin_usuarios.html` e o parcial `_nav_conta.html`.

A folha de estilos da aplicação é `static/styles.css`; o portal Docusaurus mantém seu CSS em `website/src/css/custom.css`.
