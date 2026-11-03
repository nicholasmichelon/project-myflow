PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS cursos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL COLLATE NOCASE UNIQUE,
    nivel TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id INTEGER,
    nome TEXT NOT NULL,
    codigo TEXT NOT NULL COLLATE NOCASE,
    carga_horaria INTEGER NOT NULL CHECK (carga_horaria > 0),
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE SET NULL,
    UNIQUE (curso_id, codigo)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL COLLATE NOCASE UNIQUE,
    jornada TEXT NOT NULL,
    objetivo TEXT NOT NULL,
    tempo_disponivel INTEGER NOT NULL CHECK (tempo_disponivel > 0),
    curso_id INTEGER,
    senha_hash TEXT,
    is_owner INTEGER NOT NULL DEFAULT 0 CHECK (is_owner IN (0, 1)),
    FOREIGN KEY (curso_id) REFERENCES cursos(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_disciplinas_curso_id
    ON disciplinas(curso_id);

CREATE TABLE IF NOT EXISTS progresso_disciplinas (
    usuario_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    concluida INTEGER NOT NULL DEFAULT 0 CHECK (concluida IN (0, 1)),
    atualizado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (usuario_id, disciplina_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_progresso_disciplina_id
    ON progresso_disciplinas(disciplina_id);

CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    disciplina_id INTEGER,
    titulo TEXT NOT NULL CHECK (length(trim(titulo)) > 0),
    descricao TEXT NOT NULL DEFAULT '',
    prazo TEXT,
    prioridade TEXT NOT NULL DEFAULT 'media' CHECK (prioridade IN ('alta', 'media', 'baixa')),
    duracao_estimada INTEGER NOT NULL CHECK (duracao_estimada > 0),
    concluida INTEGER NOT NULL DEFAULT 0 CHECK (concluida IN (0, 1)),
    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_tarefas_usuario_status_prazo
    ON tarefas(usuario_id, concluida, prazo);

CREATE TABLE IF NOT EXISTS schema_migrations (
    versao TEXT PRIMARY KEY,
    aplicado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
