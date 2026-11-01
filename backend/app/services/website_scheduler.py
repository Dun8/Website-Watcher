import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from ..database.repositories.websites import db_get_all_websites, db_get_last_checked, db_new_check
from .website_checker import check_hash


scheduler = BackgroundScheduler()


def check_due_websites():
    websites = db_get_all_websites()

    for inf in websites:
        if not inf[4]:
            continue

        last_checked = db_get_last_checked(inf[0])

        if last_checked is None or datetime.datetime.now(datetime.timezone.utc) - last_checked >= datetime.timedelta(minutes=inf[3]):
            try:
                check_hash(inf[0])
            except Exception as error:
                db_new_check(inf[0], None, None, None, str(error))
                print(f"Ошибка проверки сайта {inf[0]}: {error}")


scheduler.add_job(check_due_websites, "interval", seconds=30, max_instances=1)