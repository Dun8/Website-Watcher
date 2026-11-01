from ..database.repositories.websites import (db_health, db_new_website, db_get_all_websites, db_change_css_selector, db_change_name,
                                              db_change_is_active, db_change_check_interval_minutes, db_check_website)
import uvicorn
from fastapi import FastAPI, HTTPException, status
from ..schemas import websites

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    try:
        db_health()
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")


@app.post("/api/websites", status_code=status.HTTP_201_CREATED)
def new_website(data: websites.WebsiteCreate):
    try:
        res = db_new_website(data.name, str(data.url), data.css_selector, data.check_interval_minutes)
        return {"id": res[0], "name": res[1], "url": res[2], "css_selector": res[3], "check_interval_minutes": res[4],
                "is_active": res[5], "created_at": res[6], "updated_at": res[7]}
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")


@app.get("/api/websites", status_code=status.HTTP_200_OK)
def get_all_websites():
    try:
        fetch = db_get_all_websites()
        res = []

        for website in fetch:
            res.append({"id": website[0], "name": website[1], "url": website[2], "check_interval_minutes": website[3],
                        "is_active": website[4], "created_at": website[5]})

        return res
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")


@app.patch("/api/websites/{website_id}", status_code=status.HTTP_200_OK)
def update_website(website_id: int, data: websites.WebsiteUpdate):
    try:
        check = db_check_website(website_id)

        if check is None:
            raise HTTPException(status_code=404, detail="Сайт не найден")

        if data.name is not None:
            db_change_name(website_id, data.name)

        if data.css_selector is not None or "css_selector" in data.model_fields_set:
            db_change_css_selector(website_id, data.css_selector)

        if data.check_interval_minutes is not None:
            db_change_check_interval_minutes(website_id, data.check_interval_minutes)

        if data.is_active is not None:
            db_change_is_active(website_id, data.is_active)

        return {"detail": "Сайт успешно обновлён"}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")


from .check import check_website, check_website_history


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)