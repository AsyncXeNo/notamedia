import sys
from datetime import datetime

from loguru import logger

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

logger.remove()
logger.add(sys.stderr, format='<level>> {message}</level>')
logger.add(f'logs/{formatted_datetime}.log', mode='w', format='[{time:DD-MM-YYYY}][{time:HH:mm:ss}][{time:zz}] > {message}')