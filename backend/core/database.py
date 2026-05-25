import sqlite3
import os
from datetime import datetime
from backend.core.config import settings

# Caminho do banco de dados (na pasta data/)
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "operational.db")

def get_connection():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabela de Métricas (Contadores agregados)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT UNIQUE NOT NULL,
            metric_value INTEGER DEFAULT 0
        )
    """)

    # Tabela de Feedbacks
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message_id TEXT,
            evaluation TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de Histórico de Conversas (Memória)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Iniciar métricas básicas se não existirem
    default_metrics = ['total_interactions', 'total_fallbacks', 'total_handoffs']
    for m in default_metrics:
        cursor.execute("INSERT OR IGNORE INTO metrics (metric_name, metric_value) VALUES (?, 0)", (m,))

    conn.commit()
    conn.close()

def increment_metric(metric_name: str, increment: int = 1):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE metrics SET metric_value = metric_value + ? WHERE metric_name = ?", (increment, metric_name))
        conn.commit()
    except Exception as e:
        print(f"Erro ao incrementar métrica {metric_name}: {e}")
    finally:
        conn.close()

def get_all_metrics() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT metric_name, metric_value FROM metrics")
    rows = cursor.fetchall()
    conn.close()
    return {row["metric_name"]: row["metric_value"] for row in rows}

def save_feedback(user_id: str, evaluation: str, message_id: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (user_id, message_id, evaluation) VALUES (?, ?, ?)",
        (user_id, message_id, evaluation)
    )
    conn.commit()
    conn.close()

def get_feedback_stats() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT evaluation, COUNT(*) as count FROM feedback GROUP BY evaluation")
    rows = cursor.fetchall()
    conn.close()
    return {row["evaluation"]: row["count"] for row in rows}

def save_message(user_id: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (user_id, role, content) VALUES (?, ?, ?)",
        (user_id, role, content)
    )
    conn.commit()
    conn.close()

def get_history(user_id: str, limit: int = 5) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    # Pega as ultimas 'limit' mensagens, ordenadas cronologicamente
    cursor.execute(
        "SELECT role, content FROM conversations WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    conn.close()
    
    # Inverte para ficar em ordem cronológica correta
    history = [{"role": row["role"], "content": row["content"]} for row in reversed(rows)]
    return history
