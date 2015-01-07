import traceback, time, logging
from gardasoft import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
#er0-5 give answers...
led = GardasoftDevice()
led.dump_port_list()
led.open(None)
if (led.connected):
    log.info("LED device connected")
else:
    log.error ("LED device not connected")
try:
    led.version()
except:
    log.warn ("LED device not connected")

def test1(l):
    try:
        led.continuous ( l , 2000)
        time.sleep (.3)
        led.continuous ( l , 0)
        time.sleep (1)
        led.strobe(l,0,4000,20)
        led.status()
        log.info ("Version: " + led.version())
        #for x in range(0, 1000, 1):
        #    led.continuous ( l, x)
        #for x in range(500, 0, -50):
        #    led.continuous ( l, x)
        led.all_off()
        led.clear_error()
        
    except Exception, err:
        traceback.print_exc()
        print "emergency shut off"
        led.all_off()
        sys.stderr.write('ERROR: %s\n' % str(err))

test1(2)
#test1(2)
