---
title: Manutenção e contribuição
sidebar_position: 1
description: Como atualizar a aplicação, testes e documentação.
---

# Manutenção e contribuição

## Ao alterar o código

1. Identifique a classe, rota, repositório e tabela envolvidos.
2. Faça backup do banco local antes de migração ou exclusão de dados.
3. Atualize os testes correspondentes. A suíte atual contém `tests/test_tarefas.py`.
4. Execute a suíte sem tocar no banco local:

```powershell
python -m unittest discover -s tests -v
```

5. Teste manualmente os formulários Flask, especialmente login, CSRF, permissão de proprietário, tarefas de usuários distintos e recuperação de senha.
6. Atualize diagramas PlantUML e as páginas deste portal quando o comportamento mudar.

## Ao alterar a documentação

```powershell
cd website
npm ci
npm run build
```

Use `npm run start` para pré-visualizar. Mantenha a navegação em `website/sidebars.js` e evite IDs repetidos (por exemplo, `intro.md` + `intro.mdx`). Não adicione `editUrl: null` ou a opção obsoleta `onBrokenMarkdownLinks` no nível raiz.

## Checklist de revisão

- [ ] Cadastro, login e páginas protegidas funcionam.
- [ ] Cursos e disciplinas não alteram o progresso de outros usuários.
- [ ] Tarefas de uma conta não podem ser consultadas/editadas por outra.
- [ ] Sugestão respeita tempo, atraso, prioridade, prazo e duração.
- [ ] Administração exige usuário proprietário.
- [ ] Recuperação de senha possui tabela de tokens e fluxo testado.
- [ ] `debug` desativado para ambientes não locais.
- [ ] `npm run build` concluído sem erros.
- [ ] ZIP livre de banco local, backups, `.env`, `node_modules` e credenciais.
