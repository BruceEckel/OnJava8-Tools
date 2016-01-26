import logging
from logging import debug
# logging.basicConfig(filename= __file__.split('.')[0] + ".log", level=logging.DEBUG)
logging.basicConfig(filename= __file__.replace(".py", ".log"), level=logging.DEBUG)

debug("foo")