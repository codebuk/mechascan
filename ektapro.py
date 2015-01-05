#!/usr/bin/env python
"""

   Ektapro v1.0
   

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
   
   This program serves as a controller for the ektapro slide projector
   devices. One projector per serial port is supported.
"""
import serial, pprint, time, logging, fcntl
try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None

log = logging.getLogger(__name__)

class EktaproDevice:

    #Encapsulates the logic to control a single Ektapro slide projector.
    def __init__(self):
        # own temporary values
        self.maxBrightness = 100
        self.brightness = 0
        self.slide = 0
        self.maxDisplayTray = 140
        self.projektorID = 0
        self.info = None
        #self.pre_timeout = 2
        #self.post_timeout = 2

    def open_port(self, port):
        if (port is None):
            for port, desc, hwid in sorted(comports(), reverse=True):  #usb is first!
                log.info("Trying port: " + port + " --- " + desc + " --- " + hwid)
                try:
                    s = serial.serial_for_url(port, 9600, timeout=.5, writeTimeout=.5)
                    try:
                        fcntl.flock(s, fcntl.LOCK_EX | fcntl.LOCK_NB )
                        #fcntl.flock(open('/tmp/locktest', 'r'), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except IOError:
                        log.info("Can't immediately write-lock the file ($!), blocking ...")
                    else:
                        log.debug("No error")
                        s.write(EktaproCommand(0).statusSystemReturn().toData())
                        self.info = s.read(5)
                        info = self.info
                        if info == None or len(info) == 0 \
                            or not (ord(info[0]) % 8 == 6) \
                            or not (ord(info[1]) / 16 == 13) \
                            or not (ord(info[1]) % 2 == 0):
                            logging.info("Not a Ektapro device")
                        else:
                            self.serialDevice = s
                        return 1
                except serial.SerialException:
                    pass
                except IOError:
                    logging.error("Not a Ektapro device")
            return 0        
        #else:
            #replace with insert into has and use above 
