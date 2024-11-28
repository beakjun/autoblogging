import logging
from logging.handlers import RotatingFileHandler
LOG_FILE = "/home/wjsqorwns93/bj/autoblogging/logs/restaurant_info.log"

# 공통 핸들러
handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(module)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# 로거 생성 함수
def get_logger(name):
    """
    이름에 따라 로거를 생성합니다.
    Args:
        name (str): 로거 이름 (보통 클래스명 또는 모듈명)
    Returns:
        logging.Logger: 설정된 로거 객체
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():  # 핸들러 중복 추가 방지
        logger.addHandler(handler)
    return logger