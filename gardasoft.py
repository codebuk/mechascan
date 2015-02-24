#!/usr/bin/env python3
import re
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)

from enumerate_serial import *


class GardasoftDevice:
    # communications port should be set to 9600 baud, no parity, 8 data bits, 1 stop bit.
    # al characters are echoed so read returns characters sent to device

    def __init__(self):
        log.debug('gardasoft device init')
        self.port = "Not connected"
        self.connected = 0
        self.ver = None
        self.ser = None

    def open(self, comm_port=None):
        self.ver = ""
        self.connected = 0
        if comm_port is None:
            ports = enumerate_physical_serial_ports(check_lock=True)
            for comm_port in ports:
                if self.open_port(comm_port):
                    return True
        else:
            if self.open_port(comm_port):
                return True
        log.warn("Can not find a gardasoft device")
        return False

    def open_port(self, comm_port):
        log.info("Trying port: " + comm_port)
        try:
            collection = [9600, 115200]
            for speeds in collection:
                self.ser = serial.serial_for_url(comm_port, speeds, timeout=.1, writeTimeout=.01)
                log.info("Port opened: " + comm_port)
                try:
                    fcntl.flock(self.ser, fcntl.LOCK_EX | fcntl.LOCK_NB)
                except IOError:
                    log.info("Can not immediately write-lock the file as it is locked: " + comm_port)
                else:
                    log.info("Check for device at: " + str(speeds) + " baud. Port: " + comm_port)
                    self.ser.flush()
                    self.ser.read(2000)  # clear any junk
                    self.connected = 1  # allow clear error to access port
                    if self.clear_error():
                        self.ser.timeout = .1  # tried .01 but random errors
                        self.ver = self.version()
                        self.port = comm_port
                        self.connected = 1
                        return 1
                self.connected = 0
                self.ser.close()
        except serial.SerialException:
            logging.error("Serial exception")
            pass
        except IOError:
            logging.error("Not a Gardasoft device")
            return 0
        
    def write_read(self, mess, read_char):
        if self.connected:
            try:
                self.ser.write(mess)
                self.ser.flush()
                info = self.ser.read(read_char)
                return info.decode("utf-8")
                
            except:
                raise

    def close(self):
        self.connected = 0
        self.port = "Not Connected"
        self.all_off()
        self.ser.close()
        
    def status(self):
        info = repr(self.write_read(b"ST\n\r", 200))
        if info:
            log.debug("Status: " + info)
            return info
        else:
            return ""

    def version(self):
        info = self.write_read(b"VR\n\r", 20)
        if info:
            ver = re.search("\A.*VR(.*)\n\r>\Z", str(info), re.DOTALL)
            if ver:
                name = ver.group(1)
                log.debug('version -' + name)
                return name
            else:
                log.error('version not valid' + repr(info))
                raise Exception('Version not valid')
        return ""
            
    def clear_error(self):
        info = self.write_read(b"GR\n\r", 10)
        if info:
            er = re.search("\A(GR\n\r>)\Z", str(info), re.DOTALL)
            if er:
                log.debug('clear error OK')
                return 1
            log.error("clear error found error. Response: " + repr(info))  # do not raise error on clear error
            er = re.search("GREC1", str(info), re.DOTALL)
            if er:
                log.debug('max current clear ok')
                return 1
            if re.search("GRErr 21", str(info), re.DOTALL):
                log.debug('Err 21 - Bad command format')
                return 1
            if re.search("GRE", str(info), re.DOTALL):
                log.debug('Other error see docs')
                return 1
        return 0
        
    def all_off(self):
        self.continuous(1, 0)
        self.continuous(2, 0)
        log.debug('All off OK')

    def continuous(self, channel, current):
        com = b'RC' + bytes(str(channel), 'ascii') + b'C0V' + bytes(str(current), 'ascii') + b'\n\r'
        z = len(com)
        msg = 'continuous ' + str(channel) + ' - ' + str(current) + " - " + repr(com)
        info = self.write_read(com, z + 1)
        if info is None:
            return 0
        er = re.search("\A" + com.decode("utf-8") + "(>)\Z", info, re.DOTALL)
        if er:
            log.debug(msg)
        else:
            log.error("Send: " + msg + "  len: " + str(z) + " resp size: " + str(len(info)) + " Response: " + str(info))
            raise Exception('Bad continuous response' + repr(info))

    def strobe(self, channel, min_current, max_current, count):
        for count in range(0, count):
            self.continuous(channel, max_current)
            self.continuous(channel, min_current)
        self.all_off()

if __name__ == "__main__":
    import time
    import logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
    #er0-5 give answers...
    led = GardasoftDevice()
    led.open(None)
    if led.connected:
        log.info("LED device connected")
    else:
        log.error("LED device not connected")
    x = led.version()
    if not x:
        log.warn("LED device not connected")
    l = 1
    for l in [1, 2]:
        try:
            led.continuous(l, 2000)
            time.sleep(.3)
            led.continuous(l, 0)
            time.sleep(1)
            led.strobe(l, 0, 4000, 20)
            led.status()
            log.info("Version: " + led.version())
            #for x in range(0, 1000, 1):
            #    led.continuous ( l, x)
            #for x in range(500, 0, -50):
            #    led.continuous ( l, x)
            led.all_off()
            led.clear_error()
        except:
            raise






