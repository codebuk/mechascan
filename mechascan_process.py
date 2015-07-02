#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#   One projector per serial port is supported.
#   Wraps led,c amera and tranport device.
#   Provides a high level interface to functions.
#   All GUI actions should be seperate to this module.


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

class ProcessError(Exception):
    pass


class Process:
    def __init__(self, msg_q, file_q, work_q):
        self.run = False
        self.msg_queue = msg_q
        self.file_queue = file_q
        self.work_queue = work_q
        self.lock = TimeoutLock()

        self.capture_delay_min = 0
        self.capture_delay_max = 10000
        self.capture_settle_delay = 100

        self.slot_min = 0
        self.slot_max = 140
        self.slot_start = 1
        self.slot_end = 80

        self.scan_state = ScanState.stopped

        self.led_flash = 350
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

        self._cam = None #CameraDevice()
        self._led = None #GardasoftDevice()
        self._tpt = None #EktaproDevice()
        self.msg_queue.put("Init done")

    def work_threaded(self):
        self.thread = threading.Thread(target=self.work)
        self.thread.daemon = False        # thread dies when main thread (only non-daemon thread) exits.
        self.thread.start()

    def work(self):
        self.run = True
        while self.run:
           log.debug ("waiting for work")
           job = self.work_queue.get()
           job()
           self.work_queue.task_done()
        log.debug("leaving work thread")


    def stop_scan(self):
        log.info("stopping scan")
        self.scan_state = ScanState.stopped

    def end(self):
        log.debug ("end msp thread")
        self.tpt_connect (open = False)
        self.led_connect (open = False)
        self.cam_connect (open = False)
        self.run = False
        return

    def tpt_connect (self, open = True):
        with self.lock.acquire_timeout(0):
            if open:
                self._tpt = EktaproDevice()
                # ektapro setup
                self._tpt.open(None)
                # for gui layer
                self.tpt_port = self._tpt.port
                self.tpt_connected = self._tpt.connected
                self.msg_queue.put("Transport connected")
            else:
                self.tpt_port = "Disabled"
                self.tpt_connected = False
                self._tpt.close()
                self._tpt = None
                self.msg_queue.put("Transport disconnected")

    def cam_connect (self, open = True):
        with self.lock.acquire_timeout(0):
            if open:
                self._cam = CameraDevice()
                cams = self._cam.list_cameras()
                #Nikon DSC D800E
                self._cam.open()
                self.cam_port = self._cam.port
                self._cam.use_sdram()
                self.cam_connected =self._cam.connected
                self.msg_queue.put("Camera connected")
            else:
                self.cam_port = "Disabled"
                self.cam_connected = False
                self._cam.close()
                self._cam = None
                self.msg_queue.put("Camera disconnected")

    def led_connect (self, open = True):
        with self.lock.acquire_timeout(0):
            if open:
                self._led = GardasoftDevice()
                self._led.open(None)
                if self._led.connected:
                    self._led.status()
                    self._led.version()
                    self._led.strobe(1, 0, self.led_flash, 4)
                    self._led.continuous(1, self.led_rest)
                    self.led_port =self._led.port
                    self.led_connected =self._led.connected
                    self.msg_queue.put("Lamp connected")
            else:

                self.led_port = "Disabled"
                self.led_connected = False
                self._led.close()
                self._led = None
                self.msg_queue.put("Lamp disconnected")


    def scan(self, scan_type=ScanType.start_end, start=1, end=1):
        with self.lock.acquire_timeout(0):
            if self.scan_state == ScanState.scanning:
                raise ProcessError ("Scan re-entered")
            self.scan_state = ScanState.scanning
            if scan_type == ScanType.start_end:
                self.slot_start = start
                self.slot_end = end
                if self.tpt_enabled:
                    self._tpt.select(self.slot_start)
            elif scan_type == ScanType.next:
                if self._tpt is not None:
                    self._tpt.next(post_timeout=0)
                    self.slot_start = self._tpt.slide
                    self.slot_end = self._tpt.slide
            elif scan_type == ScanType.prev:
                if self._tpt is not None:
                    self._tpt.prev(post_timeout=0)
                    self.slot_start = self._tpt.slide
                    self.slot_end = self._tpt.slide
            elif scan_type == ScanType.current:
                if self._tpt is not None:
                    self.slot_start = self._tpt.slide
                    self.slot_end = self._tpt.slide
                else:
                    self.slot_start = 0
                    self.slot_end = 0
            else:
                raise ProcessError ("Invalid scan type")
            log.info("scanning slots " + str(self.slot_start) + " to " + str(self.slot_end))
            for slide in range(self.slot_start, self.slot_end + 1):
                ts = time.time()
                self.msg_queue.put("Scanning slide in slot " + str(slide))
                if self.scan_state == ScanState.stopped:
                    self.msg_queue.put("Stopping scanning")
                    break
                if self.tpt_enabled and not scan_type == ScanType.current:
                    try:
                        self._tpt.log_debug = False
                        while self._tpt.get_status(busy_check=True)and (self.scan_state != ScanState.stopped):
                            pass
                    except EktaproError:
                        break
                    self._tpt.log_debug = False
                    self._tpt.get_status() # update status including slide in gate etc
                    if not self._tpt.slide_in_gate:
                        log.info('No slide in gate')
                    if self._tpt.slide_in_gate and self.capture_settle_delay > 0:
                        log.info("settle delay (ms) :" + str(self.capture_settle_delay))
                        time.sleep(self.capture_settle_delay / 1000)
                if self.led_enabled and self._tpt.slide_in_gate:
                    self._led.continuous(1, self.led_flash)
                if self.cam_enabled and ( self._tpt == None or self._tpt.slide_in_gate):
                    self.cam_capture()
                if self.led_enabled and self._tpt.slide_in_gate:
                    self._led.continuous(1, self.led_rest)
                if self.tpt_enabled and (slide != self.slot_end):
                    log.info("Move to next slot")
                    self._tpt.next(post_timeout=0)
                if self.cam_enabled and ( self._tpt == None or self._tpt.slide_in_gate):
                    file = "/home/dan/Documents/pics/" + str(slide) + ".jpg"
                    log.debug("Capture complete - Now save" + file)
                    self.cam_save(file)
                    self.file_queue.put(file)
                log.debug("Scan time: " + str(time.time() - ts) + "for slot: " + str(slide))
            if scan_type == ScanType.start_end:
                # todo check checkbox!
                self.select_slot(0)
            self.stop_scan()

    def cam_capture(self):
       self._cam.open()
       self._cam.capture()

    def cam_save(self, file):
       self._cam.save(file)
       self._cam.close()

    def led_on(self):
        with self.lock.acquire_timeout(0):
            if self._led is not None:
                self._led.continuous(1, self.led_flash)

    def led_off(self):
        with self.lock.acquire_timeout(0):
            if self._led is not None:
                self._led.continuous(1, 0)

    def select_slot(self, slot):
        with self.lock.acquire_timeout(0):
            if self._tpt is not None:
                self._tpt.select(slot)

    def get_slot(self):
        if self._tpt is not None:
            return self._tpt.slide
        else:
            return 0

    def get_slide_in_gate(self):
        if self._tpt is not None:
            return self._tpt.slide_in_gate
        else:
            return 0

    def home_slot(self):
        with self.lock.acquire_timeout(0):
            self._tpt.select(0)

    def tpt_reset(self):
        with self.lock.acquire_timeout(0):
            if self._tpt is not None:
                self._tpt.reset()

    def next_slot(self):
        with self.lock.acquire_timeout(0):
            self._tpt.next(pre_timeout=0, post_timeout=0)

    def prev_slot(self):
        with self.lock.acquire_timeout(0):
            self._tpt.prev(pre_timeout=1.5, post_timeout=1.5)

    def get_tpt_tray_size(self):
        if self._tpt is not None:
            return self._tpt.tray_size
        else:
            return 80 # fake value


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


