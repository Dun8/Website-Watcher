from ..connection import get_connection


def db_health():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT version();")
    finally:
        conn.close()


def db_new_website(name, url, css_selector, check_interval_minutes):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO websites (name, url, css_selector, check_interval_minutes) VALUES (%s, %s, %s, %s) RETURNING id, name, url, css_selector, check_interval_minutes, is_active, created_at, updated_at", (name, url, css_selector, check_interval_minutes, ))
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


def db_get_last_checked(website_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT checked_at FROM website_checks WHERE website_id = %s ORDER BY checked_at DESC, id DESC LIMIT 1", (website_id, ))
        res = cursor.fetchone()

        if res is None:
            return None

        return res[0]
    finally:
        conn.close()


def db_get_check_history(website_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, website_id, checked_at, has_changed FROM website_checks WHERE website_id = %s ORDER BY checked_at DESC, id DESC", (website_id, ))
        res = cursor.fetchall()
        return res
    finally:
        conn.close()


def db_change_name(website_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE websites SET name = %s, updated_at = NOW() WHERE id = %s", (name, website_id, ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def db_change_check_interval_minutes(website_id, check_interval_minutes):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE websites SET check_interval_minutes = %s, updated_at = NOW() WHERE id = %s", (check_interval_minutes, website_id, ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def db_change_is_active(website_id, is_active):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE websites SET is_active = %s, updated_at = NOW() WHERE id = %s", (is_active, website_id, ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def db_change_css_selector(website_id, css_selector):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE websites SET css_selector = %s, updated_at = NOW() WHERE id = %s", (css_selector, website_id, ))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()