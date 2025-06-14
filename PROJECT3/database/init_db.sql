-- Инициализация базы данных
CREATE TABLE IF NOT EXISTS professions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    skills TEXT,
    salary TEXT,
    education TEXT,
    subjects TEXT
);