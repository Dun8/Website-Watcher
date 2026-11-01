import httpx
from bs4 import BeautifulSoup
import hashlib
from ..database.repositories.websites import db_new_check, db_get_url_and_css_selector, db_get_old_hash

def fetch_page(url):
    response = httpx.get(url, timeout=10, follow_redirects=True)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "").lower()

    if "text/html" not in content_type and "application/xhtml+xml" not in content_type:
        raise ValueError("Сайт вернул не HTML")

    return response

def extract_text(html, css_selector=None):
    soup = BeautifulSoup(html.text, 'html.parser')

    if css_selector:
        css = soup.select_one(css_selector)
        if not css:
            raise ValueError("Выбранный CSS-селектор не найден на сайте")
        return css.get_text(" ", strip=True)

    return soup.get_text(" ", strip=True)

def normalize_text(text):
    cleaned_text = " ".join(text.split())
    return cleaned_text

def get_website_content(url, css_selector=None):
    response = fetch_page(url)
    text = extract_text(response, css_selector)
    text = normalize_text(text)

    return {"status_code": response.status_code, "content": text}

def check_hash(website_id):
    try:
        website = db_get_url_and_css_selector(website_id)

        if website is None:
            raise ValueError("Сайт не найден")

        url, css_selector = website

        page = get_website_content(url, css_selector)
        status_code = page["status_code"]
        content = page["content"]
        new_hash = hashlib.sha256(content.encode()).hexdigest()
        old_hash = db_get_old_hash(website_id)

        if old_hash is None:
            db_new_check(website_id, status_code, new_hash, None, None)
            return {"website_id": website_id, "status_code": status_code, "has_changed": None, "error_message": None}
        elif new_hash != old_hash:
            db_new_check(website_id, status_code, new_hash, True, None)
            return {"website_id": website_id, "status_code": status_code, "has_changed": True, "error_message": None}
        else:
            db_new_check(website_id, status_code, new_hash, False, None)
            return {"website_id": website_id, "status_code": status_code, "has_changed": False, "error_message": None}
    except Exception:
        raise




