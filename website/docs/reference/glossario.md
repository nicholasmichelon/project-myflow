---
title: Glossário
sidebar_position: 4
description: Termos usados na documentação do MyFlow.
---

# Glossário

| Termo | Significado no projeto |
|---|---|
| Modelo | Classe de domínio que representa usuário, curso, disciplina ou progresso |
| Repositório | Classe que realiza consultas e persistência de um modelo no SQLite |
| Curso compartilhado | Registro de curso que pode estar associado a vários usuários |
| Catálogo de disciplinas | Conjunto de disciplinas associadas a um curso, compartilhado pelos usuários desse curso |
| Progresso individual | Estado de conclusão de uma disciplina para um usuário específico |
| `senha_hash` | Representação criptográfica da senha usada para verificar autenticação sem armazenar a senha pura |
| Sessão Flask | Dados assinados que permitem reconhecer a conta autenticada entre requisições |
| Migração | Alteração controlada do schema ou transferência de dados de uma estrutura antiga para a nova |
| `ValueError` | Exceção usada pelo projeto para sinalizar valores inválidos ou alguns conflitos de persistência |
| Docusaurus | Gerador de site estático usado para publicar esta documentação |
| PlantUML (`.puml`) | Formato textual dos diagramas UML originais do repositório |
| Mermaid | Sintaxe textual para diagramas renderizados diretamente nas páginas Docusaurus |
