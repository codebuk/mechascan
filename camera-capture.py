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

from __future__ import print_function

from datetime import datetime
import logging, os
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
log = logging.getLogger(__name__)
import sys
import time

import gphoto2 as gp

def set_config(camera, context, name, value):
    # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera, context))
    widget_child = gp.check_result (gp.gp_widget_get_child_by_name(config, name))
    widget_type = gp.check_result(gp.gp_widget_get_type(widget_child))
    widget_value = gp.check_result(gp.gp_widget_get_value(widget_child))
    logging.info ( name + " type : " + str(widget_type) + " old value : " + str(widget_value))
    gp.check_result(gp.gp_widget_set_value(widget_child, value))
    gp.check_result(gp.gp_camera_set_config(camera, config, context))
    logging.info ( name + " type : " + str(widget_type) + " old value : " + str(widget_value) + " new value : " + value)
    return False

def main():
    #logger = logging.getLogger("gp")
    gp.check_result(gp.use_python_logging())
    # open camera connection
    camera = gp.check_result(gp.gp_camera_new())
    context = gp.gp_context_new()
    gp.check_result(gp.gp_camera_init(camera, context))
    set_config ( camera, context, 'capturetarget', 'sdram' )
    error, path = gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE , context)
    print (path.name)
    print (path.folder)
    error, camera_file =  gp.gp_camera_file_get ( camera, path.folder, path.name, gp.GP_FILE_TYPE_NORMAL , context)

    #cam_file = ctypes.c_void_p()  
    #fd = os.open('image.jpg', os.O_CREAT | os.O_WRONLY)  
    #gp.gp_file_new_from_fd(fd)  
    #gp.gp_camera_file_get(camera, path.folder,path.name, gp.GP_FILE_TYPE_NORMAL, camera_file,  context)

    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, path.folder, path.name, gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(camera_file, "1.cr2"))


    
##gp.gp_camera_file_delete(camera,  
##                         cam_path.folder,  
##                         cam_path.name,  
##                         context)  
##gp.gp_file_unref(cam_file) 


    
    log.info ( unicode (camera_file))
    # clean up
    gp.check_result(gp.gp_camera_exit(camera, context))
    return 0

if __name__ == "__main__":
    sys.exit(main())


#photo2 --set-config capturetarget=0 --set-config drivemode=0 --set-config eosviewfinder=0 --set-config output=0 --set-config autofocusdrive=0 --set-config eosremoterelease=4 --wait-event=1s --set-config eosremoterelease=3
#gphoto2 --set-config capturetarget=0 --set-config drivemode=0 --set-config eosviewfinder=0 --set-config output=1 --set-config autofocusdrive=0 --filename test.jpg --capture-image-and-download 
