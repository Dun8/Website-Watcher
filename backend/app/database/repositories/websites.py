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
            "css_selector, check_interval_minutes, is_active, created_at, updated_at", (name, url, css_selector, check_interval_minutes, ))
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



def db_get_old_hash(website_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT content_hash FROM website_checks WHERE website_id = %s AND content_hash IS NOT NULL ORDER BY checked_at DESC, id DESC LIMIT 1", (website_id, ))
        res = cursor.fetchone()

        if res is None:
            return None

        return res[0]

    finally:
        conn.close()

def db_get_url_and_css_selector(website_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT url, css_selector FROM websites WHERE id = %s", (website_id, ))
        res = cursor.fetchone()

        if res is None:
            return None

        return res[0], res[1]

    finally:
        conn.close()

def db_new_check(website_id, status_code, content_hash, has_changed, error_message):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO website_checks (website_id, status_code, content_hash, has_changed, error_message) VALUES (%s, %s, %s, %s, %s)", (website_id, status_code, content_hash, has_changed, error_message, ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def db_check_website(website_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT is_active FROM websites WHERE id = %s", (website_id, ))
        res = cursor.fetchone()

        if res is None:
            return None

        return res[0]

    finally:
        conn.close()