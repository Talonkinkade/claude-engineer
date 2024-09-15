import logging
from fastapi import HTTPException

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AppException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        logger.error(f"AppException: {status_code} - {detail}")

def log_info(message: str):
    logger.info(message)

def log_error(message: str):
    logger.error(message)