##            log.info('Open port: ' + port)
##            try:
##                s = serial.serial_for_url(port, 9600, timeout=1, writeTimeout=.01)
##                s.write(EktaproCommand(0).statusSystemReturn().toData())
##                self.info = s.read(5)
##                info = self.info
##                if info == None or len(info) == 0 \
##                    or not (ord(info[0]) % 8 == 6) \
##                    or not (ord(info[1]) / 16 == 13) \
##                    or not (ord(info[1]) % 2 == 0):
##                    logging.error("Not a Ektapro device")
##                else:
##                    self.serialDevice = s
##                    return 1
##            except serial.SerialException:
##                pass
##            except IOError:
##                logging.error("Not a Ektapro device")
        return 0
      
    def open(self, port):
        if (self.open_port(port)):
            self.serialDevice.write(EktaproCommand(0).statusSystemReturn().toData())
            self.info = self.serialDevice.read(5)
            # from info string delivered by device
            info = self.info
            self.projektorID = ord(info[0]) / 16
            self.projektorType = ord(info[2]) / 16
            self.projektorVersion = str(ord(info[2]) % 16) + "." \
                + str(ord(info[3]) / 16) \
                + str(ord(info[3]) % 16)
            self.powerFrequency = (ord(info[4]) & 128) / 128
            self.autoFocus = (ord(info[4]) & 64) / 64
            self.autoZero = (ord(info[4]) & 32) / 32 
            self.lowLamp = (ord(info[4]) & 16) / 16
            self.traySize = 140 if ord(info[4]) & 8 == 1 else 80
            self.activeLamp = (ord(info[4]) & 4) / 4
            self.standby = (ord(info[4]) & 2) /2
            self.highLight = ord(info[4]) & 1 
     
    def reset(self):
        self.setStandby(False)
        self.gotoSlide(1)
        self.setBrightness(0)
        self.standby = False

    def close(self):
        self.reset()
        self.serialDevice.close()
       
    def toggleStandby(self):
        self.standby = not self.standby
        self.setStandby(self.standby)
        
    def __str__(self):
        modelStrings = {
            7: "4010 / 7000",
            4: "4020",
            5: "5000",
            6: "5020",
            8: "7010 / 7020",
            9: "9000",
            10: "9010 / 9020"
        }

        return "Kodak Ektapro " \
               + modelStrings.get(self.projektorType, "Unknown") \
               + " id=" + unicode(self.projektorID) \
               + " Version " + unicode(self.projektorVersion)

    def get_details(self):
        return "Power frequency: " + ("60Hz" if self.powerFrequency == 1 else "50Hz") \
               + "\n Autofocus: " + ("On" if self.autoFocus == 1 else "Off") \
               + "\n Autozero: " + ("On" if self.autoZero == 1 else "Off") \
               + "\n Low lamp mode: " + ("On" if self.lowLamp == 1 else "Off") \
               + "\n Tray size: " + str(self.traySize) \
               + "\n Active lamp: " + ("L2" if self.activeLamp == 1 else "L1") \
               + "\n Standby: " + ("On" if self.standby == 1 else "Off") \
               + "\n High light: " + ("On" if self.highLight == 1 else "Off")\
               + "\n Flag 1: " + str(self.unknown_flag1 ) \
               + "\n Flag 2: "  + str(self.unknown_flag2 ) \
               + "\n Busy: " + str(self.projector_status) \
               + "\n At zero: " + str(self.at_zero_position) \
               + "\n Slide lift motor error: " + str(self.slide_lift_motor_error) \
               + "\n Tray transport motor error: " + str(self.tray_transport_motor_error) \
               + "\n Command Error: " + str(self.command_error ) \
               + "\n Over run error: " + str(self.overrun_error) \
               + "\n buffer_overflow_error" + str( self.buffer_overflow_error) \
               + "\n overrun_error" + str(self.overrun_error) \
               + "\n self.framing_error" + str(self.framing_error) 

    def setStandby(self, on):
        c = EktaproCommand(self.projektorID).setStandby(on)
        log.info(str(c))
        self.serialDevice.write(c.toData())

    def setBrightness(self, brightness):
        c = EktaproCommand(self.projektorID).paramSetBrightness(brightness * 10)
        log.info(str(c))
        self.serialDevice.write(c.toData())
        self.brightness = brightness

    def reset(self):
        c = EktaproCommand(self.projektorID).directResetSystem()
        log.info(str(c))
        try: #might be disconnected
            self.serialDevice.write(c.toData())
        except IOError as e:
            log.debug ("I/O error: "  + str(e.errno))
        except ValueError:
            print "Could not convert data to an integer."      
        except serial.SerialException:
            log.info("reset port serial error")
            
    def busy(self, timeout):
        busy = True
        ts = time.time()
        if (timeout > 0 ):
            while busy:
                status = self.get_status()
                busy = (self.projector_status == 1)
                if (time.time () - ts > timeout):
                    log.error("Busy timeout")
                    raise IOError, "Busy timeout"
            log.debug ( "Busy for: " + str(time.time () - ts))

    def select(self, slide):
        c = EktaproCommand(self.projektorID).paramRandomAccess(slide)
        log.info(str(c))
        self.busy(1)
        self.serialDevice.write(c.toData())
        self.slide = slide

    def next(self, pre_timeout , post_timeout):
        c = EktaproCommand(self.projektorID).directSlideForward()
        log.info(str(c))
        self.busy(pre_timeout)
        self.serialDevice.write(c.toData())
        self.slide = self.slide + 1
        if self.slide > self.traySize:
            self.slide = 0 #? 1
        self.busy(post_timeout)

    def prev(self):
        c = EktaproCommand(self.projektorID).directSlideBackward()
        log.info(str(c))
        self.busy(1.5)
        self.serialDevice.write(c.toData())
        self.slide = self.slide - 1
        if self.slide == -1:
            self.slide = self.traySize

    def get_status(self):
        c = EktaproCommand(self.projektorID).statusSystemStatus()
        self.serialDevice.write(c.toData())
        s = self.serialDevice.read(3)
        if not (ord(s[0]) % 8 == 6) or not (ord(s[2]) % 4 == 3):
            #or not (ord(s[1]) % 64 == 3) \ #should be 11XX XXXX don't check for now
            log.error ("get_status invalid response. Sent: " + c.toData() + " Revd: " + repr(s))  
            raise IOError, "Invalid response"
        self.projector_id = ord(s[0]) / 8
        #this is undocumented - seems to be on after reset processs
        self.unknown_flag1 = (ord(s[1]) & 16 ) / 16
        self.unknown_flag2 = (ord(s[1]) & 32 ) / 32
        self.lamp1_status = (ord(s[1]) & 8) / 8
        self.lamp2_status = (ord(s[1]) & 4) / 4
        self.projector_status = (ord(s[1]) & 2) / 2
        self.at_zero_position = ord(s[1]) & 1
        self.slide_lift_motor_error = (ord(s[2]) & 128) /128
        self.tray_transport_motor_error = (ord(s[2]) & 64) / 64
        self.command_error = (ord(s[2]) & 32)  / 32
        self.overrun_error = (ord(s[2]) & 16) / 16 
        self.buffer_overflow_error = (ord(s[2]) & 8) / 8
        self.framing_error = (ord(s[2]) & 4) / 4
        log.debug (self.get_details())

    def print_status(self):
        log.debug ("unknown_flag1" + str(self.unknown_flag1 ))
        log.debug ("unknown_flag2" + str(self.unknown_flag2 ))
        log.debug ("projector_status" + str(self.projector_status))
        log.debug ("at_zero_position" + str(self.at_zero_position))
        log.debug ("slide_lift_motor_error" + str(self.slide_lift_motor_error))
        log.debug ("tray_transport_motor_error" + str(self.tray_transport_motor_error))
        log.debug ("command_error" + str(self.command_error ))
        log.debug ("overrun_error" + str(self.overrun_error))
        log.debug ("buffer_overflow_error" + str( self.buffer_overflow_error))
        log.debug ("overrun_error" + str(self.overrun_error))
        log.debug ("self.framing_error" + str(self.framing_error))
             

    def sync(self):
        log.debug ("sync")
        c = EktaproCommand(self.projektorID).statusGetTrayPosition()
        log.debug ("sync. Send: " + str (c) + " hex: " + repr (c.toData()))
        log.debug ("sync2")
        self.serialDevice.write(c.toData())
        s = self.serialDevice.read(3)
        log.debug ("GetTray. Revd: " + repr(s))  
