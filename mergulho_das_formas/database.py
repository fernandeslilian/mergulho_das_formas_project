import sqlite3
import os

DB_FILE = "ranking.db"

def init_db():
    """
    cria a tabela do banco de dados se ela não existir.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE COLLATE NOCASE,  
            tempo_segundos REAL NOT NULL
        )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        if conn:
            conn.close()

def check_name_exists(nome):
    """
    Verifica se um nome já existe no banco de dados.
    Retorna True se o nome existir, False caso contrário.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM ranking WHERE nome = ? COLLATE NOCASE", (nome,))
        result = cursor.fetchone()
        
        # se fetchone() encontrar algo, result não é None, então o nome existe
        return result is not None 
        
    except sqlite3.Error as e:
        print(f"Erro ao checar nome: {e}")
        return False # assume que não existe se der erro
    finally:
        if conn:
            conn.close()


def add_score(nome, tempo_segundos):
    """
    Adiciona ou atualiza uma pontuação no banco de dados.
    Se o nome já existe, só atualiza se o novo tempo for menor.
    (Agora ignora maiúsculas/minúsculas)
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # verifica se o nome já existe (ignorando maiúsculas/minúsculas)
        cursor.execute("SELECT tempo_segundos FROM ranking WHERE nome = ? COLLATE NOCASE", (nome,))
        result = cursor.fetchone()

        if result is None:
            # se nome não existe, insere novo recorde
            # o nome será salvo com as maiúsculas/minúsculas da primeira vez.
            cursor.execute("INSERT INTO ranking (nome, tempo_segundos) VALUES (?, ?)", (nome, tempo_segundos))
            print(f"Novo jogador '{nome}' adicionado com tempo {tempo_segundos:.2f}s.")
        else:
            # se nome existe, compara os tempos
            old_time = result[0]
            if tempo_segundos < old_time:
                # se novo tempo é melhor (menor), atualiza
                cursor.execute("UPDATE ranking SET tempo_segundos = ? WHERE nome = ? COLLATE NOCASE", (tempo_segundos, nome)) # <-- MUDANÇA AQUI
                print(f"Recorde de '{nome}' atualizado para {tempo_segundos:.2f}s (era {old_time:.2f}s).")
            else:
                # se novo tempo não é melhor, não faz nada
                print(f"Tempo de '{nome}' ({tempo_segundos:.2f}s) não bateu o recorde ({old_time:.2f}s).")

        conn.commit()

    except sqlite3.Error as e:
        print(f"Erro ao adicionar/atualizar pontuação: {e}")
    finally:
        if conn:
            conn.close()


def get_ranking():
    """
    retorna uma lista com o Top 5 (nome, tempo) do ranking
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, tempo_segundos FROM ranking ORDER BY tempo_segundos ASC LIMIT 5")
        ranking = cursor.fetchall()
        return ranking
    except sqlite3.Error as e:
        print(f"Erro ao buscar ranking: {e}")
        return []
    finally:
        if conn:
            conn.close()