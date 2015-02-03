#!/usr/bin/env python3
"""
   Copyright (C) 2014,2015 Breager
   One projector per serial port is supported.
"""

import logging, threading
from enum import Enum
from ektapro import *
from cam import *
from gardasoft import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
# shut up gphoto
logit = logging.getLogger('gphoto2')
logit.setLevel(logging.INFO)

class scan_state (Enum):
    stopped = 1
    scanning = 2

class mechascan_process():
    def __init__(self):
        self.capture_delay_min = 0
        self.capture_delay_max = 10000
        self.capture_delay = 100
        self.slot_min = 0
        self.slot_max = 140
        self.slot_start = 1
        self.slot_end = 80
        self.scan_state = scan_state.stopped
        self.led_flash = 2000
        self.led_rest = 0
        self.led_enabled = True
        self.tpt_enabled = True
        self.cam_enabled = True
        self.cam = CameraDevice()
        self.led = GardasoftDevice()
        self.tpt = EktaproDevice()

    def scan(self):
        if not self.led_enable: self.led.continuous (1,0)
        self.scan_state = scan_state.scanning
        ok = False
        if self.tpt_enabled: self.tpt.select(self.slot_start)
        for slide in range(self.slot_start, self.slot_end + 1):
            ts = time.time()
            log.debug("Scanning count: " + str (slide))
            if (self.scan_state == scan_state.stopped): break
            if (self.tpt_enabled):
                while (self.tpt.get_status(busy = True, debug = False)):
                    print ("1 = 1")
                if (self.capture_delay > 0 ):
                    tcd = time.time()
                    while 1:
                        if (time.time () - tcd > (self.capture_delay /1000)):
                            break
                    log.debug ( "Delay for: " + str(time.time () - tcd))
            if self.led_enabled:self.led.continuous (1, self.led_flash)
            if (self.cam_enabled == True):
                try:
                    self.cam.open()
                except:
                    pass
                try:
                    ok = self.cam.capture()
                except:
                    pass
            if self.led_enabled: self.led.continuous (1, self.led_rest)
            if self.enable_tpt.get(): self.tpt.next(post_timeout = 0)
            if (ok and self.enable_cam.get()):
                f = "/home/dan/Documents/pics/" + str(slide) + ".jpg"
                log.debug ("Capture complete - Now save" + f )
                self.cam.save(f)
                self.cam.close()
            log.error("Scan time: " + str(time.time () - ts) + "for slot: " + str (slide))
        self.stop_scan()

    def init_hardware (self, led, tpt, cam):
        #gardasoft setup
        led.open(None)
        try:
            led.version()
        except:
            log.warn ("LED device not connected")
        led.strobe(1,0,4000,4)
        led.continuous (1, self.led_rest)

        #ektapro setup
        tpt.open(None)
        tpt.reset()

    def connect_hardware_threaded(self):
        thread = threading.Thread(target=self.init_hardware, args = (self.led, self.tpt, self.cam ))
        thread.daemon = True        # thread dies when main thread (only non-daemon thread) exits.
        thread.start()

    def connect_hardware(self):
        self.init_hardware ( self.led, self.tpt, self.cam )

    def disconnect_hardware(self):
        try:
            led.close()
        except:
            pass
        try:
            self.cam.close()
        except:
            pass
        try:
            self.tpt.reset()  #move back to 0 position
            self.tpt.close()
        except:
            pass

    def capture_delay(self, delay):
        try:
            capture_delay = int(delay)
        except:
            capture_delay = -1
        if capture_delay in range(self.capture_delay_min, self.capture_delay_max):
            self.capture_delay = capture_delay
            log.debug ("Valid capture delay: " + str (capture_delay))
        else:
            log.error ("Invalid capture delay: " + str (capture_delay))
            self.capture_delay = self.capture_delay_min
            #todo raise err

    def slot_start(self, slot_start):
        try:
            slot_start = int(slot_start)
        except:
            slot_start = -1
        if slot_start in range(1, self.slot_max):
            self.slot_start = slot_start
            log.debug ("Valid Start slot: " + str (self.slot_start))

        else:
            self.slot_start = self.slot_min
            log.error ("Start slot: " + str (self.slot_start))
            raise "err" #??      #todo raise err

    def slot_end (self, slot_end):
        try:
            slot_end = int(slot_end)
        except:
            slot_end = -1
        if slot_end in range(1, 140):
            self.slot_end = slot_end
            log.debug ("Valid End slot: " + str (self.slot_end))
        else:
            self.slot_end = self.slot_max
            log.error ("End slot: " + str (self.slot_end))
            #todo raise err

    def stop_scan (self):
        self.scan_state = scan_state.stopped

    def select_slot(self, slot):
        self.tpt.select(slot)

    def home_slot(self):
        self.tpt.select(0)

    def next_slot(self):
        self.tpt.next(pre_timeout=0, post_timeout=0)

    def prev_slot(self):
        self.tpt.prev(pre_timeout=1.5, post_timeout = 1.5)



if __name__ == "__main__":
    import traceback, time, logging
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
    ms = mechascan_process()
    ms.connect_hardware()
    ms.disconnect_hardware()
    ms.connect_hardware_threaded()
    time.sleep (10000)


