---
title: Agenda de tarefas
sidebar_position: 1
description: Visualização das tarefas por prazo e identificação de atrasos.
---

# Agenda de tarefas

A rota `GET /agenda` mostra uma visão das tarefas do usuário, com base nos prazos cadastrados em `/tarefas`. Usa o template `agenda.html` e consulta `TarefaRepository.listar_do_usuario(usuario.id)`.

- Tarefas com prazo podem ser exibidas e comparadas à data atual para sinalizar **atraso**.
- Tarefas sem prazo continuam disponíveis na lista de tarefas; sua situação não é classificada como atrasada.
- Ações sobre tarefas são encaminhadas ao endpoint `POST /tarefas/<id>/acao` e retornam para a agenda quando o formulário informa `origem=agenda`.

A agenda é alimentada pelo banco SQLite do projeto: **não há integração automática com Google Calendar, Outlook ou notificações de calendário** nesta versão.

Para cadastrar ou editar um prazo, utilize [Tarefas e prioridades](./tarefas.md).
