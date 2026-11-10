---
title: Segurança e limitações
sidebar_position: 1
description: Proteções existentes, problemas observados e condições para publicação.
---

# Segurança e limitações conhecidas

O MyFlow é um **protótipo acadêmico local**. As medidas do código não são equivalentes a uma auditoria de segurança.

## Proteções presentes

- Hash de senha com `werkzeug.security` (`generate_password_hash` / `check_password_hash`).
- Validação de token CSRF em todas as requisições `POST` no `before_request`.
- Consultas SQL parametrizadas nos repositórios.
- Sessão baseada em `usuario_id`, conferindo o papel administrativo no banco.
- Isolamento das tarefas por `usuario_id`; progresso por usuário e disciplina.
- Token aleatório para ativação inicial de proprietário quando não há contas proprietárias.
- Fluxo de redefinição **programado** para armazenar hash do token, expirar após 30 minutos e limitar solicitações em memória.

## Pendências confirmadas no código enviado

| Prioridade | Questão | Consequência e medida |
|---|---|---|
| Alta | `tokens_recuperacao_senha` não é criada pelo schema | Recuperação de senha falha em banco novo; atualizar schema e migração |
| Alta | `app.run(debug=True, use_reloader=False)` | Debug fica ativo quando executado com `python app.py`; desativar antes de exposição externa |
| Alta | Não há limitação geral de tentativas de login | Avaliar bloqueio progressivo, rate limiting e monitoramento |
| Alta | Ausência de infraestrutura HTTPS e gestão de segredos para produção | Não publicar diretamente o servidor de desenvolvimento |
| Média | Limite de solicitações de recuperação mantido em dicionário em memória | Reinício do processo zera o limite; inadequado para múltiplas instâncias |
| Média | `.env.example` citado no guia, mas ausente do pacote | Criar configuração local manualmente, sem divulgar credenciais |
| Média | Cobertura automática limitada a `tests/test_tarefas.py` | Testar formulário, autorização, administração e recuperação separadamente |

A variável `MYFLOW_DEBUG` **não é utilizada** pelo `app.py` atual. O fallback de `MYFLOW_SECRET_KEY` gera uma chave aleatória por inicialização, encerrando as sessões anteriores após reinício.

:::danger Não implantar diretamente na internet
Antes de qualquer publicação: desative debug, complete a migração do banco, configure HTTPS e segredos, valide autorização, estabeleça limites de tentativas e teste o fluxo de recuperação. O site Docusaurus é estático; essas recomendações referem-se ao servidor Flask.
:::

## Privacidade

Não distribua `database/banco.db`, arquivos `.env`, backups, senhas, tokens ou capturas contendo e-mails de usuários. Os pacotes desta atualização omitem o banco do projeto recebido.
