from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import procesoCupos

def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(procesoCupos.generarCantidadCupos, 'interval',seconds=10)
    scheduler.add_job(procesoCupos.generarCantidadCupos, 'cron',hour=23,minute=55)
    scheduler.start()