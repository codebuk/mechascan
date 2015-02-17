
#!/usr/bin/env python3
"""
   Copyright (C) 2014,2015 Breager
   One projector per serial port is supported.

"""
from contextlib import contextmanager
import logging, threading
from enum import Enum
from ektapro import *
from cam import *
from gardasoft import *

class scan_state (Enum):
    stopped = 1
    scanning = 2

class process:
    def __init__(self, q):
        self.queue = q
        self.lock = TimeoutLock()

        self.capture_delay_min = 0
        self.capture_delay_max = 10000
        self.settle_delay = 100

        self.slot_min = 0
        self.slot_max = 140
        self.slot_start = 1
        self.slot_end = 80

        self.scan_state = scan_state.stopped

        self.led_flash = 2000
        self.led_rest = 0

        self.led_enabled = True
        self.led_port = "Not connected"
        self.led_connected = False

        self.tpt_enabled = True
        self.tpt_port = "Not connected"
        self.tpt_connected = False

        self.cam_enabled = True
        self.cam_port = "Not connected"
        self.cam_connected = False


        self.cam = CameraDevice()
        self.led = GardasoftDevice()
        self.tpt = EktaproDevice()
        self.queue.put("Init done")

    def scan_threaded(self):
        thread = threading.Thread(target=self.scan)
        thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        thread.start()

    def scan(self):
        with self.lock.acquire_timeout(0):
            try:
                if self.led_enabled and not self.led.connected:
                    self.queue.put("Lamp not connected")
                    raise "Lamp not connected"
                if self.tpt_enabled and not self.tpt.connected:
                    self.queue.put("Transport not connected")
                    raise "Transport not connected"
                if self.cam_enabled and not self.cam.connected:
                    self.queue.put("Camera not connected")
                    raise "Camera  not connected"

                if not self.led_enabled: self.led.continuous(1, 0)
                self.scan_state = scan_state.scanning
                ok = False
                if self.tpt_enabled: self.tpt.select(self.slot_start)

                for slide in range(self.slot_start, self.slot_end + 1):
                    ts = time.time()
                    self.queue.put("Scanning slide in slot " + str(slide))
                    if (self.scan_state == scan_state.stopped): break
                    if (self.tpt_enabled):
                        while (self.tpt.get_status(busy=True, debug=False)): pass
                        if (self.settle_delay > 0 ):
                            log.info("settle delay (ms) :" + str(self.settle_delay))
                            time.sleep(self.settle_delay / 1000)
                    if self.led_enabled: self.led.continuous(1, self.led_flash)
                    if (self.cam_enabled == True): cam_capture()
                    if self.led_enabled: self.led.continuous(1, self.led_rest)
                    if self.tpt_enabled: self.tpt.next(post_timeout=0)
                    if self.enable_cam.get():
                        file = "/home/dan/Documents/pics/" + str(slide) + ".jpg"
                        log.debug("Capture complete - Now save" + file)
                        cam_save(file)
                    log.debug("Scan time: " + str(time.time() - ts) + "for slot: " + str(slide))
            except:
                pass
            self.stop_scan()

    def cam_capture(self):
        self.cam.open()
        self.ok = self.cam.capture()

    def cam_save(self, file):
        self.cam.save(file)
        self.cam.close()

    def connect_hardware (self):
        with self.lock.acquire_timeout(0):
            # gardasoft setup
            self.led.open(None)
            try:
                self.led.version()
            except:
                log.warn("LED device not connected")
            self.led.strobe(1, 0, 4000, 4)
            self.led.continuous(1, self.led_rest)
            self.led_port = self.led.port
            self.led_connected = self.led.connected

            # ektapro setup
            self.tpt.open(None)
            self.tpt.reset()
            self.tpt_port = self.tpt.port
            self.tpt_connected = self.tpt.connected

            self.cam_port = self.cam.port
            self.cam_connected = self.cam.connected



    def connect_hardware_threaded(self):
        thread = threading.Thread(target=self.connect_hardware)
        thread.daemon = True        # thread dies when main thread (only non-daemon thread) exits.
        thread.start()

    def disconnect_hardware(self):
        with self.lock.acquire_timeout(0):
            try:
                led.close()
            except:
                pass
            try:
                self.cam.close()
            except:
                pass
            try:
                self.tpt.reset()  # move back to 0 position
                self.tpt.close()
                self.led_port = self.led.port
            except:
                pass
            return True

    def led_on(self):
        with self.lock.acquire_timeout(0):
            self.led.continuous(1, self.led_flash)

    def led_off(self):
        with self.lock.acquire_timeout(0):
            self.led.continuous(1, 0)

    def capture_delay(self, delay):
        try:
            capture_delay = int(delay)
        except:
            capture_delay = -1
        if capture_delay in range(self.capture_delay_min, self.capture_delay_max):
            self.settle_delay = capture_delay
            log.debug ("Valid capture delay: " + str (capture_delay))
        else:
            log.error ("Invalid capture delay: " + str (capture_delay))
            self.settle_delay = self.capture_delay_min
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
        with self.lock.acquire_timeout(0):
            self.tpt.select(slot)

    def get_slot(self):
        with self.lock.acquire_timeout(0):
            return self.tpt.slide

    def home_slot(self):
        with self.lock.acquire_timeout(0):
            self.tpt.select(0)

    def tpt_reset(self):
        with self.lock.acquire_timeout(0):
            self.tpt.reset()


    def next_slot(self):
        with self.lock.acquire_timeout(0):
            self.tpt.next(pre_timeout=0, post_timeout=0)

    def prev_slot(self):
        with self.lock.acquire_timeout(0):
            self.tpt.prev(pre_timeout=1.5, post_timeout=1.5)


class TimeoutLock(object):
    def __init__(self):
        self._lock = threading.Lock()

    def acquire(self, blocking=True, timeout=-1):
        return self._lock.acquire(blocking, timeout)

    @contextmanager
    def acquire_timeout(self, timeout):
        result = self._lock.acquire(timeout=timeout)
        yield result
        if result:
            self._lock.release()

    def release(self):
        self._lock.release()


if __name__ == "__main__":
    import traceback, time, logging
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
    ms = process()
    ms.connect_hardware()
    ms.disconnect_hardware()
    ms.connect_hardware_threaded()
    time.sleep (10000)


