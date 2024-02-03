import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, format='<green>[{elapsed}]</green> <level>[{file}: {line}] ></level> {message}')
logger.add('logs/app.log', mode='w', format='[{elapsed}] [{name}: {line}] > {message}')