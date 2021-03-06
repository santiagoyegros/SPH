from datetime import datetime
import logging
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import ausencias,alertas,procesoCupos,temporal

def listener_error(event):
    if event.exception:
        print('THE JOB CRASHED')
    else:
        print("THE JOB WORKED")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_listener(listener_error, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(ausencias.registrar_ausencia, 'interval', minutes=0.017)
    scheduler.add_job(alertas.registrar_alerta, 'interval', minutes=15)
    scheduler.add_job(temporal.borrar_temporales, 'cron',hour=2,minute=0)
    scheduler.add_job(procesoCupos.generarCantidadCupos, 'cron',hour=23,minute=55)
    scheduler.start()
