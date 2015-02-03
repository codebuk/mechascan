#!/usr/bin/env python3
from glob import glob
import sys, serial,logging
from serial import *

log = logging.getLogger(__name__)

def enumerate(check_lock = None):
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    ports = []
  

    if sys.platform == 'win32':
        # Iterate through registry because WMI does not show virtual serial ports
        import winreg

        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DEVICEMAP\SERIALCOMM')
        except WindowsError:
            return []
        i = 0
        while True:
            try:
                ports.append(winreg.EnumValue(key, i)[1])
                i = i + 1
            except WindowsError:
                break
    elif sys.platform.startswith ('linux') or sys.platform.startswith('cygwin'):
        if os.path.exists('/dev/serial/by-id'):
            entries = os.listdir('/dev/serial/by-id')
            dirs = []
            for devs in entries:
                link = os.readlink(os.path.join('/dev/serial/by-id', devs))
                path = os.path.normpath(os.path.join('/dev/serial/by-id', link))
                log.debug (path + " -- " + link + "--" + devs)
                if (check_lock):
                    try:
                        ser = serial.Serial(path, 9600, timeout=.1, writeTimeout=.01)
                        log.debug ("Port opened: " + path)
                        try:
                            fcntl.flock(ser, fcntl.LOCK_EX | fcntl.LOCK_NB )
                            ports.extend([path])
                        except IOError:
                            log.info( "Can not immediately write-lock the file as it is locked. Port is in use: " + path)
                    except:
                        raise
                        log.info( "Can not open port: " + path)
                else:
                    ports.extend([path])

        for dev in glob('/dev/ttyS*'):
            try:
                port = Serial(dev)
            except (OSError):
                pass
            else:
                log.debug (dev)
                port.close()
                ports.append(dev)
                
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')
    return ports

def script():
    for port in enumerate():
        print(port)
    for port in enumerate(check_lock=True):
        print(port)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
    script()
