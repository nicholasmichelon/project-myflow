---
title: Administração de contas
sidebar_position: 1
description: Ativação de proprietário e permissões de gerenciamento.
---

# Administração de contas

O MyFlow distingue contas comuns e contas com papel **proprietário**, representado pelo booleano `Usuario.is_owner`. As operações administrativas verificam o papel atual no **banco**, não apenas um valor no navegador.

## Ativação do primeiro proprietário

1. Quando ainda não existe proprietário, o servidor exibe um token no terminal (ou usa `MYFLOW_OWNER_SETUP_TOKEN`).
2. Entre com a conta que será proprietária.
3. Abra `/configurar-proprietario` e informe o código.
4. Após ativação, a rota de configuração fica indisponível a contas comuns; proprietários usam `/admin/usuarios`.

## Operações disponíveis

| Rota | Ação | Restrições |
|---|---|---|
| `GET /admin/usuarios` | Listar usuários | Exige proprietário; não mostra hash no painel |
| `POST /admin/usuarios/<id>/senha` | Definir senha de conta comum | Mínimo 8 caracteres e confirmação; não altera senha de proprietário |
| `POST /admin/usuarios/<id>/papel` | Promover/rebaixar | Não altera o próprio papel; não remove o último proprietário |
| `POST /admin/usuarios/<id>/excluir` | Excluir conta comum | Não exclui a conta ativa nem conta ainda proprietária |

## Dados compartilhados e particulares

Cursos e disciplinas podem ser compartilhados; tarefas e progresso pertencem às respectivas contas. Excluir uma conta remove seus registros relacionados conforme as relações de banco e as operações do repositório.

:::caution Uso acadêmico
O mecanismo inicial de proprietário depende de um token de configuração. Não exponha esse token em imagens, commits ou mensagens. Antes de qualquer implantação pública, realize uma revisão de autorização e infraestrutura.
:::
