from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import procesoHoras

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(procesoHoras.proceso_de_horas, 'interval', minutes=1)
    scheduler.start()