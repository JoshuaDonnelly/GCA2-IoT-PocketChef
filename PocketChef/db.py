from mysql.connector import pooling, Error
import os
import logging

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
    global POOL
    if POOL is None:
        init_db_pool()
    return POOL.get_connection()

def save_cooking_session(session):
    sql = """
        INSERT INTO cooking_sessions
            (user_email, device_id, meat_type, image_url, target_temp, actual_temp,
             start_time, end_time, notes,
             weight, is_metric, desired_temp, timer_seconds)
        VALUES (%s, %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s)
    """
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, (
            session.get("user_email"),
            session.get("device_id"),
            session.get("meat_type"),
            session.get("image_url"),
            session.get("target_temp"),
            session.get("actual_temp"),
            session.get("start_time"),
            session.get("end_time"),
            session.get("notes"),
            session.get("weight"),
            1 if session.get("is_metric", True) else 0,
            session.get("desired_temp"),
            session.get("timer_seconds"),
        ))
        conn.commit()
        inserted_id = cur.lastrowid
        cur.close()
        return inserted_id
    except Error:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def list_sessions(user_email=None, limit=100, offset=0):
    sql = """
    SELECT id, user_email, device_id, meat_type, image_url, target_temp, actual_temp,
           start_time, end_time, notes,
           weight, is_metric, desired_temp, timer_seconds
    FROM cooking_sessions
    """
    params = []
    if user_email:
        sql += " WHERE user_email = %s"
        params.append(user_email)

    sql += " ORDER BY start_time DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    conn = get_conn()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, tuple(params))
        rows = cursor.fetchall()
        cursor.close()
        return rows
    finally:
        conn.close()


def get_session(session_id, user_email=None):
    sql = """
    SELECT id, user_email, device_id, meat_type, image_url, target_temp, actual_temp,
           start_time, end_time, notes,
           weight, is_metric, desired_temp, timer_seconds
    FROM cooking_sessions
    WHERE id = %s
    """
    params = [session_id]
    if user_email:
        sql += " AND user_email = %s"
        params.append(user_email)

    conn = get_conn()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, tuple(params))
        row = cursor.fetchone()
        cursor.close()
        return row
    finally:
        conn.close()
def add_favorite(user_email, meal_id):
    sql = "INSERT IGNORE INTO favorite_recipes (user_email, meal_id) VALUES (%s, %s)"
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, (user_email, meal_id))
        conn.commit()
        cur.close()
    finally:
        conn.close()

def remove_favorite(user_email, meal_id):
    sql = "DELETE FROM favorite_recipes WHERE user_email = %s AND meal_id = %s"
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, (user_email, meal_id))
        conn.commit()
        cur.close()
    finally:
        conn.close()

def list_favorites(user_email):
    sql = "SELECT meal_id FROM favorite_recipes WHERE user_email = %s"
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, (user_email,))
        rows = cur.fetchall()
        cur.close()
        return rows
    finally:
        conn.close()