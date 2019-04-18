from datetime import datetime


def define_event_status(event):
    if datetime.now() < event.time_start:
        event.status = 'Starting_soon'
    elif datetime.now() > event.time_end:
        event.status = 'Finished'
    else:
        event.status = 'Opening_now'