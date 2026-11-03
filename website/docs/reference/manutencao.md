---
title: Manutenção e contribuição
sidebar_position: 5
description: Procedimentos para evoluir o código e manter a documentação consistente.
---

# Manutenção e contribuição

Esta página descreve um procedimento enxuto para alterações acadêmicas no MyFlow. O repositório não inclui uma suíte automatizada de testes como diretório ou comando dedicado; por isso, mudanças devem ser verificadas localmente antes de serem consideradas concluídas.

## Antes de modificar

1. Confira a regra de negócio nos modelos e no schema.
2. Identifique os repositórios e rotas que usam o atributo ou método afetado.
3. Faça backup do banco local se a mudança envolver estrutura ou dados.
4. Evite alterar nomes públicos de métodos sem atualizar os locais de chamada, os diagramas UML e a documentação.

## Depois de modificar a aplicação

- Inicie `python app.py` e percorra o fluxo relacionado à alteração.
- Teste entradas válidas e inválidas.
- Confirme que os dados permanecem corretos após sair e entrar novamente.
- Quando houver relações entre usuário, curso e disciplina, teste dois usuários que compartilham o mesmo curso para garantir que o progresso continua independente.
- Se alterar schema, documente a migração e como preservar dados existentes.

## Depois de modificar a documentação

```powershell
cd website
npm run build
```

O build valida a configuração e os links internos. Para pré-visualizar durante a escrita, use `npm run start`.

## Padrões recomendados

- Escreva em português claro e mantenha os nomes do código em `snake_case`/CamelCase exatamente como estão implementados.
- Diferencie comportamento existente de proposta futura.
- Prefira exemplos pequenos e sem dados pessoais.
- Atualize o diagrama de classes quando mudar atributos, métodos ou relacionamentos.
- Atualize um diagrama de sequência quando mudar a ordem das interações entre interface, modelo, repositório e banco.
- Não inclua `database/banco.db`, `.env`, `.venv/`, `node_modules/`, `__pycache__/` ou arquivos de senha no pacote distribuído.

## Checklist de entrega

- [ ] Aplicação Flask inicia sem erros.
- [ ] Cadastro e login foram testados.
- [ ] Curso e disciplinas foram salvos e carregados novamente.
- [ ] Progresso foi verificado com mais de um usuário do mesmo curso.
- [ ] Diagrama UML correspondente foi atualizado.
- [ ] `npm run build` finaliza sem erros.
- [ ] Nenhum banco local ou segredo foi incluído no pacote.
