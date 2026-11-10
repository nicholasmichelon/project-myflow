const sidebars = {
  docsSidebar: [
    {type: 'doc', id: 'intro', label: 'Visão inicial'},
    {type: 'category', label: 'Produto', collapsed: false, items: [
      'product/visao-geral',
    ]},
    {type: 'category', label: 'Começar', collapsed: false, items: [
      'getting-started/instalacao', 'getting-started/configuracao',
    ]},
    {type: 'category', label: 'Guias de uso', collapsed: false, items: [
      'guides/jornada-do-usuario', 'guides/dashboard', 'guides/tarefas',
      'guides/sugestor', 'guides/agenda', 'guides/cursos-e-disciplinas',
      'guides/progresso-individual', 'guides/perfil',
      'guides/autenticacao', 'guides/recuperacao-senha', 'guides/administracao',
    ]},
    {type: 'category', label: 'Arquitetura', collapsed: false, items: [
      'architecture/arquitetura', 'architecture/modelos', 'architecture/repositorios',
      'architecture/banco-de-dados', 'architecture/aplicacao-web',
    ]},
    {type: 'category', label: 'Referência', collapsed: false, items: [
      'reference/uml', 'reference/seguranca-e-limitacoes',
      'reference/solucao-de-problemas', 'reference/glossario', 'reference/manutencao',
    ]},
  ],
};
module.exports = sidebars;
