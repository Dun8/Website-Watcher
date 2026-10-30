from ..connection import get_connection



def db_health():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT version();")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_new_website(name, url, css_selector, check_interval_minutes):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO websites (name, url, css_selector, check_interval_minutes) VALUES (%s, %s, %s, %s) RETURNING id, name, url, "
            "css_selector, check_interval_minutes, is_active, created_at, updated_at", (name, url, css_selector, check_interval_minutes))
        res = cursor.fetchone()
        conn.commit()
        return res
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_get_all_websites():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name, url, check_interval_minutes, is_active, created_at FROM websites ORDER BY id DESC")
        return cursor.fetchall()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_new_check(website_id, status_code, content_hash, has_changed):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO website_checks (website_id, status_code, content_hash, has_changed) VALUES (%s, %s, %s, %s)",
                       (website_id, status_code, content_hash, has_changed))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_get_old_hash(url):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT content_hash WHERE website_id = (SELECT id FROM websites WHERE url = %s)", (url))
        return cursor.fetchone()[0]
    except Exception:
        raise
    finally:
        conn.close()