#!/usr/bin/env python3

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


import serial
import glob
from serial import *
import fcntl

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)


def enumerate_physical_serial_ports(check_lock=True):
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    ports = []
  
    if sys.platform == 'win32':
        # Iterate through registry because WMI does not show virtual serial ports
        # noinspection PyUnresolvedReferences
        import winreg

        # noinspection PyUnresolvedReferences
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DEVICEMAP\SERIALCOMM')
        except WindowsError:
            return []
        i = 0
        while True:
            # noinspection PyUnresolvedReferences
            try:
                ports.append(winreg.EnumValue(key, i)[1])
                i += 1
            except WindowsError:
                break
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        if os.path.exists('/dev/serial/by-id'):
            entries = os.listdir('/dev/serial/by-id')
            for devs in entries:
                link = os.readlink(os.path.join('/dev/serial/by-id', devs))
                path = os.path.normpath(os.path.join('/dev/serial/by-id', link))
                log.debug(path + " -- " + link + "--" + devs)
                if check_lock:
                    try:
                        ser = serial.Serial(path, 9600, timeout=.1, writeTimeout=.01)
                        log.debug("Port opened: " + path)
                        try:
                            fcntl.flock(ser, fcntl.LOCK_EX | fcntl.LOCK_NB)
                            log.info("Success. Unlocked port available: " + path)
                            ports.extend([path])
                        except OSError:
                            log.info("Can not immediately write-lock file as it is locked. Port is in use: " + path)
                    except:
                        log.info("Can not open port: " + path)
                        raise
                else:
                    log.info("Success. Port available: " + path)
                    ports.extend([path])

        for dev in glob.glob('/dev/ttyS*'):
            # to do add port locking check
            try:
                comm_port = Serial(dev)
            except OSError:
                pass
            else:
                log.debug(dev)
                comm_port.close()
                ports.append(dev)

    else:
        raise EnvironmentError('Unsupported platform')
    return ports


def script():
    for comm_port in enumerate_physical_serial_ports():
        print(comm_port)
    for comm_port in enumerate_physical_serial_ports(check_lock=False):
        print(comm_port)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
    script()
