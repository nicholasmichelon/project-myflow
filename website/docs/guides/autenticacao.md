---
title: Cadastro, login e sessão
sidebar_position: 2
description: Regras atuais de autenticação, hash de senha e encerramento de sessão.
---

# Cadastro, login e sessão

A autenticação é implementada nas rotas `/` (cadastro), `/login` e `/sair`. O estado de autenticação é mantido por uma sessão Flask, identificada pela chave `usuario_id`.

## Cadastro

- O campo de senha deve ter pelo menos oito caracteres.
- A confirmação precisa coincidir com a senha.
- O e-mail é obrigatório e precisa conter `@` segundo a validação da classe `Usuario`; o banco também impõe unicidade sem diferenciar maiúsculas/minúsculas.
- A senha é transformada com `generate_password_hash()` antes de persistir. O texto puro não é armazenado.
- Após sucesso, a sessão é limpa e recriada para o novo usuário.

## Login

A aplicação localiza a conta pelo e-mail e verifica a senha com `check_password_hash()`. Usuário inexistente e senha incorreta recebem a mensagem genérica “E-mail ou senha inválidos”. Contas antigas sem `senha_hash` recebem instruções para definir uma senha localmente.

## Contas antigas sem senha

Execute pela raiz do projeto:

```powershell
python scripts\definir_senha_usuario.py
```

O script solicita o e-mail da conta existente e a nova senha. Use esse procedimento apenas no ambiente local e nunca compartilhe a senha em mensagens ou arquivos.

## Sair da conta

A rota `/sair` aceita `POST`, limpa os dados da sessão e redireciona para `/login`.

:::warning Limitações atuais
O projeto não implementa recuperação de senha por e-mail, proteção CSRF para formulários nem limite de tentativas de login. Isso é importante considerar antes de disponibilizar a aplicação fora de um ambiente acadêmico local. Consulte [Segurança e limitações](../reference/seguranca-e-limitacoes.md).
:::
