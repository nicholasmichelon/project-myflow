---
title: Glossário
sidebar_position: 1
description: Conceitos usados no projeto e nas regras de negócio.
---

# Glossário

| Conceito | Significado |
|---|---|
| Modelo | Classe Python que representa dados ou regras de negócio |
| Repositório | Classe que consulta e persiste objetos SQLite |
| Curso compartilhado | Curso associado a mais de um usuário |
| Disciplina | Item do catálogo de um curso; sem conclusão compartilhada |
| Progresso individual | Conclusão de disciplina registrada por usuário |
| Tarefa | Atividade pessoal com prazo, prioridade e duração estimada |
| Sugestor de tarefas | Ordenação determinística da próxima tarefa compatível com o tempo livre |
| Dashboard | Tela de resumo individual em `/dashboard` |
| Agenda | Apresentação de tarefas conforme prazos em `/agenda` |
| Proprietário | Conta com `is_owner=True`, autorizada a administrar usuários |
| CSRF | Ataque que tenta enviar formulário em nome de uma sessão; o app exige token nas requisições POST |
| Hash de senha | Representação protegida utilizada para verificar a senha sem salvar o texto original |
| Token de recuperação | Segredo aleatório temporário usado para redefinir senha; requer tabela ainda não criada pelo schema anexado |
| SMTP | Protocolo para envio de e-mail de recuperação |
| Schema | Estrutura SQL de tabelas, campos e restrições |
| Migração | Mudança de estrutura ou dados em uma versão anterior do banco |
| PlantUML | Formato `.puml` dos diagramas editáveis |
| Mermaid | Sintaxe dos diagramas renderizados no site Docusaurus |
