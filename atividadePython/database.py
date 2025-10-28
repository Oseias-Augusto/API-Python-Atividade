import sqlite3

DB_NAME = "arte.db"

def conectar():
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    
    conn, cursor = conectar()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pintores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nacionalidade TEXT,
        anoNasc TEXT,
        anoMort TEXT,
        estilo TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Quadros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        anoCriacao TEXT,
        autor TEXT,
        valorEstimado REAL,
        descricao TEXT,
        pintor_id INTEGER,
        FOREIGN KEY (pintor_id) REFERENCES Pintores(id)
    )
    """)

    conn.commit()
    conn.close()
