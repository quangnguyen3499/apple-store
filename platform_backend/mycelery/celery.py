from celery import Celery

# from ..store.services.store import create_store
from celery.schedules import crontab


app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(2.0, test.s("hello"), name="add every 10")


@app.task
def test(arg):
    # create_store(name="store_test", address="address_test", province="province_test")
    print("test")
    return "completed"
