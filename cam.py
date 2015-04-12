#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#https://github.com/codebuk/python-gphoto2/commit/588e0e0b81f9bd8d6eab5ef1dbac9bab31d3510f

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)
import gphoto2 as gp


class CameraDevice:
    def __init__(self):
        log.debug('cam device init')
        self.camera = None
        self.path = None
        self.context = None
        self.connected = True
        self.config = None
        self.port = "Auto"
        self.capture_ok = False


    def set_config(self, camera, context, name, value):
        # get configuration tree
        log.debug('set config')
        # noinspection PyUnresolvedReferences
        self.config = gp.check_result(gp.gp_camera_get_config(camera, context))
        # noinspection PyUnresolvedReferences
        widget_child = gp.check_result(gp.gp_widget_get_child_by_name(self.config, name))
        # widget_type = gp.check_result(gp.gp_widget_get_type(widget_child))
        # widget_value = gp.check_result(gp.gp_widget_get_value(widget_child))
        # noinspection PyUnresolvedReferences
        gp.check_result(gp.gp_widget_set_value(widget_child, value))
        # noinspection PyUnresolvedReferences
        gp.check_result(gp.gp_camera_set_config(camera, self.config, context))
        # log.info ( name + " type : " + str(widget_type) + " old value : " +
        # str(widget_value) + " new value : " + value)


    def use_sdram (self):
        self.set_config ( self.camera, self.context, 'capturetarget', 'sdram' )


    def open(self):
        log.debug('open')
        gp.check_result(gp.use_python_logging())
        log.debug('allocate memory')
        # noinspection PyUnresolvedReferences
        #gp.gp_camera_new()
        # noinspection PyUnresolvedReferences
        self.camera = gp.check_result(gp.gp_camera_new())
        # noinspection PyUnresolvedReferences
        self.context = gp.gp_context_new()
        log.debug('init camera')
        # noinspection PyUnresolvedReferences
        gp.check_result(gp.gp_camera_init(self.camera, self.context))
        #gp.gp_camera_init(self.camera, self.context)
        self.connected = True

    def capture(self):
        if self.connected:
            log.debug('capture')
            # noinspection PyUnresolvedReferences
            error, self.path = gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE, self.context)
            if error:
                log.error("Image capture failed " + str(error))
                self.capture_ok = False
                return False
            log.info("Image captured to: " + self.path.folder + self.path.name)
            self.capture_ok = True
            return True
        else:
            log.debug('no connected - no capture')
            self.capture_ok = False
            return False

    def save(self, name):
        log.debug('save')
        if self.capture_ok:
            # noinspection PyUnresolvedReferences
            camera_file = gp.check_result(gp.gp_camera_file_get(
                self.camera, self.path.folder, self.path.name, gp.GP_FILE_TYPE_NORMAL, self.context))
            # noinspection PyUnresolvedReferences
            gp.check_result(gp.gp_file_save(camera_file, name))
            # noinspection PyUnresolvedReferences
            #gp.check_result(gp.gp_camera_file_delete(self.camera, self.path.folder, self.path.name, self.context))
        else:
            log.info("save failed")

    def close(self):
        if self.connected:
            log.debug('cam device close')
            # gp.check_result(gp.gp_camera_exit(self.camera, self.context))
            # noinspection PyUnresolvedReferences
            gp.gp_camera_exit(self.camera, self.context)
            # log.info("Error closing camera - not opened?")
            self.connected = False
            return 0

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(module)s %(message)s',
                        datefmt='%H:%M:%S')
    logit = logging.getLogger('gphoto2')
    logit.setLevel(logging.INFO)

    for x in range(0, 1):
        t = CameraDevice()
        t.open()
        t.use_sdram()
        ok = t.capture()
        f = "test.jpg"
        log.debug("Capture complete - Now save file: " + f)
        t.save(f)
        t.close()