##        if (len (s) != 3) \
##            or not (ord(s[0]) % 8 == 6) \
##            or not (ord(s[1]) / 16 == 10):
##            log.error ("get_status invalid response. Sent: " + c.toData() + " Revd: " + repr(s))  
##            #raise IOError, "Invalid response"
##        else:    
##            self.slide = int(str(ord(s[2])))


class EktaproCommand:

    """
    Represents a single low level 3 byte command that is sent to an Ektapro slide projector
    by the user software.
     
    Permits easy construction of the 3 byte commands and decoding of 3 byte hex sequences to into
    a human readable string (for example for debugging).  
    """

    def __init__(self, *args):
        if len(args) == 1:
            self.projektorID = args[0]
            self.initalized = False
        elif len(args) == 3:
            self.projektorID = args[0] / 8
            self.mode = args[0] % 8 / 2
            self.arg1 = args[1]
            self.arg2 = args[2]
            self.initalized = True
        else:
            raise Exception, "Argument count invalid"
        
    def toData(self):
        if not self.initalized:
            raise Exception, "Command not initialized"

        return chr(self.projektorID * 8 + self.mode * 2 + 1) \
            + chr(self.arg1) + chr(self.arg2)

    # Command  construction
    # Parameter mode

    def constructParameterCommand(self, command, param):
        self.mode = 0
        self.arg1 = command * 16 + param / 128 * 2
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
    # String  conversion
    #

    def __str__(self):
        commandstring = {
            0: "Parameter Mode - " + self.parameterModeToString(),
            1: "Set/Reset Mode - " + self.setResetModeToString(),
            2: "Direct Mode - " + self.directModeToString(),
            3: "Status Request Mode - " + self.statusRequestToString()
        }

        return "Projector " + str(self.projektorID) + " - " \
               + commandstring.get(self.mode, "Unknown Mode")

    def parameterModeToString(self):
        upDown = {
            0: "Down",
            1: "Up"
        }

        parametersettings = {
            0: "Random Access - Slide " + str(self.arg1 % 16 * 64 + self.arg2 / 2),
            1: "SetBrightness - " + str(self.arg1 % 16 * 64 + self.arg2 / 2),
            3: "Group Address - " + str(self.arg2 / 2),
            6: "Fade up/down - " + upDown.get(self.arg1 % 16 / 2, "?") + " - "
                + str(self.arg2 / 2),
            7: "SetLowerLimit for Fading - " + str(self.arg1 % 16 * 64 + self.arg2 / 2),
            8: "SetUpperLimit for Fading - " + str(self.arg1 % 16 * 64 + self.arg2 / 2)
        }

        return parametersettings.get(self.arg1 / 16, "Unknown parameter")

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

        return setresetstring.get(self.arg1 / 4, "Unknown command") \
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

        if self.arg1 / 128 == 1:
            return "Direct User Mode"

        return directModeString.get(self.arg1 / 4, "Unknown command")

    def statusRequestToString(self):
        statusRequests = {
            10: "GetTray position",
            11: "GetKeys",
            12: "System status",
            13: "System return"
        }
        return statusRequests.get(self.arg1 / 16, "Unknown request")       
