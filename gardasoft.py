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
        self.connected = 0

    def open(self, port):
        self.ver = ""
        self.connected = 0
        #self.ser.close()
        if (port is None):
            for port, desc, hwid in sorted(comports(), reverse=True):
                if (self.open_port( port)):
                    return True
        else:
            if (self.open_port( port)):
                return True
        return False

    def open_port(self, port):
        log.info("Trying port: " + port)
        try:
            collection = [ 9600, 115200]
            for speeds in collection:
                self.ser = serial.serial_for_url(port, speeds, timeout=.1, writeTimeout=.01)
                log.info("Port opened: " + port)
                try:
                    fcntl.flock(self.ser, fcntl.LOCK_EX | fcntl.LOCK_NB )
                except IOError:
                    log.info( "Can not immediately write-lock the file as it is locked: " + port)
                else:
                    log.info ("Port not locked. Check for device at: " + str(speeds) + " baud. Port: " + port)
                    self.ser.flush() 
                    self.ser.read(2000) #clear any junk
                    self.connected = 1
                    if (self.clear_error()):
                        self.ser.timeout = .1 #tried .01 but random errors 
                        self.ver = self.version()
                        return 1
                    self.connected = 0
                    self.ser.close()
        except serial.SerialException:
            logging.error("Serial exception")
            pass
        except IOError:
            logging.error("Not a Gardasoftdevice")
            return 0
        

    def write_read(self, mess, read_char):
        if (self.connected):
            try:
                self.ser.write(str( mess))
                self.ser.flush()
                info = self.ser.read(read_char)
                return info
            except:
                raise

    def close(self):
        self.connected = 0
        self.all_off()
        self.ser.close()
        
    def status(self):
        info = repr(self.write_read ( "ST\n\r" , 200))
        if (info):
            log.debug ("Status: " + info)
            return info
        else:
            return ""

    def version(self):
        info = self.write_read ( "VR\n\r", 20)
        if (info):
            ver = re.search("\A.*VR(.*)\n\r>\Z", info, re.DOTALL)
            if ver:
                name = ver.group(1)
                log.debug('version -' + name)
                return name
            else:
                log.error('version not valid' + repr(info))
                raise Exception('Version not valid')
        return ""
            

    def clear_error(self):
        info = self.write_read ( "GR\n\r" , 10)
        if (info):
            er = re.search("\A(GR\n\r>)\Z", info, re.DOTALL)
            if er:
                log.debug('clear error OK')
                return 1
            log.error("clear error found error. Response: " + repr(info)) #do not raise error on clearerror
            er = re.search("GREC1", info, re.DOTALL)
            if er:
                log.debug('max current clear ok')
                return 1
            if (re.search("GRErr 21", info, re.DOTALL)):
                log.debug('Err 21 - Bad command format')
                return 1
            if (re.search("GRE", info, re.DOTALL)):
                log.debug('Other error see docs')
                return 1
        return 0
        
    def all_off(self):
        self.continuous(1, 0)
        self.continuous(2, 0)
        log.debug('All off OK')

    def continuous(self, channel, current):
        com = 'RC' + str(channel) + "C0V" + str(current) + "\n\r"
        z = len (com)
        mesg = 'continous ' + str(channel) + ' - ' + str(current) + " - " + repr(com)
        info = self.write_read ( com , z + 1)
        if (info == None):
            return 0
        er = re.search("\A" + com + "(>)\Z", info, re.DOTALL)
        if er:
            log.debug(mesg) # + "--" + unicode (info) )
        else:
            log.error ("Send: " + mesg + "  len: " + str(z) + " response size: " + str (len(info)) + " Response: " + str (info))
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
