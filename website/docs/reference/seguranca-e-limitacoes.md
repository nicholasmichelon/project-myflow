---
title: Segurança e limitações conhecidas
sidebar_position: 2
description: Medidas existentes e lacunas relevantes antes de qualquer publicação pública.
---

# Segurança e limitações conhecidas

O MyFlow é um protótipo acadêmico local. O código contém algumas medidas positivas, mas não implementa todos os controles esperados de uma aplicação publicada na internet.

## Medidas existentes

- As senhas são armazenadas como hash por `werkzeug.security`.
- O login retorna mensagem genérica para e-mail inexistente ou senha incorreta.
- A sessão é limpa antes de iniciar sessão após cadastro ou login.
- O modo de depuração fica desativado por padrão.
- A chave secreta pode ser fornecida pela variável `MYFLOW_SECRET_KEY`.
- Os comandos SQL dos repositórios usam parâmetros para os valores recebidos.
- O SQLite ativa chaves estrangeiras em cada conexão.

## Lacunas que precisam ser tratadas antes de publicar

- **Chave secreta padrão:** o código possui um valor de fallback para desenvolvimento local. Uma publicação precisa definir uma chave própria e protegida por variável de ambiente.
- **CSRF:** os formulários não têm proteção CSRF implementada.
- **Tentativas de login:** não há limitação de tentativas ou mecanismo de bloqueio.
- **Recuperação de senha:** não há fluxo de recuperação por e-mail.
- **HTTPS e hospedagem:** este pacote não configura domínio, TLS, proxy reverso ou ambiente de produção.
- **Migração e backup:** a manutenção do arquivo SQLite requer cópias de segurança antes de migrações ou substituição de arquivos.

:::danger Não publicar como está
Não exponha este protótipo à internet sem tratar as lacunas listadas, configurar a chave secreta, adotar HTTPS e revisar o ambiente de execução. A documentação não representa uma certificação de segurança.
:::

## Dados e privacidade

Evite colocar e-mails, hashes de senha ou outros dados reais em exemplos, capturas de tela e arquivos de distribuição. O banco de dados local deve permanecer fora do ZIP de entrega e do controle de versão.
