import sys
from datetime import datetime
import time
import logging
logging.basicConfig(filename=f'output_{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}.log', level=logging.DEBUG)
logger=logging.getLogger(__name__)

try:
    arg1 = sys.argv[1]
    logger.info(arg1)
    print(arg1) 
    time.sleep(10)

except Exception as e: 
    logger.error(e)

  