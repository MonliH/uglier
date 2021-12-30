import logging

from colored_logger import ColoredFormatter
from patcher import Patcher

logger = logging.getLogger("uglier")
logger.setLevel(logging.WARNING)
sh = logging.StreamHandler()
sh.setFormatter(ColoredFormatter())
logger.addHandler(sh)

patcher = Patcher()
patcher.patch_file("./test/test_basic.py")
