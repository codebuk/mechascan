__author__ = 'dan'
#!/usr/bin/env python3
"""

   ektapro v1.0

   Copyright 2014 Dan Tyrrell


"""
from enumerate_serial import *
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)


class VonError(Exception):
    pass


class VonDevice:
    # Encapsulates the logic to control a Ektapro slide projector.
    def __init__(self):
        self.serial_device = None
        self.port = "Not connected"
        self.connected = False
        self.ready = False


    def open_port(self, comm_port):
        #self.close()
        log.info("Checking port: " + comm_port)
        try:
            self.serial_device = serial.serial_for_url(comm_port, 115200, timeout=.2, writeTimeout=.2)
            try:
                fcntl.flock(self.serial_device, fcntl.LOCK_EX | fcntl.LOCK_NB)
                log.info("Write-lock file ok: " + comm_port)
            except IOError:
                log.info("Can not immediately write-lock file: " + comm_port)
                self.serial_device = None
                return False
            else:
                self.serial_device.write( b"\x02\xa0\x11\x10\x10\x00\x00\xd3\x0d")
                self.info = self.serial_device.read(512)
                # todo use system status as it is not bufferred
                logging.info(str (len (self.info)) + "-" + str(self.info))
                if self.info is None or len(self.info) == 0 \
                        or not (self.info[0] % 8 == 6) \
                        or not (self.info[1] // 16 == 13) \
                        or not (self.info[1] % 2 == 0):
                    logging.info("Not a Von device")
                    self.serial_device = None
                else:
                    self.port = comm_port
                    self.connected = 1
                    return True
        except serial.SerialException:
            pass
        except IOError:
            logging.error("Not a Von device")
        return False

    def open(self, comm_port):
        if comm_port is None:
            ports = enumerate_physical_serial_ports()
            for comm_port in ports:
                if self.open_port(comm_port):
                    break
        else:
            self.open_port(comm_port)
        if self.connected:
            self.reset()  # possible command error from serial bus scanning needs to be cleared. 10 second delay!

    def close(self):
        if self.connected:
            self.serial_device.close()
        self.port = "Not Connected"
        self.connected = 0

    def comms(self, command, read_bytes=0, pre_timeout=0.0, post_timeout=0.0):
        #we do not rely of buffering so check
        #todo can throw 'OSError: [Errno 5] Input/output error'
        if self.serial_device.inWaiting():
            log.debug (self.serial_device.inWaiting())
            rec = self.serial_device.read()
            binary_string = "binary - "
            for c in rec:
                binary_string += bin(c) + " "
            log.debug("Received. " +
                       #"Hex: " + repr(rec)
                       binary_string +
                       " len: " + str(len(rec)))
            raise EktaproError ("junk in buffer")

        rec = bytearray()
        command_bytes = command.to_data()
        if self.log_debug:
            binary_string = ""
            for c in command_bytes:
                binary_string += bin(c) + " "
            log.debug("Send: " + str(command) +
                      #" hex: " + repr(command_bytes) +
                      " bin: " + binary_string +
                      " pre/post timeouts: " + str(pre_timeout) +
                      " - " + str(post_timeout))
        self.poll_busy(pre_timeout, desc="pre timeout ")
        if self.serial_device and not self.serial_device.closed:
            # try:  # might be disconnected or port removed or....
            self.serial_device.write(command_bytes)

            #except:
            #    raise EktaproError ""
        else:
            log.debug("ignore serial write - device not connected")
        if self.serial_device and not self.serial_device.closed and read_bytes:
            # try:
            rec = self.serial_device.read(read_bytes)
            #except:
            #    raise
            if len(rec) != read_bytes:
                msg = "Error reading from device Received: " + repr(rec) + \
                      " len: " + str(len(rec)) + \
                      " requested: " + str(read_bytes)
                raise EktaproError(msg)
            if self.log_debug:
                binary_string = "binary - "
                for c in rec:
                    binary_string += bin(c) + " "
                log.debug("Received. " +
                          #"Hex: " + repr(rec)
                          binary_string +
                          " len: " + str(len(rec)))
        elif read_bytes > 0:
            log.debug("ignore serial read - device not connected")
        self.poll_busy(post_timeout, desc="post timeout ")
        return rec





if __name__ == "__main__":
    import time
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    tpt = VonDevice()
    tpt.open(None)
    if tpt.connected:
        log.info("device connected")
    else:
        log.error("device not connected")


