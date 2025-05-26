import os
import time
from celery import Celery


if not os.path.exists('reports'):
    os.makedirs('reports')


celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery.task
def make_report(data):

    time.sleep(10)

    filename = f'report_{int(time.time())}.txt'
    filepath = os.path.join('reports', filename)

    with open(filepath, 'w') as f:
        f.write(f"Отчет сгенерирован на основе данных: '{data}'\n")
        f.write(f"Время создания: {time.ctime()}")

    return {'status': 'Отчет готов!', 'filename': filename}