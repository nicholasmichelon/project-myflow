---
title: Dashboard
sidebar_position: 1
description: Resumo de estudos, indicadores e sugestão no painel principal.
---

# Dashboard

A rota `GET /dashboard` exige sessão válida e curso associado. Ela consulta o curso, tarefas pessoais e progresso das disciplinas antes de renderizar `templates/dashboard.html`.

## Indicadores exibidos

| Informação | Origem |
|---|---|
| Progresso do curso | `ProgressoDisciplinaRepository.calcular_progresso(usuario.id, curso.id)` |
| Totais de tarefas | `TarefaRepository.resumo_do_usuario()` |
| Pendentes e concluídas | Filtro de `TarefaRepository.listar_do_usuario()` |
| Atrasadas | `Tarefa.esta_atrasada(hoje)` aplicado às pendentes |
| Próximas tarefas | Tarefas pendentes com prazo a partir de hoje, limitadas a cinco no código |
| Próxima ação | `SugestorDeTarefas.sugerir_proxima_acao()` com tempo diário do perfil |

A **conclusão de tarefas** e o **progresso do curso** são métricas distintas: a primeira depende do estado das tarefas; a segunda considera as disciplinas concluídas individualmente.

## Quando não aparece uma sugestão?

Quando nenhuma tarefa pendente tem duração estimada menor ou igual ao tempo disponível, o método retorna `None`. Atualize seu tempo em [Meu perfil](./perfil.md) ou ajuste uma tarefa em [Gerenciar tarefas](./tarefas.md).
