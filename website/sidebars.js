const sidebars = {
  tutorialSidebar: [
    { type: 'doc', id: 'intro', label: 'Início' },
    {
      type: 'category', label: 'Produto', collapsible: true, collapsed: false,
      items: ['product/visao-geral'],
    },
    {
      type: 'category', label: 'Primeiros passos', collapsible: true, collapsed: false,
      items: ['getting-started/instalacao', 'getting-started/configuracao'],
    },
    {
      type: 'category', label: 'Guias de uso', collapsible: true, collapsed: false,
      items: [
        'guides/jornada-do-usuario',
        'guides/autenticacao',
        'guides/cursos-e-disciplinas',
        'guides/progresso-individual',
      ],
    },
    {
      type: 'category', label: 'Arquitetura técnica', collapsible: true, collapsed: false,
      items: [
        'architecture/arquitetura',
        'architecture/modelos',
        'architecture/repositorios',
        'architecture/banco-de-dados',
        'architecture/aplicacao-web',
      ],
    },
    {
      type: 'category', label: 'Referência', collapsible: true, collapsed: false,
      items: [
        'reference/uml',
        'reference/seguranca-e-limitacoes',
        'reference/solucao-de-problemas',
        'reference/glossario',
        'reference/manutencao',
      ],
    },
  ],
};

module.exports = sidebars;
