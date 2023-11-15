import logging

def read_opac(filename):
    logging.info('read_opac:' + filename)
    lines = open(filename).readlines()
    logging.debug(lines)

