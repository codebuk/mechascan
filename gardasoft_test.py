import traceback, time, logging
#import gardasoft
from gardasoft import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')

#er0-5 give answers...

led = GardasoftDevice()
led.dump_port_list()
led.open(None)
try:
    led.version()
except:
    log.warn ("LED device not connected")
led.strobe(0,0,2000,4)


led.status()
led.version()
led.clearerror()
led.shutdown(0)
led.shutdown(1)
for x in range(0, 500, 50):
    led.continuous ( 0, x)
for x in range(500, 0, -50):
    led.continuous ( 0, x)
for x in range (0, 20):
    led.continuous ( 0, 0)
    time.sleep (.2)
    led.continuous ( 0, 2000)
    time.sleep (.2)
led.shutdown("0")
led.clearerror()
  
#except Exception, err:
#    traceback.print_exc()
#    print "emergency shut off"
#    led.shutdown("0")
#    sys.stderr.write('ERROR: %s\n' % str(err))

