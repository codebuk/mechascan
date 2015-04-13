#!/usr/bin/env python3
"""

   ektapro v1.0
   
   Copyright 2010 Julian Hoch
   Copyright 2014 Dan Tyrrell

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
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
        self.max_brightness = 100
        self.brightness = 0
        self.slide = None
        self.tray_size = 80  # this allows dummy scanning
        self.max_display_tray = 140
        self.info = bytearray()
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
        self.auto_focus = False
        self.auto_zero = False
        self.low_lamp = False
        self.active_lamp = 0
        self.high_light = False
        self.resetting = False
        self.unknown_flag2 = False
        self.lamp1_status = False
        self.lamp2_status = False
        self.power_frequency = 0
        self.busy = False
        self.at_zero_position = False
        self.slide_lift_motor_error = False
        self.tray_transport_motor_error = False
        self.command_error = False
        self.overrun_error = False
        self.buffer_overflow_error = False
        self.framing_error = False
        self.slot = 0
        self.slide_in_gate = False
        self.highlight = False

    def open_port(self, comm_port):
        # self.close()
        log.info("Checking port: " + comm_port)
        try:
            self.serial_device = serial.serial_for_url(comm_port, 9600, timeout=.1, writeTimeout=1)
            try:
                fcntl.flock(self.serial_device, fcntl.LOCK_EX | fcntl.LOCK_NB)
                log.info("Write-lock file ok: " + comm_port)
            except IOError:
                log.info("Can not immediately write-lock file: " + comm_port)
                self.serial_device = None
                return False
            else:
                self.serial_device.flushInput()
                self.serial_device.flushOutput()
                self.serial_device.write(EktaproCommand(0).status_system_status().to_data())
                info = self.serial_device.read(3)
                if info is None or len(info) == 0 or not (info[0] % 8 == 6) or not info[2] % 4 == 3:
                    logging.info("Not a Ektapro device")
                    self.serial_device = None
                else:
                    self.port = comm_port
                    self.connected = 1
                    self.serial_device.timeout = 10
                    logging.info("Ektapro device detected on :" + comm_port)
                    return True
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
                    break
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

    def get_model(self):
        model_strings = {
            0: "Unknown",
            7: "4010 / 7000",
            4: "4020",
            5: "5000",
            6: "5020",
            8: "7010 / 7020",
            9: "9000",
            10: "9010 / 9020"
        }
        return "Kodak Ektapro model: " \
               + model_strings.get(self.type, "Unknown") \
               + " Id: " + str(self.id) \
               + " Version: " + str(self.version)

    def get_version(self):
        return self.version

    def set_standby(self, on):
        self.comms(EktaproCommand(self.id).set_standby(on))

    def set_auto_focus(self, on):
        self.comms(EktaproCommand(self.id).set_auto_focus(on))

    def set_brightness(self, brightness):
        self.comms(EktaproCommand(self.id).param_set_brightness(brightness * 10))
        self.brightness = brightness

    def soft_reset(self):
        self.set_standby(False)
        self.set_auto_focus(False)
        self.select(1)
        self.set_brightness(0)
        self.standby = False

    def reset(self):
        # when reset device might respond with not busy
        #there is a an undocumented flag used to indicate reset is complete
        #if the next call
        self.comms(EktaproCommand(self.id).direct_reset_system())
        # while resetting it is possible no serial response so poll up to 10 seconds looking for a response
        time.sleep(2)  # stop useless polling & command error if any less
        self.serial_device.flushInput()
        self.serial_device.flushOutput()
        ts = time.time()
        while True:
            self.get_system_status()
            log.debug(self.get_details(extended=False))
            if not self.resetting and not self.busy:
                break
            time.sleep(.5)
            if time.time() - ts > self.reset_time_out:
                log.error("Reset timeout: " + str(self.reset_time_out))
                raise EktaproError("Reset timeout")
        log.debug("reset polled for: " + str(time.time() - ts))
        self.slide = 0
        #self.get_system_return()
        self.get_status()  # update internal status

    def clear_error_flag(self):
        self.comms(EktaproCommand(self.id).direct_clear_error_flag())

    def select(self, slide):
        self.comms(EktaproCommand(self.id).param_random_access(slide), pre_timeout=0, post_timeout=10)
        self.get_status()
        self.slide = slide

    def next(self, pre_timeout=0, post_timeout=0):
        self.comms(EktaproCommand(self.id).direct_slide_forward(), pre_timeout=pre_timeout, post_timeout=post_timeout)
        self.slide += 1
        if self.slide > self.tray_size:
            self.slide = 0

    def prev(self, pre_timeout=0, post_timeout=1.5):
        self.comms(EktaproCommand(self.id).direct_slide_backward(), pre_timeout=pre_timeout, post_timeout=post_timeout)
        self.slide -= 1
        if self.slide == -1:
            self.slide = self.tray_size

    def status_get_tray_position(self):
        reply = self.comms(EktaproCommand(self.id).status_get_tray_position(), read_bytes=3)
        if self.connected:
            if (len(reply) != 3) \
                    or not (reply[0] % 8 == 6) \
                    or not (reply[1] // 16 == 10):
                log.error("get_status invalid response")  # could raise error here?
            else:
                self.slot = int(reply[2])
                self.slide_in_gate = (reply[1] & 8) // 8
                self.active_lamp = (reply[1] & 4) // 4
                self.standby = (reply[1] & 2) // 2
                self.highlight = reply[1] & 1
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
        if self.command_error:
            msg += "command_error\n"
        if self.overrun_error:
            msg += "overrun_error\n"
        if self.buffer_overflow_error:
            msg += "buffer_overflow_error\n"
        if self.framing_error:
            msg += "framing_error\n"
        if len(msg):
            log.error("Get_status error detected: " + msg)  # could raise error here?
            log.debug(self.get_details())
            raise EktaproError(msg)
        if not busy_check:
            self.get_system_return()  # get the other status data
            self.status_get_tray_position()
            log.debug(self.get_details())  # dump it all
        return busy

    # secondary method to get status - adds some more info
    def get_system_return(self):
        self.info = self.comms(EktaproCommand(self.id).status_system_return(), read_bytes=5)
        if self.connected:
            if len(self.info) == 5:
                info = self.info
                # self.id = info[0] / 16 - do not change based on returned values
                self.type = int(info[2] // 16)
                self.version = str(int(info[2] % 16)) + "." + str(int(info[3] // 16)) + str(int(info[3] % 16))
                self.power_frequency = (info[4] & 128) // 128
                self.auto_focus = (info[4] & 64) // 64
                self.auto_zero = (info[4] & 32) // 32
                self.low_lamp = (info[4] & 16) // 16
                self.tray_size = 140 if (info[4] & 8) == 1 else 80
                self.active_lamp = (info[4] & 4) // 4
                self.standby = (info[4] & 2) // 2
                self.high_light = info[4] & 1
            else:
                log.error("get_system_return invalid response")
                raise EktaproError("get_system_return invalid response")
        else:
            self.system_return_clear()

    def system_return_clear(self):
        self.info = None
        self.type = None
        self.version = None
        self.power_frequency = None
        self.auto_focus = None
        self.auto_zero = None
        self.low_lamp = None
        self.tray_size = 80
        self.active_lamp = None
        self.standby = None
        self.high_light = None
        self.slot = 0
        self.slide_in_gate = None
        self.highlight = None

    # return True if busy
    def get_system_status(self):
        reply = self.comms(EktaproCommand(self.id).status_system_status(), read_bytes=3)
        self.status_valid = False
        if self.connected:
            if len(reply) == 3:
                msg = ""
                if not reply[0] % 8 == 6:
                    msg = "get_system_status byte 0 invalid response\n"
                # if not reply[1] % 64 == 3:  # should be 11XX XXXX  documentation seems to be incorrect:-)
                # msg += msg + "get_system_status byte 1 invalid response\n"
                if not reply[2] % 4 == 3:
                    msg += "get_system_status byte 2 invalid response"
                if len(msg):
                    log.error(msg)
                    raise EktaproError(msg)
                else:
                    self.status_valid = True
        if self.status_valid:
            # self.projector_id = s[0] // 8 - do not change based on returned values
            self.resetting = (reply[1] & 16) // 16  # this is undocumented - seems to be on after reset process
            self.unknown_flag2 = (reply[1] & 32) // 32
            self.lamp1_status = (reply[1] & 8) // 8
            self.lamp2_status = (reply[1] & 4) // 4
            self.busy = (reply[1] & 2) // 2
            self.at_zero_position = reply[1] & 1
            self.slide_lift_motor_error = (reply[2] & 128) // 128
            self.tray_transport_motor_error = (reply[2] & 64) // 64
            self.command_error = (reply[2] & 32) // 32
            self.overrun_error = (reply[2] & 16) // 16
            self.buffer_overflow_error = (reply[2] & 8) // 8
            self.framing_error = (reply[2] & 4) // 4
        else:
            self.system_status_clear()

        if self.busy == 1:
            self.is_busy = True
        else:
            self.is_busy = False
        return self.busy

    def system_status_clear(self):
        self.status_valid = False
        self.resetting = False
        self.unknown_flag2 = 0
        self.lamp1_status = 0
        self.lamp2_status = 0
        self.busy = 0
        self.at_zero_position = 0
        self.slide_lift_motor_error = 0
        self.tray_transport_motor_error = 0
        self.command_error = 0
        self.overrun_error = 0
        self.buffer_overflow_error = 0
        self.framing_error = 0

    def get_slide_in_gate(self):
        self.status_get_tray_position()
        return self.slide_in_gate

    def comms(self, command, read_bytes=0, pre_timeout=0.0, post_timeout=0.0):
        # we do not rely of buffering so check
        #todo can throw 'OSError: [Errno 5] Input/output error'
        if self.serial_device.inWaiting():
            log.debug(self.serial_device.inWaiting())
            rec = self.serial_device.read()
            binary_string = "binary - "
            for c in rec:
                binary_string += bin(c) + " "
            log.debug("Received. " +
                      #"Hex: " + repr(rec)
                      binary_string +
                      " len: " + str(len(rec)))
            raise EktaproError("junk in buffer")

        rec = bytearray()
        command_bytes = command.to_data()
        if self.log_debug:
            binary_string = ""
            for c in command_bytes:
                binary_string += bin(c) + " "
            log.debug("Send: " + str(command) +
                      #" hex: " + repr(command_bytes) +
                      " : " + binary_string +
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
                log.debug(msg)
                #raise EktaproError(msg)
            if self.log_debug:
                binary_string = "binary - "
                for c in rec:
                    binary_string += bin(c) + " "
                log.debug("Received " +
                          #"Hex: " + repr(rec)
                          binary_string +
                          " len: " + str(len(rec)))
        elif read_bytes > 0:
            log.debug("ignore serial read - device not connected")
        self.poll_busy(post_timeout, desc="post timeout ")
        return rec

    def get_details(self, extended=True):
        det = "Busy: " + str(self.busy) \
              + " Home: " + str(self.at_zero_position) \
              + " Reset:" + str(self.resetting) \
              + " F2:" + str(self.unknown_flag2) \
              + " SLME:" + str(self.slide_lift_motor_error) \
              + " TTME:" + str(self.tray_transport_motor_error) \
              + " CE:" + str(self.command_error) \
              + " BOE:" + str(self.buffer_overflow_error) \
              + " OE:" + str(self.overrun_error) \
              + " FE:" + str(self.framing_error) \
              + " L1:" + str(self.lamp1_status) \
              + " L2:" + str(self.lamp2_status)
        if extended:
            det += "\n Model: " + self.get_model() \
                   + " Slot: " + str(self.slot) \
                   + " Tray size: " + str(self.tray_size) \
                   + " Slide in gate: " + ("Yes" if self.slide_in_gate == 1 else "No") \
                   + " Standby: " + ("On" if self.standby == 1 else "Off") \
                   + " Active lamp: " + ("L2" if self.active_lamp == 1 else "L1") \
                   + " Standby: " + ("On" if self.standby == 1 else "Off") \
                   + " Power frequency: " + ("60Hz" if self.power_frequency == 1 else "50Hz") \
                   + " Autofocus: " + ("On" if self.auto_focus == 1 else "Off") \
                   + " Autozero: " + ("On" if self.auto_zero == 1 else "Off") \
                   + " Low lamp mode: " + ("On" if self.low_lamp == 1 else "Off") \
                   + " High light: " + ("On" if self.high_light == 1 else "Off")

        return det


class EktaproCommand:
    """
    Represents a single low level 3 byte command that is sent to an Ektapro slide projector
    by the user software.
     
    Permits easy construction of the 3 byte commands and decoding of 3 byte hex sequences to into
    a human readable string (for example for debugging).  
    """

    def __init__(self, *args):
        if len(args) == 1:
            self.id = args[0]
            self.initialized = False
        elif len(args) == 3:
            self.id = args[0] // 8
            self.mode = args[0] % 8 // 2
            self.arg1 = args[1]
            self.arg2 = args[2]
            self.initialized = True
        else:
            raise Exception("Argument count invalid")

    def to_data(self):
        if not self.initialized:
            raise Exception("Command not initialized")
        return bytes([int(self.id * 8 + self.mode * 2 + 1), int(self.arg1), int(self.arg2)])

    # Command  construction
    # Parameter mode

    def construct_parameter_command(self, command, param):
        self.mode = 0
        self.arg1 = command * 16 + param // 128 * 2
        self.arg2 = param % 128 * 2
        self.initialized = True

    def param_random_access(self, slide):
        self.construct_parameter_command(0, slide)
        return self

    def param_set_brightness(self, brightness):
        self.construct_parameter_command(1, brightness)
        return self

    def param_group_address(self, group):
        self.construct_parameter_command(3, group)
        return self

    def param_fade_up(self, t):
        self.construct_parameter_command(6, t + 128)
        return self

    def param_fade_down(self, t):
        self.construct_parameter_command(6, t)
        return self

    def param_set_lower_limit_fading(self, t):
        self.construct_parameter_command(7, t)
        return self

    def param_set_upper_limit_fading(self, t):
        self.construct_parameter_command(8, t)
        return self

    # Set/Reset mode

    def construct_set_reset_command(self, option, on):
        self.mode = 1
        self.arg1 = option * 4 + (2 if on is True else 0)
        self.arg2 = 0
        self.initialized = True
        return self

    def set_auto_focus(self, on):
        self.construct_set_reset_command(0, on)
        return self

    def set_highlight(self, on):
        self.construct_set_reset_command(1, on)
        return self

    def set_auto_shutter(self, on):
        self.construct_set_reset_command(3, on)
        return self

    def set_block_keys(self, on):
        self.construct_set_reset_command(5, on)
        return self

    def set_block_focus(self, on):
        self.construct_set_reset_command(2, on)
        return self

    def set_standby(self, on):
        self.construct_set_reset_command(7, on)
        return self

    # Direct mode

    def construct_direct_mode_command(self, command):
        self.mode = 2
        self.arg1 = command * 4
        self.arg2 = 0
        self.initialized = True

    def direct_slide_forward(self):
        self.construct_direct_mode_command(0)
        return self

    def direct_slide_backward(self):
        self.construct_direct_mode_command(1)
        return self

    def direct_focus_forward(self):
        self.construct_direct_mode_command(2)
        return self

    def direct_focus_backward(self):
        self.construct_direct_mode_command(3)
        return self

    def direct_focus_stop(self):
        self.construct_direct_mode_command(4)
        return self

    def direct_shutter_open(self):
        self.construct_direct_mode_command(7)
        return self

    def direct_shutter_close(self):
        self.construct_direct_mode_command(8)
        return self

    def direct_reset_system(self):
        self.construct_direct_mode_command(11)
        return self

    def direct_switch_lamp(self):
        self.construct_direct_mode_command(12)
        return self

    def direct_clear_error_flag(self):
        self.construct_direct_mode_command(13)
        return self

    def direct_stop_fading(self):
        self.construct_direct_mode_command(15)
        return self

    # Status request mode

    def construct_status_request_command(self, request):
        self.mode = 3
        self.arg1 = request * 16
        self.arg2 = 0
        self.initialized = True

    def status_get_tray_position(self):
        self.construct_status_request_command(10)
        return self

    def status_get_keys(self):
        self.construct_status_request_command(11)
        return self

    def status_system_status(self):
        self.construct_status_request_command(12)
        return self

    def status_system_return(self):
        self.construct_status_request_command(13)
        return self

    #
    # String  conversion
    #

    def __str__(self):
        command_string = {
            0: "Param  Mode - " + self.parameter_mode_to_string(),
            1: "SetRes Mode - " + self.set_reset_mode_to_string(),
            2: "Direct Mode - " + self.direct_mode_to_string(),
            3: "Status Mode - " + self.status_request_to_string()
        }

        return "P:" + str(self.id) + " - " \
               + command_string.get(self.mode, "Unknown Mode")

    def parameter_mode_to_string(self):
        up_down = {
            0: "Down",
            1: "Up"
        }

        parameter_settings = {
            0: "Random Access - Slide " + str(self.arg1 % 16 * 64 + self.arg2 // 2),
            1: "SetBrightness - " + str(self.arg1 % 16 * 64 + self.arg2 / 2),
            3: "Group Address - " + str(self.arg2 // 2),
            6: "Fade up/down - " + up_down.get(self.arg1 % 16 // 2, "?") + " - "
               + str(self.arg2 / 2),
            7: "SetLowerLimit for Fading - " + str(self.arg1 % 16 * 64 + self.arg2 // 2),
            8: "SetUpperLimit for Fading - " + str(self.arg1 % 16 * 64 + self.arg2 // 2)
        }

        return parameter_settings.get(self.arg1 // 16, "Unknown parameter")

    def set_reset_mode_to_string(self):
        set_reset_string = {
            0: "AutoFocus on/off - ",
            1: "Highlight on/off - ",
            3: "AutoShutter on/off - ",
            5: "BlockKeys on/off - ",
            2: "BlockFocus on/off - ",
            7: "Standby on/off - "
        }

        on_off = {
            0: "Reset (off)",
            2: "Set (on)"
        }

        return set_reset_string.get(self.arg1 // 4, "Unknown command") + on_off.get(self.arg1 % 4, "?")

    def direct_mode_to_string(self):
        direct_mode_string = {
            0: "Slide forward",
            1: "Slide backward",
            2: "Focus forward",
            3: "Focus backward",
            4: "Focus stop",
            7: "Shutter open",
            8: "Shutter close",
            11: "Reset system",
            12: "Switch lamp",
            13: "Clear error flags",
            15: "Stop fading"
        }

        if self.arg1 // 128 == 1:
            return "Direct User Mode"

        return direct_mode_string.get(self.arg1 // 4, "Unknown command")

    def status_request_to_string(self):
        status_requests = {
            10: "GetTray position",
            11: "GetKeys",
            12: "System status",
            13: "System return"
        }
        return status_requests.get(self.arg1 // 16, "Unknown request")


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

    for l in [1, 2, 3, 4, 5, 6, 7, 8]:
        tpt.next(20, 20)
        log.info('sync :' + str(tpt.status_get_tray_position()) + "   in gate: " + str(tpt.slide_in_gate))




