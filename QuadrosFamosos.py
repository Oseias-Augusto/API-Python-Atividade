import sqlite3

DB_NAME = "arte.db"

def conectar():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    return conn, cursor

def tabela_cabealho_pintores():
    print("╔════╦════════════════════╦════════════════╦════════════╦════════════╦════════════════╗")
    print("║ ID ║ Nome               ║ Criação        ║ Autor      ║ Valor      ║ Descrição      ║")
    print("╠════╬════════════════════╬════════════════╬════════════╬════════════╬════════════════╣")

def tabela_rodape_pintores():
    print("╚════╩════════════════════╩════════════════╩════════════╩════════════╩════════════════╝")


def linha():
    print("╔" + "═" * 85 + "╗")

def linha_inferior():
    print("╚" + "═" * 85 + "╝")

class Quadros:
    def __init__(self, nome,valorEstimado, descricao, anoCriacao=None, pintor_id=None, id=None):
        self.id = id
        self.nome = nome
        self.anoCriacao = anoCriacao
        self.valorEstimado = valorEstimado
        self.descricao = descricao
        self.pintor_id = pintor_id 

    # C (do CRUD)
    def salvar(self):
        """Insere o quadro no banco"""
        conn, cursor = conectar()
        cursor.execute("""
            INSERT INTO Quadros (nome, anoCriacao, valorEstimado, descricao, pintor_id)
            VALUES (?, ?, ?, ?, ?)
        """, (self.nome, self.anoCriacao, self.valorEstimado, self.descricao, self.pintor_id))
        conn.commit()
        conn.close()
        print(f"Quadro '{self.nome}' adicionado com sucesso!")

    # R (do CRUD)
    @staticmethod
    def listar():
        
        conn, cursor = conectar()
        cursor.execute("""
            SELECT 
                q.id, 
                q.nome, 
                q.anoCriacao, 
                p.nome AS 'pintor nome',
                q.valorEstimado, 
                q.descricao
            FROM Quadros q
            LEFT JOIN Pintores p ON q.pintor_id = p.id
        """)
        resultados = cursor.fetchall()
        conn.close()

        if not resultados:
            linha()
            print("║" + "Nenhum quadro registrado.".center(85) + "║")
            linha_inferior()

        else:
            tabela_cabealho_pintores()
            for row in resultados:
                print(f"║ {str(row[0]).ljust(2)} ║ "
                    f"{row[1][:18].ljust(18)} ║ "
                    f"{(row[2] or '')[:14].ljust(14)} ║ "
                    f"{(row[3] or 'Sem pintor')[:10].ljust(10)} ║ "
                    f"{(str(float(row[4])) if row[4] is not None else '')[:10].ljust(10)} ║ "
                    f"{(row[5] or '')[:14].ljust(14)} ║")
            tabela_rodape_pintores()
            
    # U (do CRUD)
    @staticmethod
    def atualizar(id_quadro, nome=None, anoCriacao=None, valorEstimado=None, descricao=None, pintor_id=None):
       
        conn, cursor = conectar()
    
        cursor.execute("SELECT id FROM Quadros WHERE id = ?", (id_quadro,))
        existe = cursor.fetchone()
        if not existe:
            conn.close()
            print(f"ERRO: Quadro ID {id_quadro} não encontrado.")
            return

        campos = {
            "nome": nome,
            "anoCriacao": anoCriacao,
            "valorEstimado": valorEstimado,
            "descricao": descricao,
            "pintor_id": pintor_id
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

        sql = f"UPDATE Quadros SET {', '.join(set_clauses)} WHERE id = ?"
        valores.append(id_quadro)

        cursor.execute(sql, tuple(valores))
        conn.commit()
        conn.close()
        print(f"Quadro ID {id_quadro} atualizado com sucesso!")

    # D (do CRUD)
    @staticmethod
    def deletar(id_quadro):
        
        conn, cursor = conectar()
        cursor.execute("DELETE FROM Quadros WHERE id=?", (id_quadro,))
        conn.commit()
        conn.close()
        print(f"Quadro ID {id_quadro} removido com sucesso!")
