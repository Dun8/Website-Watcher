from ..database.connection import get_connection
import uvicorn
from fastapi import FastAPI, HTTPException, status
from ..schemas import websites



app = FastAPI()

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT version();")

    except:
        raise HTTPException(status_code=500, detail="Ошибка при запросе")
    finally:
        conn.close()

@app.post("/api/websites", status_code=status.HTTP_201_CREATED)
def new_website(data : websites.WebsiteCreate):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO websites (name, url, css_selector, check_interval_minutes) VALUES (%s, %s, %s, %s) RETURNING *", (data.name, str(data.url), data.css_selector, data.check_interval_minutes))
        res = cursor.fetchone()
        conn.commit()
        return {"id": res[0], "name": res[1], "url": res[2], "css_selector": res[3], "check_interval_minutes": res[4],
                "is_active": res[5], "created_at": res[6], "updated_at": res[7]}
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при запросе")
    finally:
        conn.close()

@app.get("/api/websites", status_code=status.HTTP_200_OK)
def get_all_websites():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, name, url, check_interval_minutes, is_active, created_at FROM websites ORDER BY id DESC")
        res = []
        for website in cursor.fetchall():
            res.append({"id": website[0], "name": website[1], "url": website[2], "check_interval_minutes": website[3],
                        "is_active": website[4], "created_at": website[5]})
        return res
    except Exception:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при запросе")
    finally:
        conn.close()













if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)