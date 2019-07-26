from datetime import datetime
import logging
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import ausencias

def listener_error(event):
    if event.exception:
        print('THE JOB CHASHED')
    else:
        print("THE JOB WORKED")

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_listener(listener_error, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler.add_job(ausencias.registrar_ausencia, 'interval', minutes=10)
    scheduler.start()
