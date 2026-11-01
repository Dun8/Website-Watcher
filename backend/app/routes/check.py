from fastapi import HTTPException, status
from .websites import app
from ..database.repositories.websites import db_check_website, db_get_check_history
from ..services.website_checker import check_hash


@app.post("/api/websites/{website_id}/check")
def check_website(website_id: int):
    try:
        check = db_check_website(website_id)

        if check is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сайт не найден")

        elif check is False:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Мониторинг сайта отключен")

        return check_hash(website_id)

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")


@app.get("/api/websites/{website_id}/check")
def check_website_history(website_id: int):
    try:
        check = db_check_website(website_id)

        if check is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Сайт не найден")

        history = db_get_check_history(website_id)

        res = []

        for check in history:
            res.append({"id": check[0], "website_id": check[1], "checked_at": check[2], "has_changed": check[3]})

        return res

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")