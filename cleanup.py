#!/usr/bin/env python3

from ipp import *
import os


if __name__ == '__main__':
    rootdir = '/home/dan/Downloads/robandsylvia/'
    outroot = '/home/dan/Downloads/robandsylviacomplete/'
    os.mkdir (outroot)
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            fn = os.path.join(subdir, file)
            if os.path.isfile(fn) and fn.endswith(".jpg"):
                fnc = fn
                folders = []
                while 1:
                    fnc, folder = os.path.split(fnc)
                    if folder != "":
                        folders.append(folder)
                    else:
                        if fnc != "":
                            folders.append(fnc)
                        break
                folders.reverse()
                print (folders)
                print (folders[-2])

                newfn = outroot + folders[-2] + '_' + folders[-1]
                print (newfn)
                f = Ipp()
                f.open(fn)
                f.remove_border()
                f.flip_horizontal()
                f.save(newfn)


