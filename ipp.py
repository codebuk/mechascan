#!/usr/bin/env python3
"""

   ipp

   Copyright 2014 2015 Dan Tyrrell

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import numpy as np
import cv2
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)

# class IppError(Exception):
#    pass


class Ipp:
    def __init__(self):
        print("dddd")
        self.original = None
        self.img = None

    def open(self, name):
        # keep a copy of original image
        self.original = cv2.imread(name)
        #self.img = self.original.copy()
        self.img = cv2.imread(name, 0)

    def save(self, name):
        cv2.imwrite(name, self.img)

    def remove_border(self):
        # Read the image, convert it into grayscalecv2.CV_LOAD_IMAGE_GRAYSCALE
        # todo cv2.CV_LOAD_IMAGE_GRAYSCALE
        # img = cv2.imread(IMG_IN,0)
        # use binary threshold, all pixel that are beyond 3 are made white
        _, thresh_original = cv2.threshold(self.img, 3, 255, cv2.THRESH_BINARY)
        # Now find contours in it.
        #thresh = cv2.copy(thresh_original)
        z, contours, y = cv2.findContours(thresh_original, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # get contours with highest height
        lst_contours = []
        for cnt in contours:
            ctr = cv2.boundingRect(cnt)
            lst_contours.append(ctr)
        x, y, w, h = sorted(lst_contours, key=lambda coef: coef[3])[-1]
        print(x, y, w, h)
        self.img = self.original[y:y + h, x:x + w]

    def flip_horizontal(self):
        self.img = cv2.flip(self.img, flipCode = 1)
