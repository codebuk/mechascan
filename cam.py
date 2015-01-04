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

import logging
log = logging.getLogger(__name__)
import gphoto2 as gp

class CameraDevice:
    def __init__(self):
        log.debug('cam device init')
        
    def __del__(self, type, value, traceback):
        log.debug('cam device exit')
        self.close()
        
    def set_config(self, camera, context, name, value):
        # get configuration tree
        config = gp.check_result(gp.gp_camera_get_config(camera, context))
        widget_child = gp.check_result (gp.gp_widget_get_child_by_name(config, name))
        widget_type = gp.check_result(gp.gp_widget_get_type(widget_child))
        widget_value = gp.check_result(gp.gp_widget_get_value(widget_child))
        gp.check_result(gp.gp_widget_set_value(widget_child, value))
        gp.check_result(gp.gp_camera_set_config(camera, config, context))
        log.info ( name + " type : " + str(widget_type) + " old value : " + str(widget_value) + " new value : " + value)

    def open(self):
        gp.check_result(gp.use_python_logging())
        self.camera = gp.check_result(gp.gp_camera_new())
        self.context = gp.gp_context_new()
        gp.check_result(gp.gp_camera_init(self.camera, self.context))
        self.set_config ( self.camera, self.context, 'capturetarget', 'sdram' )

    def capture(self):
        error, self.path = gp.gp_camera_capture(self.camera, gp.GP_CAPTURE_IMAGE , self.context)
        if (error):
            log.error ("Image capture failed " + str(error))
            return 0
        log.info ("Image captured to: " + self.path.folder + self.path.name )
        return 1            

    def save (self,name):    
        camera_file = gp.check_result(gp.gp_camera_file_get(
                self.camera, self.path.folder, self.path.name, gp.GP_FILE_TYPE_NORMAL, self.context))
        gp.check_result(gp.gp_file_save(camera_file, name))
        gp.check_result(gp.gp_camera_file_delete(self.camera, self.path.folder, self.path.name, self.context))

    def close(self):
        log.debug('cam device close')
        try:
            gp.check_result(gp.gp_camera_exit(self.camera, self.context))
        except:
            log.info ("Error closing camera - not opened?") 
        return 0
