---
title: Meu perfil
sidebar_position: 1
description: Atualização de dados pessoais e credenciais.
---

# Meu perfil

Na rota `GET/POST /perfil`, usuários autenticados consultam e atualizam o perfil.

| Dado | Pode alterar? | Validação relevante |
|---|---|---|
| Nome, jornada e objetivo | Sim | Textos não vazios pelo modelo `Usuario` |
| Tempo disponível | Sim | Número inteiro positivo de minutos |
| E-mail | Sim | E-mail não duplicado; requer senha atual para mudança |
| Senha | Sim | Requer senha atual, nova senha com pelo menos 8 caracteres e confirmação |

O código calcula se houve alteração do e-mail ou pedido de troca de senha. Se houver, valida a **senha atual** usando `check_password_hash()` antes de persistir. A senha nova é transformada em hash com `generate_password_hash()`.

Ajustar `tempo_disponivel` altera quais tarefas podem ser consideradas na [recomendação](./sugestor.md) da próxima ação.

:::note Acesso
O perfil é individual. O painel administrativo não exibe senhas existentes; veja [Administração](./administracao.md).
:::
