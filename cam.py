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


# https://github.com/codebuk/python-gphoto2/commit/588e0e0b81f9bd8d6eab5ef1dbac9bab31d3510f

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
        self.summary = ""
        self.connected = True
        self.config = None
        self.port = "Auto"
        self.capture_ok = False
        #self.list_cameras

    # noinspection PyUnresolvedReferences
    def set_config(self, camera, context, name, value):
        if self.connected:
            # get configuration tree
            log.debug('set config')
            # noinspection PyUnresolvedReferences
            self.config = gp.check_result(gp.gp_camera_get_config(camera, context))
            try:
                # noinspection PyUnresolvedReferences
                widget_child = gp.check_result(gp.gp_widget_get_child_by_name(self.config, name))
            except gp.GPhoto2Error as ex:
                if ex.code == gp.GP_ERROR_BAD_PARAMETERS:
                    log.error("Bad parameters")
                    return False
                raise

            # noinspection PyUnresolvedReferences
            widget_type = gp.check_result(gp.gp_widget_get_type(widget_child))
            log.debug("Widget type: " + str(widget_type))
            # check value in range
            count = gp.check_result(gp.gp_widget_count_choices(widget_child))
            log.debug("Count choices: " + str(count))
            if value < 0 or value >= count:
                log.debug('Parameter out of count choices range')
            str_value = gp.check_result(gp.gp_widget_get_choice(widget_child, value))
            log.debug("Get choice repr: " + str_value)
            widget_value = gp.check_result(gp.gp_widget_get_value(widget_child))
            log.debug("Get value: " + widget_value)
            # noinspection PyUnresolvedReferences
            gp.check_result(gp.gp_widget_set_value(widget_child, str_value))
            gp.check_result(gp.gp_camera_set_config(camera, self.config, context))

    def use_sdram(self):
        self.set_config(self.camera, self.context, 'capturetarget', 0)

    # noinspection PyUnresolvedReferences
    def open(self):
        self.connected = False
        log.debug('open')
        gp.check_result(gp.use_python_logging())
        self.context = gp.gp_context_new()
        try:
            self.camera = gp.check_result(gp.gp_camera_new())
            self.camera.init(self.context)
            self.summary = self.camera.get_summary(self.context)
            log.debug(str(self.summary))
            log.debug('init camera')
            self.connected = True
        except gp.GPhoto2Error as ex:
            if ex.code == gp.GP_ERROR_MODEL_NOT_FOUND:
                log.debug("No camera found")
                return False
            elif ex.code == gp.GP_ERROR_IO_USB_CLAIM:
                log.debug("Camera in use by another process: " + ex.string)
                return False
            # some other error we can't handle here
            raise

    # noinspection PyUnresolvedReferences
    def capture(self):
        if self.connected:
            log.debug('capture')
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
        log.debug('Save image to:' + name)
        if not self.connected:
            log.error("Cannot save - camera not connected")
            return False
        if not self.capture_ok:
            log.error("Cannot save - no valid capture to save")
            return False
        # noinspection PyUnresolvedReferences
        camera_file = gp.check_result(gp.gp_camera_file_get(
            self.camera, self.path.folder, self.path.name, gp.GP_FILE_TYPE_NORMAL, self.context))
        # noinspection PyUnresolvedReferences
        gp.check_result(gp.gp_file_save(camera_file, name))
        # noinspection PyUnresolvedReferences
        gp.check_result(gp.gp_camera_file_delete(self.camera, self.path.folder, self.path.name, self.context))

    def list_cameras(self):

        #context = gp.gp_context_new()
        if hasattr(gp, 'gp_camera_autodetect'):
            # gphoto2 version 2.5+
            cameras = gp.check_result(gp.gp_camera_autodetect(self.context))
        else:
            # noinspection PyUnresolvedReferences
            port_info_list = gp.check_result(gp.gp_port_info_list_new())
            # noinspection PyUnresolvedReferences
            gp.check_result(gp.gp_port_info_list_load(port_info_list))
            # noinspection PyUnresolvedReferences
            abilities_list = gp.check_result(gp.gp_abilities_list_new())
            # noinspection PyUnresolvedReferences
            gp.check_result(gp.gp_abilities_list_load(abilities_list, self.context))
            # noinspection PyUnresolvedReferences
            cameras = gp.check_result(gp.gp_abilities_list_detect(
            abilities_list, port_info_list, self.context))
            n = 0
            for name, value in cameras:
                log.debug('Camera number :' + str(n) + ' Name: ' + name + ' Value: ' + value)
                n += 1
        return cameras

    def close(self):
        self.capture_ok = False
        if self.connected:
            log.debug('cam device close')
            # noinspection PyUnresolvedReferences
            gp.check_result(gp.gp_camera_exit(self.camera, self.context))
            #gp.gp_camera_exit(self.camera, self.context)
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
