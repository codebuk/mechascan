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


class EktaproFailed(Exception):
    pass


class EktaproDevice:
    # Encapsulates the logic to control a Ektapro slide projector.
    def __init__(self):
        self.is_busy = True
        self.max_brightness = 100
        self.brightness = 0
        self.slide = 0
        self.tray_size = 80  # this allows dummy scanning
        self.max_display_tray = 140
        self.info = bytearray()
        self.id = 0
        self.version = None
        self.type = 0
        self.serial_device = None
        self.port = None
        self.connected = 0
        self.standby = 0
        self.auto_focus = None
        self.auto_zero = None
        self.low_lamp = None
        self.active_lamp = None
        self.high_light = None
        self.unknown_flag1 = None
        self.unknown_flag2 = None
        self.lamp1_status = None
        self.lamp2_status = None
        self.power_frequency = None
        self.status = None
        self.at_zero_position = None
        self.slide_lift_motor_error = None
        self.tray_transport_motor_error = None
        self.command_error = None
        self.overrun_error = None
        self.buffer_overflow_error = None
        self.framing_error = None

        # initialise internal vars
        self.get_system_return()

    def open_port(self, comm_port):
        self.close()
        log.info("Checking port: " + comm_port)
        try:
            self.serial_device = serial.serial_for_url(comm_port, 9600, timeout=.1, writeTimeout=.1)
            try:
                fcntl.flock(self.serial_device, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                log.info("Can not immediately write-lock file: " + comm_port)
            else:
                self.serial_device.write(EktaproCommand(0).status_system_return().to_data())
                self.info = self.serial_device.read(5)
                info = self.info
                if info is None or len(info) == 0 \
                        or not (info[0] % 8 == 6) \
                        or not (info[1] / 16 == 13) \
                        or not (info[1] % 2 == 0):
                    logging.info("Not a Ektapro device")
                    self.serial_device = None
                else:
                    self.port = comm_port
                    self.connected = 1
                    return 1
        except serial.SerialException:
            pass
        except IOError:
            logging.error("Not a Ektapro device")
        return 0

    def open(self, comm_port):
        if comm_port is None:
            ports = enumerate()
            for comm_port in ports:
                if self.open_port(comm_port):
                    break
        else:
            self.open_port(comm_port)
        self.get_status()

    def close(self):
        if self.connected:
            self.serial_device.close()
        self.port = "Not Connected"
        self.connected = 0
        self.get_status()

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
        self.comms(EktaproCommand(self.id).direct_reset_system())

    def clear_error_flag(self):
        self.comms(EktaproCommand(self.id).direct_clear_error_flag())

    def select(self, slide):
        self.comms(EktaproCommand(self.id).param_random_access(slide), pre_timeout=0, post_timeout=10)
        self.slide = slide

    def next(self, pre_timeout=0, post_timeout=0):
        self.comms(EktaproCommand(self.id).direct_slide_forward(), pre_timeout=pre_timeout, post_timeout=post_timeout)
        self.slide = + 1
        if self.slide > self.tray_size:
            self.slide = 0  # ? 1

    def prev(self, pre_timeout=0, post_timeout=1.5):
        self.comms(EktaproCommand(self.id).direct_slide_backward(), pre_timeout=pre_timeout, post_timeout=post_timeout)
        self.slide -= 1
        if self.slide == -1:
            self.slide = self.tray_size

    def sync(self):
        reply = self.comms(EktaproCommand(self.id).status_get_tray_position(), read_bytes=3)
        if self.connected:
            if (len(reply) != 3) \
                    or not (reply[0] % 8 == 6) \
                    or not (reply[1] // 16 == 10):
                log.error("get_status invalid response")  # could raise error here?
            else:
                self.slide = int(str(reply[2]))

    def get_status_busy(self):
        # log.error ( str(self.is_busy) )
        return self.is_busy

    def get_status(self, busy=False, debug=True):
        self.get_system_status(debug=debug)
        msg = ""
        if self.slide_lift_motor_error:
            msg = "slide_lift_motor_error\n"
        if self.tray_transport_motor_error:
            msg = "tray_transport_motor_error\n"
        if self.command_error:
            msg = "command_error\n"
        if self.overrun_error:
            msg = "overrun_error\n"
        if self.buffer_overflow_error:
            msg = "buffer_overflow_error\n"
        if self.framing_error:
            msg = "framing_error\n"
        if len(msg):
            log.error("Get_status error detected: " + msg)  # could raise error here?
            log.debug(self.get_details())
            self.clear_error_flag()
            self.get_system_status()
            log.debug(self.get_details())
            raise EktaproFailed(msg)
        if busy:
            return
        else:
            self.get_system_return()
            if self.connected:
                log.debug(self.get_details())

    def get_system_return(self, debug=True):
        if self.connected:
            self.info = self.comms(EktaproCommand(self.id).status_system_return(), read_bytes=5, debug=debug)
        else:
            self.info = bytearray()
        # noinspection PyTypeChecker
        if self.connected and len(self.info) == 5:
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

    def get_system_status(self, debug=True):
        reply = self.comms(EktaproCommand(self.id).status_system_status(), read_bytes=3, debug=debug)
        if self.connected and (len(reply) == 3):
            if not (reply[0] % 8 == 6) or not (reply[2] % 4 == 3):
                # or not (ord(s[1]) % 64 == 3) \ #should be 11XX XXXX don't check for now
                log.error("get_status invalid response")
                raise IOError("Invalid response")
            # self.projector_id = ord(s[0]) / 8 - do not change based on returned values
            self.unknown_flag1 = (reply[1] & 16) // 16  # this is undocumented - seems to be on after reset process
            self.unknown_flag2 = (reply[1] & 32) // 32
            self.lamp1_status = (reply[1] & 8) // 8
            self.lamp2_status = (reply[1] & 4) // 4
            self.status = (reply[1] & 2) // 2
            self.at_zero_position = reply[1] & 1
            self.slide_lift_motor_error = (reply[2] & 128) // 128
            self.tray_transport_motor_error = (reply[2] & 64) // 64
            self.command_error = (reply[2] & 32) // 32
            self.overrun_error = (reply[2] & 16) // 16
            self.buffer_overflow_error = (reply[2] & 8) // 8
            self.framing_error = (reply[2] & 4) // 4
        else:
            self.unknown_flag1 = None
            self.unknown_flag2 = None
            self.lamp1_status = None
            self.lamp2_status = None
            self.status = None
            self.at_zero_position = None
            self.slide_lift_motor_error = None
            self.tray_transport_motor_error = None
            self.command_error = None
            self.overrun_error = None
            self.buffer_overflow_error = None
            self.framing_error = None

        if self.status == 1:
            self.is_busy = True
        else:
            self.is_busy = False
        return self.status

    def comms(self, command, read_bytes=0, pre_timeout=0.0, post_timeout=0.0, debug=True):
        rec = bytearray()
        if debug:
            log.debug("Send: " + str(command) + " hex: " + repr(command.to_data()) + " pre/post timeouts: " + str(
                pre_timeout) + " - " + str(post_timeout))
        self.busy(pre_timeout, desc="pre timeout ")
        if self.connected:
            try:  # might be disconnected or port removed or....
                self.serial_device.write(command.to_data())
            except:
                raise
        else:
            log.debug("ignore - device not connected")
        if self.connected and read_bytes:
            try:
                rec = self.serial_device.read(read_bytes)
            except:
                raise
            if debug:
                log.debug("Received: " + repr(rec) + " len: " + str(len(rec)))
        self.busy(post_timeout, desc="post timeout ")
        return rec

    def busy(self, to, desc=""):
        if self.connected == 0 or to == 0:
            return
        if not self.get_status(busy=True):
            return
        busy = True
        ts = time.time()
        if to > 0:
            while busy:
                self.get_status(busy=True, debug=False)
                if time.time() - ts > to:
                    log.error("Busy " + desc + " timeout: " + str(to))
                    raise IOError("Busy timeout")
            log.debug(desc + "busy for: " + str(time.time() - ts))

    def get_details(self):
        return "\n Model: " + self.get_model() \
               + "\n Projector Busy: " + str(self.status) \
               + "\n At zero: " + str(self.at_zero_position) \
               + "\n Slide lift motor error: " + str(self.slide_lift_motor_error) \
               + "\n Tray transport motor error: " + str(self.tray_transport_motor_error) \
               + "\n Command Error: " + str(self.command_error) \
               + "\n Buffer overflow: " + str(self.buffer_overflow_error) \
               + "\n Overrun error: " + str(self.overrun_error) \
               + "\n Framing error: " + str(self.framing_error) \
               + "\n Tray size: " + str(self.tray_size) \
               + "\n Active lamp: " + ("L2" if self.active_lamp == 1 else "L1") \
               + "\n Standby: " + ("On" if self.standby == 1 else "Off") \
               + "\n Flag 1: " + str(self.unknown_flag1) \
               + "\n Flag 2: " + str(self.unknown_flag2) \
               + "\n Power frequency: " + ("60Hz" if self.power_frequency == 1 else "50Hz") \
               + "\n Autofocus: " + ("On" if self.auto_focus == 1 else "Off") \
               + "\n Autozero: " + ("On" if self.auto_zero == 1 else "Off") \
               + "\n Low lamp mode: " + ("On" if self.low_lamp == 1 else "Off") \
               + "\n High light: " + ("On" if self.high_light == 1 else "Off")


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
            0: "Parameter Mode - " + self.parameter_mode_to_string(),
            1: "Set/Reset Mode - " + self.set_reset_mode_to_string(),
            2: "Direct Mode - " + self.direct_mode_to_string(),
            3: "Status Request Mode - " + self.status_request_to_string()
        }

        return "Projector " + str(self.id) + " - " \
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

    for l in [1, 2, 3, 4, 5, 6]:
        tpt.next(20, 20)
        tpt.prev(20, 20)

