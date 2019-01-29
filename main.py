#  -*- coding: utf-8 -*-
import contextlib
import logging
import os
import sys

from battlefy_helper import get_bfy_tournaments_page

DEBUG = True


@contextlib.contextmanager
def setup_logging():
    logger = logging.getLogger()
    try:
        if os.environ["DEBUG"] or DEBUG:
            logger.setLevel(logging.DEBUG)
    except KeyError:
        logger.setLevel(logging.INFO)
    try:

        # if not os.path.exists("log/"):  # Check if the directory exists
        #     os.makedirs("log/")  # Create it if not
        # log_filename = 'log/bot_{}.log'.format(time.strftime("%Y%m%d-%H%M%S"))
        # f_handler = logging.FileHandler(filename=log_filename, encoding='utf-8', mode='w')
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
        tn_list = get_bfy_tournaments_page('ow')
        logging.debug(tn_list)
