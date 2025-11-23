from mysql.connector import pooling, Error
import os

POOL = None

def init_db_pool():
    global POOL
    if POOL:
        return POOL
    POOL = pooling.MySQLConnectionPool(
        pool_name="pocketchef_pool",
        pool_size=int(os.getenv("DB_POOL_MAX", 5)),
        pool_reset_session=True,
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        charset="utf8mb4"
    )
    return POOL

def get_conn():
    """Return a connection from the pool."""
    global POOL
    if POOL is None:
        init_db_pool()
    return POOL.get_connection()

def save_cooking_session(session):
    """
    session: dict with keys:
      device_id (str), meat_type (str), target_temp (float), actual_temp (float),
      start_time (str/datetime), end_time (str/datetime), notes (str)
    Returns inserted id.
    """
    sql = """
    INSERT INTO cooking_sessions
      (device_id, meat_type, target_temp, actual_temp, start_time, end_time, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    conn = None
    try:
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (
            session.get("device_id"),
            session.get("meat_type"),
            session.get("target_temp"),
            session.get("actual_temp"),
            session.get("start_time"),
            session.get("end_time"),
            session.get("notes")
        ))
        conn.commit()
        inserted_id = cursor.lastrowid
        cursor.close()
        return inserted_id
    except Error as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def list_sessions(limit=100, offset=0):
    sql = """
    SELECT id, device_id, meat_type, target_temp, actual_temp, start_time, end_time, notes, created_at
    FROM cooking_sessions
    ORDER BY created_at DESC
    LIMIT %s OFFSET %s
    """
    conn = get_conn()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, (limit, offset))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()
