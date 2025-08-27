import sqlite3
from datetime import datetime, timedelta
import os

# --- LÓGICA DE CAMINHO ATUALIZADA ---
# Encontra o caminho absoluto para a pasta raiz do projeto subindo dois níveis
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Aponta para a pasta onde o banco de dados está (usando a recomendação)
DB_DIR = os.path.join(PROJECT_ROOT, "database_files")
DB_PATH = os.path.join(DB_DIR, "gestao_rh.db")

os.makedirs(DB_DIR, exist_ok=True)

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS funcionarios
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nome
                       TEXT
                       NOT
                       NULL,
                       cpf
                       TEXT
                       UNIQUE,
                       rg
                       TEXT,
                       matricula
                       TEXT
                       NOT
                       NULL,
                       cargo
                       TEXT,
                       departamento
                       TEXT,
                       data_admissao
                       DATE,
                       empresa
                       TEXT,
                       cnpj
                       TEXT, -- Nova coluna para o CNPJ
                       UNIQUE
                   (
                       matricula,
                       empresa
                   )
                       );
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS exames
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       funcionario_id
                       INTEGER,
                       tipo_exame
                       TEXT
                       NOT
                       NULL,
                       data_realizacao
                       DATE
                       NOT
                       NULL,
                       data_vencimento
                       DATE,
                       status
                       TEXT,
                       observacoes
                       TEXT,
                       FOREIGN
                       KEY
                   (
                       funcionario_id
                   ) REFERENCES funcionarios
                   (
                       id
                   )
                       );
                   ''')

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS funcoes
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nome_funcao
                       TEXT
                       UNIQUE
                       NOT
                       NULL
                   );
                   ''')

    # Tabela de associação funcao
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS funcao_exames
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       funcao_id
                       INTEGER,
                       nome_exame
                       TEXT
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       funcao_id
                   ) REFERENCES funcoes
                   (
                       id
                   )
                       );
                   ''')

    conn.commit()
    conn.close()


def add_funcionario(nome, cpf, rg, matricula, cargo, departamento, data_admissao, empresa, cnpj):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
                       INSERT INTO funcionarios (nome, cpf, rg, matricula, cargo, departamento, data_admissao, empresa, cnpj)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (nome, cpf, rg, matricula, cargo, departamento, data_admissao, empresa, cnpj))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_funcionarios():
    conn = create_connection()
    cursor = conn.cursor()
    # Adicionamos a coluna 'cnpj' ao final da consulta
    cursor.execute("SELECT id, nome, matricula, cargo, empresa, cpf, cnpj FROM funcionarios ORDER BY nome")
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios


def get_all_funcionarios_detalhes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT nome,
                          cpf,
                          rg,
                          matricula,
                          cargo,
                          departamento,
                          strftime('%d-%m-%Y', data_admissao),
                          empresa
                   FROM funcionarios
                   ORDER BY nome
                   """)
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios

def add_exame(funcionario_id, tipo_exame, data_realizacao, data_vencimento, status, observacoes):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO exames (funcionario_id, tipo_exame, data_realizacao, data_vencimento, status, observacoes)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''', (funcionario_id, tipo_exame, data_realizacao, data_vencimento, status, observacoes))
    conn.commit()
    conn.close()


def get_exames_vencendo(dias=30):
    conn = create_connection()
    hoje = datetime.now().date()
    data_limite = hoje + timedelta(days=dias)

    # Consulta o EXAME MAIS RECENTE de cada funcionário
    query = f"""
        SELECT f.nome, f.matricula, e.tipo_exame, strftime('%d-%m-%Y', e.data_vencimento)
        FROM exames e
        JOIN funcionarios f ON e.funcionario_id = f.id
        -- Esta subconsulta garante que estamos pegando apenas o exame mais recente de cada funcionário
        INNER JOIN (
            SELECT funcionario_id, MAX(data_realizacao) AS max_data
            FROM exames
            GROUP BY funcionario_id
        ) AS ultimos_exames ON e.funcionario_id = ultimos_exames.funcionario_id AND e.data_realizacao = ultimos_exames.max_data

        WHERE e.data_vencimento BETWEEN '{hoje}' AND '{data_limite}'
        ORDER BY e.data_vencimento;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    exames = cursor.fetchall()
    conn.close()
    return exames


def get_exames_vencidos():
    conn = create_connection()
    hoje = datetime.now().date()
    query = f"""SELECT f.nome, f.matricula, e.tipo_exame, strftime('%d-%m-%Y', e.data_vencimento) FROM exames e JOIN funcionarios f ON e.funcionario_id = f.id WHERE e.data_vencimento < '{hoje}' ORDER BY e.data_vencimento;"""
    cursor = conn.cursor()
    cursor.execute(query)
    exames = cursor.fetchall()
    conn.close()
    return exames

def add_funcao(nome_funcao):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO funcoes (nome_funcao) VALUES (?)", (nome_funcao,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_all_funcoes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_funcao FROM funcoes ORDER BY nome_funcao")
    funcoes = cursor.fetchall()
    conn.close()
    return funcoes


def add_exame_para_funcao(funcao_id, nome_exame):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO funcao_exames (funcao_id, nome_exame) VALUES (?, ?)", (funcao_id, nome_exame))
    conn.commit()
    conn.close()


def get_exames_por_funcao(funcao_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nome_exame FROM funcao_exames WHERE funcao_id = ?",
                   (funcao_id,))
    exames = cursor.fetchall()
    conn.close()
    return [exame[0] for exame in exames]


def get_exames_por_nome_funcao(nome_funcao):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT fe.nome_exame FROM funcao_exames fe JOIN funcoes f ON fe.funcao_id = f.id WHERE f.nome_funcao = ?""",
                   (nome_funcao,))
    exames = cursor.fetchall()
    conn.close()
    return [exame[0] for exame in exames]


def update_funcionario_funcao(funcionario_id, nova_funcao):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE funcionarios SET cargo = ? WHERE id = ?", (nova_funcao, funcionario_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar função: {e}")
        return False
    finally:
        conn.close()

def get_all_funcionarios_for_editing():
    """
    Busca todos os funcionários retornando todas as colunas, incluindo o ID,
    essencial para a edição.
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf, rg, matricula, cargo, departamento, data_admissao, empresa, cnpj FROM funcionarios ORDER BY nome")
    funcionarios = cursor.fetchall()
    conn.close()
    return funcionarios


def update_funcionario_detalhes(func_id, nome, cpf, rg, matricula, cargo, departamento, data_admissao, empresa, cnpj):
    """
    Atualiza todas as informações de um funcionário específico usando seu ID.
    """
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
                       UPDATE funcionarios
                       SET nome = ?, cpf = ?, rg = ?, matricula = ?, cargo = ?,
                           departamento = ?, data_admissao = ?, empresa = ?, cnpj = ?
                       WHERE id = ?
                       """, (nome, cpf, rg, matricula, cargo, departamento, data_admissao, empresa, cnpj, func_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar funcionário: {e}")
        return False
    finally:
        conn.close()


# Inicializa o banco de dados
create_tables()
