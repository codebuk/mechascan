#!/usr/bin/env python3
import logging

log = logging.getLogger(__name__)


def read_list():
    return ('bmp', 'gif', 'ico', 'jpg', 'jpeg', 'png', 'pbm',
            'pgm', 'ppm', 'xbm', 'xpm', 'svg', 'svgz', 'mng', 'wbmp',
            'tga', 'tif', 'tiff')


def write_list():
    return ('bmp', 'ico', 'jpg', 'jpeg', 'pbm', 'pgm', 'png',
            'wbmp', 'tif', 'tiff', 'ppm', 'xbm', 'xpm')
