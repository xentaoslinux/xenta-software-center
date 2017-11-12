import logging

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG.addHandler(handler)
