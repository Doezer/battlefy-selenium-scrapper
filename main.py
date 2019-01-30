#  -*- coding: utf-8 -*-
import contextlib
import logging
import os
import sys
import time

from battlefy_helper import get_tournaments

# To enable debug level (see setup_logging)
DEBUG = False
# select between lol, fortnite, cod_bo4, hs, ow, pubg, fifa, c-ops, ssbu, shadowverse, qc
GAME = 'ow'
# see get_tournaments docstring. Default = Global
REGION = ''
# see get_tournaments docstring. Default = Any Platform
PLATFORM = ''
# see get_tournaments docstring. Default = Any Format. All games have this critera available.
TYPE = ''


@contextlib.contextmanager
def setup_logging():
    logger = logging.getLogger()
    try:
        if os.environ["DEBUG"]:
            logger.setLevel(logging.DEBUG)
    except KeyError:
        if DEBUG:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    try:

        s_handler = logging.StreamHandler(stream=sys.stdout)
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter(
            '%(asctime)s %(levelname)-5.5s [%(name)s] [%(funcName)s()] %(message)s <line %(lineno)d>',
            dt_fmt,
            style='%')
        for handler in [s_handler]:
            handler.setFormatter(fmt)
            logger.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = logger.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            logger.removeHandler(hdlr)


if __name__ == '__main__':
    with setup_logging():
        tn_list = get_tournaments(game=GAME, region=REGION, platform=PLATFORM, type=TYPE)
        logging.debug(tn_list)
        for tn in tn_list:
            logging.info(f"{'#' * 80}")
            logging.info(tn['url'])
            logging.info(tn['prize'])
            logging.info(tn['name'])
            logging.info(time.strftime('%a, %d %b %Y %H:%M:%S', tn['date']))
            logging.info(tn['region'])
            logging.info(tn['org'])
