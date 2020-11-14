#!/usr/bin/env python3
"""

   ektapro

   Copyright 2014 2015 Dan Tyrrell

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

   Class for the ektapro slide projector devices.
   One projector per serial port is supported.
"""
from enumerate_serial import *
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)


class EktaproError(Exception):
    pass


class EktaproDevice:
    # Encapsulates the logic to control a Ektapro slide projector.
    def __init__(self):
        self.is_busy = True
        #self.slide = None
        self.slot = None
        self.slide_in_gate = False
        self.tray_size = 80  # this allows dummy scanning
        self.max_display_tray = 140
        self.id = 0
        self.version = ""
        self.type = 0
        self.serial_device = None
        self.port = "Not connected"
        self.connected = False
        self.ready = False
        self.status_valid = False
        self.log_debug = True
        self.reset_time_out = 10
        self.standby = 0
        self.auto_zero = False
        self.resetting = False
        self.busy = False
        self.at_zero_position = False
        self.slide_lift_motor_error = False
        self.tray_transport_motor_error = False
        self.command_error = False

        self.80_tray_steps = 47
        self.140_tray_steps = 27

    def open_port(self, comm_port):
        # self.close()
        log.info("Checking port: " + comm_port)
        try:

        except serial.SerialException:
            pass
        except IOError:
            logging.error("Not a Ektapro device")
        return False

    def open(self, comm_port):
        if comm_port is None:
            ports = enumerate_physical_serial_ports()
            for comm_port in ports:
                if self.open_port(comm_port):
            # keep checking for second tic break
        else:
            self.open_port(comm_port)
        if self.connected:
            self.reset()  # possible command error from serial bus scanning needs to be cleared. 10 second delay!

    def close(self):
        log.debug('ektapro device close')
        if self.connected:
            self.serial_device.close()
        self.port = "Not Connected"
        self.connected = 0
        self.system_status_clear()
        self.system_return_clear()

    def toggle_standby(self):
        self.standby = not self.standby
        self.set_standby(self.standby)

    def __str__(self):
        self.get_model()

    def get_version(self):
        return self.version

    def set_tray_slots(self, slots):
        self.tray_size = slots

    def reset(self):
        # SLIDE LIFT MOTOR rotates clockwise(max.of 805 steps = one SLIDE LIFTER cycle).
        # If SENSOR SIGNAL changes from not actuated to  actuated, the SLIDE LIFTER is in up position.

        if self.connected:
            self.busy = True
            ts = time.time()

            log.debug("reset polled for: " + str(time.time() - ts))
            self.slide = 0
            # self.get_system_return()
            self.get_status()  # update internal status

    #goto specific slot and load slide
    def select(self, slot):
        self.slot = slot
        self.lifter_up()
        #move

        self.lifter_down()
        self.get_status()

    def next(self, pre_timeout=0, post_timeout=0):
        self.slot += 1
        if self.slot > self.tray_size:
            self.slot = 0
        self.select()

    def prev(self, pre_timeout=0, post_timeout=1.5):
        self.slot -= 1
        if self.slot == -1:
            self.slot = self.tray_size
        self.select()

    def status_get_tray_position(self):
        return self.slot

    def poll_busy(self, time_out=0.0, desc=""):
        if not self.connected:
            return
        if time_out == 0:
            return
        log.debug("busy wait for: " + str(time_out))
        busy = True
        ts = time.time()
        # turn off logging so we do not spam logs
        if time_out > 0:
            while busy:
                self.log_debug = False
                busy = self.get_status(busy_check=True)
                self.log_debug = True
                if time.time() - ts > time_out:
                    log.error("Busy " + desc + " timeout: " + str(time_out))
                    raise EktaproError("Busy timeout")
            log.debug(desc + "polled for: " + str(time.time() - ts))
        self.log_debug = True

    # primary method to get status of projector -will invoke both type of system status checks
    # busy_check is fast path for just checking if busy
    def get_status(self, busy_check=False):
        busy = self.get_system_status()
        msg = ""
        if self.slide_lift_motor_error:
            msg = "slide_lift_motor_error\n"
        if self.tray_transport_motor_error:
            msg += "tray_transport_motor_error\n"
        return busy

    # return True if busy
    def get_system_status(self):
        self.status_valid = False
        if self.connected:
            self.status_valid = True
        if self.status_valid:
        else:
            self.clear()
        return self.busy

    def clear(self):
        self.status_valid = False
        self.resetting = False
        self.busy = 0
        self.at_zero_position = 0
        self.slide_lift_motor_error = 0
        self.tray_transport_motor_error = 0
        self.info = None
        self.type = None
        self.version = None
        self.auto_zero = None
        self.tray_size = 80
        self.active_lamp = None
        self.standby = None
        self.high_light = None
        self.slot = 0
        self.slide_in_gate = None
        self.highlight = None

    def get_slide_in_gate(self):
        return self.slide_in_gate # 1 slide in gate

    def get_details(self, extended=True):
        if self.connected:
            det = "Busy: " + str(self.busy) \
                + " Home: " + str(self.at_zero_position) \
                + " Reset:" + str(self.resetting) \
                + " SLME:" + str(self.slide_lift_motor_error) \
                + " TTME:" + str(self.tray_transport_motor_error) \
                + "\n Model: " + self.get_model() \
                           + " Slot: " + str(self.slot) \
                           + " Tray size: " + str(self.tray_size) \
                           + " Slide in gate: " + ("Yes" if self.slide_in_gate == 1 else "No") \
        return det
                    # secondary method to get status - adds some more info

                if len(self.info) == 5:
                    info = self.info
                    # self.id = info[0] / 16 - do not change based on returned values
                    self.type = int(info[2] // 16)
                    self.version = str(int(info[2] % 16)) + "." + str(int(info[3] // 16)) + str(int(info[3] % 16))
                    self.power_frequency = (info[4] & 128) // 128
                    self.auto_focus = (info[4] & 64) // 64
                    self.auto_zero = (info[4] & 32) // 32
                    self.tray_size = 140 if (info[4] & 8) == 1 else 80

                else:
                    log.error("get_system_return invalid response")
                    raise EktaproError("get_system_return invalid response")
            else:
                self.system_return_clear()

if __name__ == "__main__":
    import time
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    tpt = EktaproDevice()
    tpt.open(None)
    if tpt.connected:
        log.info("EktaproDevice device connected")
    else:
        log.error("EktaproDevice device not connected")
    log.debug(tpt.get_version())
    tpt.reset()
    log.debug(tpt.get_details())

    log.info('sync :' + str(tpt.status_get_tray_position()))

    for l in [1, 2, 3, 4]:
        tpt.next(20, 20)
        log.info('sync :' + str(tpt.status_get_tray_position()) + "   in gate: " + str(tpt.slide_in_gate))