import sys, serial, io, re, logging, fcntl
log = logging.getLogger(__name__)

try:
    from serial.tools.list_ports import comports
except ImportError:
    comports = None


class GardasoftDevice:
    # communications port should be set to 9600 baud, no parity, 8 data bits, 1 stop bit.
    # al characters are echoed so read returns characters sent to device

    def __init__(self):
        log.debug('gardasoft device init')

    def open(self, port):
        if (port is None):
            for port, desc, hwid in sorted(comports(), reverse=True):
                log.info("Trying port: " + port + " --- " + desc + " --- " + hwid)
                try:
                    self.ser = serial.serial_for_url(port, 9600, timeout=1, writeTimeout=.01)
                    try:
                        fcntl.flock(self.ser, fcntl.LOCK_EX)
                        #fcntl.flock(open('/tmp/locktest', 'r'), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except IOError:
                        log.info("can't immediately write-lock the file as it is locked")
                    else:
                        log.info ("Not locked")
                        self.ser.flush()
                        self.ser.read(200) #clear any junk
                        if (self.clear_error()):
                            return 1
                        self.ser.close()
                        self.ser = serial.serial_for_url(port, 115200, timeout=1, writeTimeout=.01)
                        self.ser.flush()
                        self.ser.read(200) #clear any junk
                        if (self.clear_error()):
                            return 1
                        
                except serial.SerialException:
                    pass
                except IOError:
                    logging.error("Not a Gardasoftdevice")
            return 0        
        else:
            log.info('open port ' + port)
            try:
                self.ser = serial.serial_for_url(port, 9600, timeout=1, writeTimeout=.01)
                if (self.clear_error()):
                    return 1
            except serial.SerialException:
                pass
            except IOError:
                logging.error("Not a Gardasoftdevice")
        return 0

    def close(self):
        self.all_off()
        #todo self.ser.close()
        
    def status(self):
        self.ser.write(unicode("ST\n\r"))
        self.ser.flush()
        info = self.sio.readline()
        print repr(info)

    def version(self):
        self.ser.write(unicode("VR\n\r"))
        self.ser.flush()
        info = self.ser.read(20)
        ver = re.search("\A.*VR(.*)\n\r>\Z", info, re.DOTALL)
        if ver:
            name = ver.group(1)
            log.info('version -' + name)
        else:
            log.error('version not valid' + repr(info))
            raise Exception('Version not valid')

    def clear_error(self):
        self.ser.write("GR\n\r")
        self.ser.flush()
        info = self.ser.read(5)
        er = re.search("\A(GR\n\r>)\Z", info, re.DOTALL)
        if er:
            log.debug('clear error OK')
            return 1
        log.error("clear error found error. Response: " + repr(info)) #do not raise error on clearerror
        er = re.search("GREC1", info, re.DOTALL)
        if er:
            log.debug('max current clear ok')
            return 1
        
        return 0
        
    def all_off(self):
        self.continuous(0, 0)
        self.continuous(1, 0)
        log.debug('All off OK')

    def continuous(self, channel, current):
        com = 'RC' + unicode(channel) + "C0V" + unicode(current) + "\n\r"
        z = len (com)
        mesg = 'continous ' + unicode(channel) + ' - ' + unicode(current) + " - " + repr(com)
        self.ser.write(unicode(com))
        self.ser.flush()
        info = self.ser.read( z + 1)
        er = re.search("\A" + com + "(>)\Z", info, re.DOTALL)
        if er:
            log.debug(mesg) # + "--" + unicode (info) )
        else:
            log.error ("Send: " + mesg + "  len: " + str(z))
            log.error ("Length of response: " + str (len(info)))
            log.error ("Rsponse: " + unicode (info))
            #self.clearerror()
            #self.all_off()
            log.error(mesg)
            raise Exception('Bad continous response' + repr(info))

    def strobe(self, channel, min_current, max_current, count):
        for x in range (0, count):
            self.continuous ( channel, max_current)
            self.continuous ( channel, min_current)
        self.all_off()

    def dump_port_list(self):
        if comports:
            sys.stderr.write('\n--- Available ports:\n')
            for port, desc, hwid in sorted(comports()):
                sys.stderr.write('--- %-20s %s [%s]\n' % (port, desc, hwid))
