#!/usr/bin/env python3
"""
   Copyright (C) 2014,2015 Breager
   One projector per serial port is supported.

"""

from contextlib import contextmanager
import threading
from enum import Enum
from ektapro import *
from cam import *
from gardasoft import *

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s',
                    datefmt='%M:%S')
log = logging.getLogger(__name__)


class ScanState(Enum):
    stopped = 1
    scanning = 2


class ScanType(Enum):
    prev = 1
    next = 2
    current = 3
    start_end = 4


class Process:
    def __init__(self, msg_q, file_q):
        self.msg_queue = msg_q
        self.file_queue = file_q
        self.lock = TimeoutLock()

        self.capture_delay_min = 0
        self.capture_delay_max = 10000
        self.capture_settle_delay = 100

        self.slot_min = 0
        self.slot_max = 140
        self.slot_start = 1
        self.slot_end = 80

        self.scan_state = ScanState.stopped

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
        self.msg_queue.put("Init done")

    def scan_threaded(self, scan_type=ScanType.start_end, start=1, end=1):
        thread = threading.Thread(target=self.scan, args=(scan_type, start, end))
        thread.daemon = True  # thread dies when main thread (only non-daemon thread) exits.
        thread.start()

    def scan(self, scan=ScanType.start_end, start=1, end=1):
        with self.lock.acquire_timeout(0):
            self.scan_state = ScanState.scanning
            if scan == ScanType.start_end:
                self.slot_start = start
                self.slot_end = end
                if self.tpt_enabled:
                    self.tpt.select(self.slot_start)
            elif scan == ScanType.next:
                self.tpt.next(post_timeout=0)
                self.slot_start = self.tpt.slide
                self.slot_end = self.tpt.slide
            elif scan == ScanType.prev:
                self.tpt.prev(post_timeout=0)
                self.slot_start = self.tpt.slide
                self.slot_end = self.tpt.slide
            else:  # scan == ScanType.current: or anything...
                self.slot_start = self.tpt.slide
                self.slot_end = self.tpt.slide

            if not self.led_enabled:
                self.led.continuous(1, 0)
            log.info("scanning slots " + str(self.slot_start) + " to " + str(self.slot_end))
            for slide in range(self.slot_start, self.slot_end + 1):
                ts = time.time()
                self.msg_queue.put("Scanning slide in slot " + str(slide))
                if self.scan_state == ScanState.stopped:
                    self.msg_queue.put("Stopping scanning")
                    break
                if self.tpt_enabled and not scan == ScanType.current:
                    try:
                        while self.tpt.get_status(busy_check=True):
                            pass
                    except EktaproError:
                        break
                    if self.capture_settle_delay > 0:
                        log.info("settle delay (ms) :" + str(self.capture_settle_delay))
                        time.sleep(self.capture_settle_delay / 1000)
                if self.led_enabled:
                    self.led.continuous(1, self.led_flash)
                if self.cam_enabled:
                    self.cam_capture()
                if self.led_enabled:
                    self.led.continuous(1, self.led_rest)
                if self.tpt_enabled and (slide != self.slot_end):
                    log.info("set")
                    self.tpt.next(post_timeout=0)
                if self.cam_enabled:
                    file = "/home/dan/Documents/pics/" + str(slide) + ".jpg"
                    log.debug("Capture complete - Now save" + file)
                    self.cam_save(file)
                    self.file_queue.put(file)
                log.debug("Scan time: " + str(time.time() - ts) + "for slot: " + str(slide))
            self.stop_scan()

    def cam_capture(self):
        self.cam.open()
        self.cam.capture()

    def cam_save(self, file):
        self.cam.save(file)
        self.cam.close()

    def connect_hardware(self):
        with self.lock.acquire_timeout(0):
            # gardasoft setup
            self.led.open(None)
            if self.led.connected:
                self.led.version()
                self.led.strobe(1, 0, 4000, 4)
                self.led.continuous(1, self.led_rest)
                self.led_port = self.led.port
                self.led_connected = self.led.connected

            # ektapro setup
            self.tpt.open(None)
            # for gui layer
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
            self.led.close()
            self.cam.close()
            self.tpt.reset()  # move back to 0 position
            self.tpt.close()

    def led_on(self):
        with self.lock.acquire_timeout(0):
            self.led.continuous(1, self.led_flash)

    def led_off(self):
        with self.lock.acquire_timeout(0):
            self.led.continuous(1, 0)

    def stop_scan(self):
        self.scan_state = ScanState.stopped

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

    def acquire(self, blocking=True, time_out=-1):
        return self._lock.acquire(blocking, time_out)

    @contextmanager
    def acquire_timeout(self, time_out):
        result = self._lock.acquire(timeout=time_out)
        yield result
        if result:
            self._lock.release()

    def release(self):
        self._lock.release()


if __name__ == "__main__":
    import time
    from queue import Queue
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                        datefmt='%H:%M:%S')
    msg_queue = Queue()
    file_queue = Queue()
    ms = Process(msg_queue, file_queue)
    ms.connect_hardware()
    ms.disconnect_hardware()
    ms.connect_hardware_threaded()
    time.sleep(10000)


