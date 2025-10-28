import sqlite3

DB_NAME = "arte.db"

def conectar():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def tabela_cabealho_pintores():
    print("╔════╦════════════════════╦════════════════╦════════════╦════════════╦════════════════╗")
    print("║ ID ║ Nome               ║ Nacionalidade  ║ Nascimento ║ Morte      ║ Estilo         ║")
    print("╠════╬════════════════════╬════════════════╬════════════╬════════════╬════════════════╣")

def tabela_rodape_pintores():
    print("╚════╩════════════════════╩════════════════╩════════════╩════════════╩════════════════╝")

def linha():
    print("╔" + "═" * 85 + "╗")

def linha_inferior():
    print("╚" + "═" * 85 + "╝")

class Pintores:
    def __init__(self, nome, anoMorte, anoNasc, estilo, nacionalidade, id=None):
        self.id = id
        self.nome = nome
        self.anoMorte = anoMorte
        self.anoNasc = anoNasc
        self.estilo = estilo
        self.nacionalidade = nacionalidade

    # C (do CRUD)
    def salvar(self):
        
        conn, cursor = conectar()
        cursor.execute("""
            INSERT INTO Pintores (nome, nacionalidade, anoNasc, anoMort, estilo)
            VALUES (?, ?, ?, ?, ?)
        """, (self.nome, self.nacionalidade, self.anoNasc, self.anoMorte, self.estilo))
        conn.commit()
        conn.close()
        print(f"Pintor {self.nome} adicionado com sucesso!")

    # R (do CRUD)
    @staticmethod
    def listar():
        
        conn, cursor = conectar()
        cursor.execute("SELECT * FROM Pintores")
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            linha()
            print("║" + "Nenhum pintor registrado.".center(85) + "║")
            linha_inferior()
            
        else:
            tabela_cabealho_pintores()
            for row in resultados:
                print(f"║ {str(row[0]).ljust(2)} ║ "
                    f"{row[1][:18].ljust(18)} ║ "
                    f"{(row[2] or '')[:14].ljust(14)} ║ "
                    f"{(row[3] or '')[:10].ljust(10)} ║ "
                    f"{(row[4] or '')[:10].ljust(10)} ║ "
                    f"{(row[5] or '')[:14].ljust(14)} ║")
            tabela_rodape_pintores()

    # U (do CRUD)
    @staticmethod
    def atualizar(id_pintor, nome=None, nacionalidade=None, anoNasc=None, anoMort=None, estilo=None):
        conn, cursor = conectar()

        
        cursor.execute("SELECT id FROM Pintores WHERE id = ?", (id_pintor,))
        existe = cursor.fetchone()
        if not existe:
            conn.close()
            print(f"ERRO: Pintor ID {id_pintor} não encontrado.")
            return

        campos = {
            "nome": nome,
            "nacionalidade": nacionalidade,
            "anoNasc": anoNasc,
            "anoMort": anoMort,
            "estilo": estilo
        }
        set_clauses = []
        valores = []

        for coluna, valor in campos.items():
            if valor is not None:
                set_clauses.append(f"{coluna} = ?")
                valores.append(valor)

        if not set_clauses:
            conn.close()
            print("Nada para atualizar: nenhum campo foi informado.")
            return

        sql = f"UPDATE Pintores SET {', '.join(set_clauses)} WHERE id = ?"
        valores.append(id_pintor)

        cursor.execute(sql, tuple(valores))
        conn.commit()
        conn.close()
        print(f"Pintor ID {id_pintor} atualizado com sucesso!")

    
    # D (do CRUD)
    @staticmethod
    def deletar(id_pintor):
        
        conn, cursor = conectar()
        cursor.execute("DELETE FROM Pintores WHERE id=?", (id_pintor,))
        conn.commit()
        conn.close()
        print(f"Pintor ID {id_pintor} removido com sucesso!")
