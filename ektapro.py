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
   33:40.342-ektapro-MainThread-DEBUG
 Model: Kodak Ektapro model: 5000 Id: 0 Version: 2.31
 Projector Busy: 1
 At zero: 0
 Slide lift motor error: 0
 Tray transport motor error: 1
 Command Error: 0
 Buffer overflow: 1
 Overrun error: 0
 Framing error: 0
 Tray size: 80
 Active lamp: L1
 Standby: Off
 Flag 1: 0
 Flag 2: 0
 Power frequency: 50Hz
 Autofocus: Off
 Autozero: Off
 Low lamp mode: Off



   
"""
from enumerate_serial import *
import logging
log = logging.getLogger(__name__)


class EktaproDevice:
    # Encapsulates the logic to control a Ektapro slide projector.
    def __init__(self):
        self.is_busy = True
        self.max_brightness = 100
        self.brightness = 0
        self.slide = 0
        self.tray_size = 80 #this allows dummy scanning
        self.max_display_tray = 140
        self.info = None
        self.id = 0
        self.version = None
        self.type = 0
        self.serial_device = None
        self.connected = 0
        #initalise internal vars
        self.get_system_return()
        #self.pre_timeout = 2
        #self.post_timeout = 2

    def open_port(self, port):
        self.close()
        log.info("Checking port: " + port)
        try:
            s = serial.serial_for_url(port, 9600, timeout=.1, writeTimeout=.1)
            try:
                fcntl.flock(s, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError:
                log.info("Can not immediately write-lock the file ($!), blocking ...")
            else:
                s.write(EktaproCommand(0).statusSystemReturn().toData())
                self.info = s.read(5)
                info = self.info
                if info == None or len(info) == 0 \
                        or not (info[0] % 8 == 6) \
                        or not (info[1] / 16 == 13) \
                        or not (info[1] % 2 == 0):
                    logging.info("Not a Ektapro device")
                else:
                    self.serialDevice = s
                    self.port = port
                    self.connected = 1
                    return 1
        except serial.SerialException:
            pass
        except IOError:
            logging.error("Not a Ektapro device")
        return 0

    def open(self, port):
        if (port is None):
            ports = enumerate()
            for port in ports:
                if (self.open_port(port)):
                    break
        else:
            self.open_port(port)
        self.get_status()

    def reset(self):
        self.setStandby(False)
        self.setAutoFocus(False)
        self.gotoSlide(1)
        self.setBrightness(0)
        self.standby = False

    def close(self):
        if (self.connected):
            try:
                self.serialDevice.close()
            except:
                pass
        self.port = "Not Connected"
        self.connected = 0
        self.get_status()

    def toggleStandby(self):
        self.standby = not self.standby
        self.setStandby(self.standby)

    def __str__(self):
        self.get_model()

    def get_model(self):
        modelStrings = {
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
               + modelStrings.get(self.type, "Unknown") \
               + " Id: " + str(self.id) \
               + " Version: " + str(self.version)

    def get_version(self):
        return self.version

    def setStandby(self, on):
        self.comms(EktaproCommand(self.id).setStandby(on))

    def setAutoFocus(self, on):
        self.comms(EktaproCommand(self.id).setAutoFocus(on))

    def setBrightness(self, brightness):
        self.comms(EktaproCommand(self.id).paramSetBrightness(brightness * 10))
        self.brightness = brightness

    def reset(self):
        self.comms(EktaproCommand(self.id).directResetSystem())

    def clear_error_flag(self):
        self.comms(EktaproCommand(self.id).directClearErrorFlag())

    def select(self, slide):
        self.comms(EktaproCommand(self.id).paramRandomAccess(slide), pre_timeout=0, post_timeout=10)
        self.slide = slide

    def next(self, pre_timeout=0, post_timeout=0):
        self.comms(EktaproCommand(self.id).directSlideForward(), pre_timeout=pre_timeout, post_timeout=post_timeout)
        self.slide = self.slide + 1
        if self.slide > self.tray_size:
            self.slide = 0  #? 1

    def prev(self, pre_timeout=0, post_timeout=1.5):
        self.comms(EktaproCommand(self.id).directSlideBackward(), pre_timeout=pre_timeout, post_timeout=post_timeout)
        self.slide = self.slide - 1
        if self.slide == -1:
            self.slide = self.tray_size

    def sync(self):
        s = self.comms(EktaproCommand(self.id).statusGetTrayPosition(), read_bytes=3)
        if (self.connected):
            if (len(s) != 3) \
                    or not (ord(s[0]) % 8 == 6) \
                    or not (ord(s[1]) // 16 == 10):
                log.error("get_status invalid response")  #could raise error here?
            else:
                self.slide = int(str(ord(s[2])))

    def get_status_busy(self):
        #log.error ( str(self.is_busy) )
        return self.is_busy

    def get_status(self, busy=False, debug=True):
        ret = self.get_system_status(debug=debug)
        if ( self.slide_lift_motor_error \
                     or self.tray_transport_motor_error \
                     or self.command_error \
                     or self.overrun_error \
                     or self.buffer_overflow_error \
                     or self.framing_error):
            log.error("get_status error detected")  #could raise error here?
            log.debug(self.get_details())
            self.clear_error_flag()
            ret = self.get_system_status()
            log.debug(self.get_details())
        if (busy):
            return ret
        else:
            self.get_system_return()
            if (self.connected):
                log.debug(self.get_details())

    def get_system_return(self, debug=True):
        if (self.connected):
            self.info = self.comms(EktaproCommand(self.id).statusSystemReturn(), read_bytes=5, debug=debug)
        else:
            self.info = ""
        if (self.connected and (len(self.info) == 5) ):
            info = self.info
            #self.id = info[0] / 16 - do not change based on returned values

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
        s = self.comms(EktaproCommand(self.id).statusSystemStatus(), read_bytes=3, debug=debug)
        if (self.connected and (len(s) == 3) ):
            if not (s[0] % 8 == 6) or not (s[2] % 4 == 3):
                #or not (ord(s[1]) % 64 == 3) \ #should be 11XX XXXX don't check for now
                log.error("get_status invalid response")
                raise IOError("Invalid response")
            #self.projector_id = ord(s[0]) / 8 - do not change based on returned values 
            self.unknown_flag1 = (s[1] & 16 ) // 16  #this is undocumented - seems to be on after reset process
            self.unknown_flag2 = (s[1] & 32 ) // 32
            self.lamp1_status = (s[1] & 8) // 8
            self.lamp2_status = (s[1] & 4) // 4
            self.status = (s[1] & 2) // 2
            self.at_zero_position = s[1] & 1
            self.slide_lift_motor_error = (s[2] & 128) // 128
            self.tray_transport_motor_error = (s[2] & 64) // 64
            self.command_error = (s[2] & 32) // 32
            self.overrun_error = (s[2] & 16) // 16
            self.buffer_overflow_error = (s[2] & 8) // 8
            self.framing_error = (s[2] & 4) // 4
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

        if (self.status == 1):
            self.is_busy = True
        else:
            self.is_busy = False
        return self.status

    def comms(self, command, read_bytes=0, pre_timeout=0, post_timeout=0, debug=True):
        rec = ""
        if (debug):
            log.debug("Send: " + str(command) + " hex: " + repr(command.toData()) + " pre/post timeouts: " + str(
                pre_timeout) + " - " + str(post_timeout))
        self.busy(pre_timeout, desc="pre timeout ")
        if (self.connected):
            try:  #might be disconnected or port removed or....
                self.serialDevice.write(command.toData())
            except:
                raise
        else:
            log.debug("ignore - device not connected")
        if (self.connected and read_bytes):
            try:
                rec = self.serialDevice.read(read_bytes)
            except:
                raise
            if (debug):
                log.debug("Revd: " + repr(rec) + " len: " + str(len(rec)))
        self.busy(post_timeout, desc="post timeout ")
        return rec

    def busy(self, timeout, desc=""):
        if ( self.connected == 0 or timeout == 0):
            return
        if (not self.get_status(busy=True)):
            return
        busy = True
        ts = time.time()
        if (timeout > 0 ):
            while busy:
                busy = self.get_status(busy=1, debug=False)
                if (time.time() - ts > timeout):
                    log.error("Busy " + desc + " timeout: " + str(timeout))
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
            self.initalized = False
        elif len(args) == 3:
            self.id = args[0] // 8
            self.mode = args[0] % 8 // 2
            self.arg1 = args[1]
            self.arg2 = args[2]
            self.initalized = True
        else:
            raise Exception("Argument count invalid")

    def toData(self):
        if not self.initalized:
            raise Exception("Command not initialized")
        return bytes([int(self.id * 8 + self.mode * 2 + 1), int(self.arg1), int(self.arg2)])

    # Command  construction
    # Parameter mode

    def constructParameterCommand(self, command, param):
        self.mode = 0
        self.arg1 = command * 16 + param // 128 * 2
        self.arg2 = param % 128 * 2
        self.initalized = True

    def paramRandomAccess(self, slide):
        self.constructParameterCommand(0, slide)
        return self

    def paramSetBrightness(self, brightness):
        self.constructParameterCommand(1, brightness)
        return self

    def paramGroupAddress(self, group):
        self.constructParameterCommand(3, group)
        return self

    def paramFadeUp(self, time):
        self.constructParameterCommand(6, time + 128)
        return self

    def paramFadeDown(self, time):
        self.constructParameterCommand(6, time)
        return self

    def paramSetLowerLimitFading(self, time):
        self.constructParameterCommand(7, time)
        return self

    def paramSetUpperLimitFading(self, time):
        self.constructParameterCommand(8, time)
        return self

    # Set/Reset mode

    def constructSetResetCommand(self, option, on):
        self.mode = 1
        self.arg1 = option * 4 + (2 if on == True else 0)
        self.arg2 = 0
        self.initalized = True
        return self

    def setAutoFocus(self, on):
        self.constructSetResetCommand(0, on)
        return self

    def setHighlight(self, on):
        self.constructSetResetCommand(1, on)
        return self

    def setAutoShutter(self, on):
        self.constructSetResetCommand(3, on)
        return self

    def setBlockKeys(self, on):
        self.constructSetResetCommand(5, on)
        return self

    def setBlockFocus(self, on):
        self.constructSetResetCommand(2, on)
        return self

    def setStandby(self, on):
        self.constructSetResetCommand(7, on)
        return self

    # Direct mode

    def constructDirectModeCommand(self, command):
        self.mode = 2
        self.arg1 = command * 4
        self.arg2 = 0
        self.initalized = True

    def directSlideForward(self):
        self.constructDirectModeCommand(0)
        return self

    def directSlideBackward(self):
        self.constructDirectModeCommand(1)
        return self

    def directFocusForward(self):
        self.constructDirectModeCommand(2)
        return self

    def directFocusBackward(self):
        self.constructDirectModeCommand(3)
        return self

    def directFocusStop(self):
        self.constructDirectModeCommand(4)
        return self

    def directShutterOpen(self):
        self.constructDirectModeCommand(7)
        return self

    def directShutterClose(self):
        self.constructDirectModeCommand(8)
        return self

    def directResetSystem(self):
        self.constructDirectModeCommand(11)
        return self

    def directSwitchLamp(self):
        self.constructDirectModeCommand(12)
        return self

    def directClearErrorFlag(self):
        self.constructDirectModeCommand(13)
        return self

    def directStopFading(self):
        self.constructDirectModeCommand(15)
        return self

    # Status request mode

    def constructStatusRequestCommand(self, request):
        self.mode = 3
        self.arg1 = request * 16
        self.arg2 = 0
        self.initalized = True

    def statusGetTrayPosition(self):
        self.constructStatusRequestCommand(10)
        return self

    def statusGetKeys(self):
        self.constructStatusRequestCommand(11)
        return self

    def statusSystemStatus(self):
        self.constructStatusRequestCommand(12)
        return self

    def statusSystemReturn(self):
        self.constructStatusRequestCommand(13)
        return self

    #
    # String  conversionc
    #

    def __str__(self):
        commandstring = {
            0: "Parameter Mode - " + self.parameterModeToString(),
            1: "Set/Reset Mode - " + self.setResetModeToString(),
            2: "Direct Mode - " + self.directModeToString(),
            3: "Status Request Mode - " + self.statusRequestToString()
        }

        return "Projector " + str(self.id) + " - " \
               + commandstring.get(self.mode, "Unknown Mode")

    def parameterModeToString(self):
        upDown = {
            0: "Down",
            1: "Up"
        }

        parametersettings = {
            0: "Random Access - Slide " + str(self.arg1 % 16 * 64 + self.arg2 // 2),
            1: "SetBrightness - " + str(self.arg1 % 16 * 64 + self.arg2 / 2),
            3: "Group Address - " + str(self.arg2 // 2),
            6: "Fade up/down - " + upDown.get(self.arg1 % 16 // 2, "?") + " - "
               + str(self.arg2 / 2),
            7: "SetLowerLimit for Fading - " + str(self.arg1 % 16 * 64 + self.arg2 // 2),
            8: "SetUpperLimit for Fading - " + str(self.arg1 % 16 * 64 + self.arg2 // 2)
        }

        return parametersettings.get(self.arg1 // 16, "Unknown parameter")

    def setResetModeToString(self):
        setresetstring = {
            0: "AutoFocus on/off - ",
            1: "Highlight on/off - ",
            3: "AutoShutter on/off - ",
            5: "BlockKeys on/off - ",
            2: "BlockFocus on/off - ",
            7: "Standby on/off - "
        }

        onOff = {
            0: "Reset (off)",
            2: "Set (on)"
        }

        return setresetstring.get(self.arg1 // 4, "Unknown command") \
               + onOff.get(self.arg1 % 4, "?")

    def directModeToString(self):
        directModeString = {
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

        return directModeString.get(self.arg1 // 4, "Unknown command")

    def statusRequestToString(self):
        statusRequests = {
            10: "GetTray position",
            11: "GetKeys",
            12: "System status",
            13: "System return"
        }
        return statusRequests.get(self.arg1 // 16, "Unknown request")


if __name__ == "__main__":
    import time, logging

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')

    tpt = EktaproDevice()
    tpt.open(None)
    if (tpt.connected):
        log.info("EktaproDevice device connected")
    else:
        log.error("EktaproDevice device not connected")
    try:
        log.debug(tpt.get_version())
    except:
        log.warn("EktaproDevice not reporting version")
    try:
        tpt.reset()
    except:
        log.warn("EktaproDevice not resetting")
    try:
        log.debug(tpt.get_details())
    except:
        log.warn("EktaproDevice not resetting")

    for l in [1, 2, 3, 4, 5, 6]:
        try:
            tpt.next(20, 20)
            tpt.prev(20, 20)

        except:
            pass


