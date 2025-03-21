import logging

logging.basicConfig(
    format="%(asctime)s [%(name)s%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", encoding="utf-8"),
    ]
)

def new_logger(name: str = '') -> logging.Logger:
    return logging.getLogger(f'{name}/' if name else name)
