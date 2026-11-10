---
title: Cadastro, login e sessão
sidebar_position: 1
description: Autenticação, CSRF e recuperação de credenciais.
---

# Cadastro, login e sessão

A autenticação usa sessão Flask em `session['usuario_id']` e senhas verificadas com funções de `werkzeug.security`.

## Cadastro (`GET/POST /`)

A pessoa informa nome, e-mail, jornada, objetivo, tempo disponível, senha e confirmação. A senha exige **oito caracteres ou mais**. O e-mail é único no banco; o modelo exige um valor não vazio contendo `@`. Após o cadastro, o sistema registra a sessão e redireciona para o curso.

## Login (`GET/POST /login`)

O fluxo consulta `UsuarioRepository.buscar_por_email()` e verifica a senha com `check_password_hash()`. Falhas comuns de autenticação apresentam mensagem genérica. Contas legadas sem senha cadastrada recebem orientação para definir uma senha inicial com um proprietário.

O redirecionamento após login depende do curso: `/curso` quando não existe vínculo e `/dashboard` quando existe.

## Proteção dos formulários

O app cria um token CSRF na sessão, disponibilizado aos templates pelo `context_processor`. O `before_request` exige correspondência desse token para **requisições POST**. Caso não corresponda, retorna HTTP 400. O mecanismo é simples e não substitui revisão completa de segurança.

## Saída

`POST /sair` limpa a sessão e retorna à tela de login.

## Recuperação e contas antigas

As rotas de recuperação existem no `app.py`, mas dependem de uma tabela ausente do schema do anexo. Veja [Recuperação de senha](./recuperacao-senha.md). Contas legadas podem receber senha temporária na [administração](./administracao.md) ou pelo script local `scripts/definir_senha_usuario.py`.
