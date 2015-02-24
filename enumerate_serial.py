#!/usr/bin/env python3
import serial
import glob
from serial import *

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
                        except IOError:
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
