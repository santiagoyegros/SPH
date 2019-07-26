from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import procesoCupos

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(procesoCupos.generarCantidadCupos, 'interval', seconds=5)
    scheduler.start()