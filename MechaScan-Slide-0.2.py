#!/usr/bin/env python
"""
   MechaScan-Slide
   
   Copyright 2014 Breager

   This program serves as a controller for the ektapro slide projector
   devices. It searches for slide projector devices on the serial
   ports on startup, and presents a GUI to manually control
   the projectors or use a timer for automatic slideshows. Currently,
   only one projector per serial port is supported.
"""


from Tkconstants import SINGLE, END, DISABLED, HORIZONTAL, BOTTOM, W, X, LEFT, \
    BOTH, RIGHT, N, TOP, NORMAL
from Tkinter import Tk, Frame, Listbox, Button, Label, Entry, IntVar, \
    Checkbutton, Scale, Menu
from thread import allocate_lock
import tkMessageBox
import tkSimpleDialog
import os, logging , fcntl

# custom modules
from ektapro import *
from gardasoft import *
from cam import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
logit = logging.getLogger('gphoto2')
logit.setLevel(logging.INFO)

class TimerController:

    #Contains the logic to control the timer and fading mechanism.
    def __init__(self, tpt, gsd, cam,  gui):
        log.debug ("tc init")
        self.t_tpt = tpt
        self.t_led = gsd
        self.t_cam = cam
        self.gui = gui
        self.auto_active = False
        self.timer_active = False
        self.auto_paused = False
        self.lock = allocate_lock()
        self.auto_delay = 1
        self.count = 1000
        self.end_slot = 80
        self.start_slot = 0

    def next(self):
        log.debug("Next count: " + str (self.count) + " start: " + str(self.start_slot))
        if self.t_tpt == None:
            return
        if (self.start_slot <=  self.count):
            self.t_led.continuous (1, 4000)
            try:
                self.t_cam.open()
            except:
                pass
            try:
                ok = self.t_cam.capture()
            except:
                pass
            if (ok):
                f = "/home/dan/pics/" + str(self.count) + ".jpg"
                log.debug ("Capture complete - Now save" + f )
                self.t_cam.save(f)
                self.t_cam.close()
            self.t_led.continuous (1, 200)
            self.t_tpt.next(0, 0)  #do the move - do not wait after starting move
        
        if self.auto_active:
            self.lock.acquire()
            if not self.timer_active:
                self.timer_active = True
                log.debug ("Start Delay(ms): " + self.auto_delay)
                self.gui.after(int (self.auto_delay), self.timer_event)
            self.lock.release()
        self.count = self.count + 1
        if (self.count >= 81): self.stop_auto()

    def prev(self):
        if self.t_tpt == None:
            return
        else:
            self.t_tpt.prev(pre_timeout = 1.5, post_timeout = 1.5)
            return

    def start_auto(self):
        if self.t_tpt == None:
            return
        self.auto_delay = self.gui.timerInput.get()
        self.auto_active = True
        self.auto_paused = False
        self.count = 0
        log.debug ("Delay: " + self.auto_delay)
        self.lock.acquire()
        if not self.timer_active:
            self.gui.after( int(self.auto_delay), self.timer_event)
            self.timer_active = True
        self.lock.release()

    def pause(self):
        self.auto_paused = True

    def resume(self):
        self.auto_paused = False
        self.lock.acquire()
        if not self.timer_active:
            self.timer_active = True
            self.gui.after(50, self.timer_event)
        self.lock.release()

    def stop_auto(self):
        self.auto_active = False
        self.auto_paused = False
        self.gui.pauseButton.config(text="II")
        self.t_tpt.reset()

    def timer_event(self):
        log.debug("Timer Event" + str (self.count))
        self.timer_active = False
        if (self.count > self.end_slot):
            self.stop_auto()
        if self.t_tpt == None:
            return
        if self.auto_active and not self.auto_paused:
            self.t_led.continuous (1,200)
            self.next()
            self.gui.updateGUI()

class EktaproGUI(Tk):
    #Constructs the main program window and interfaces with the EktaproDevice
    #and the TimerController to access the slide projector.
    def __init__(self):
        self.tpt = EktaproDevice()
        self.led = GardasoftDevice()
        self.cam = CameraDevice()
        Tk.__init__(self)
        self.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.wm_title("Mechascan Slide")
        self.bind("<Prior>", self.prevPressed)
        self.bind("<Next>", self.nextPressed)
        self.slide = 1
        self.timerController = TimerController(self.tpt, self.led, self.cam, self)
        self.statusPanel = Frame(self)
        self.controlPanel = Frame(self)
        self.manualPanel = Frame(self)
        #status panel
        self.statusLabel = Label(self.statusPanel, text="Status")
        self.statusLabel.pack(side=RIGHT, anchor=N, padx=4, pady=4)
        #control panel
        self.connectButton = Button(self.controlPanel, text="Connect Transport", command=self.connectButtonPressed)
        self.nextButton = Button(self.controlPanel, text=" > ", command=self.nextPressed)
        self.prevButton = Button(self.controlPanel, text=" < ", command=self.prevPressed)
        self.startButton = Button(self.controlPanel, text="Start Scanning", command=self.startTimer)
        self.pauseButton = Button(self.controlPanel, text="II", command=self.pauseTimer)
        self.stopButton = Button(self.controlPanel, text="Stop Scanning", command=self.stopTimer)

        self.timerLabel = Label(self.controlPanel, text="Stable Time")
        self.timerInput = Entry(self.controlPanel, width=3)
        self.timerInput.insert(0, "500")
        self.timerInput.bind("<KeyPress-Return>", self.inputValuesChanged)
        self.timerInput.bind("<ButtonRelease>", self.updateGUI)
        
        self.start_slot_label = Label(self.controlPanel, text="Slot Start")
        self.start_slot_input = Entry(self.controlPanel, width=3)
        self.start_slot_input.insert(0, "1")
        self.start_slot_input.bind("<KeyPress-Return>", self.inputValuesChanged)
        self.start_slot_input.bind("<ButtonRelease>", self.updateGUI)

        self.end_slot_label = Label(self.controlPanel, text="Slot End")
        self.end_slot_input = Entry(self.controlPanel, width=3)
        self.end_slot_input.insert(0, "80")
        self.end_slot_input.bind("<KeyPress-Return>", self.inputValuesChanged)
        self.end_slot_input.bind("<ButtonRelease>", self.updateGUI)
        
        self.syncButton = Button(self.controlPanel, text="Get Position", command=self.sync)
        self.statusButton = Button(self.controlPanel,text="Status", command=self.status)
        self.enable_camera = IntVar()
        self.enable_camera = Checkbutton(self.controlPanel, text="Capture Images", variable=self.enable_camera, command=self.enable_camera_toggle)
        self.gotoSlideScale = Scale(self.manualPanel, from_=0, to=self.tpt.maxDisplayTray, label="Select slide")
        self.gotoSlideScale.set(1)
        self.gotoSlideScale.bind("<ButtonRelease>", self.gotoSlideChanged)
        self.gotoSlideScale.config(orient=HORIZONTAL)
        self.gotoSlideScale.config(length=400)
        self.gui ("Disable")
        #setup panels - order is important....
        self.manualPanel.pack(side=TOP, expand=1, fill=BOTH)
        self.statusPanel.pack(side=BOTTOM, anchor=W, fill=X)
        self.controlPanel.pack(side=RIGHT, anchor=W, fill=X)
        #layout panels
        self.connectButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.prevButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.nextButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.startButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.pauseButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
               
        self.stopButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.syncButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.statusButton.pack(side=LEFT, anchor=N, padx=4, pady=4)

        self.end_slot_input.pack(side=RIGHT, anchor=N, padx=4, pady=4)
        self.end_slot_label.pack(side=RIGHT, anchor=N, padx=4, pady=4)

        self.start_slot_input.pack(side=RIGHT, anchor=N, padx=4, pady=4)
        self.start_slot_label.pack(side=RIGHT, anchor=N, padx=4, pady=4)
               
        self.timerInput.pack(side=RIGHT, anchor=N, padx=4, pady=4)
        self.timerLabel.pack(side=RIGHT, anchor=N, padx=4, pady=4)
        
        self.enable_camera.pack(side=RIGHT, anchor=N, padx=4, pady=4)
                
        self.gotoSlideScale.pack(side=TOP, anchor=W, expand=1, fill=X)
        
        self.menubar = Menu(self)
        self.toolsmenu = Menu(self.menubar)
        self.helpmenu = Menu(self.menubar)
        self.filemenu = Menu(self.menubar)

        self.helpmenu.add_command(label="About MechaScan", command=lambda: tkMessageBox.showinfo(
                                      "About MechaScan","MechaScan 0.1 (C)opyright Breager 2014"))
        self.filemenu.add_command(label="Exit", command=self.onQuit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.configure(menu=self.menubar)
        
        self.gui ("Enable")
        self.updateGUI("Connect")
        self.init_hardware()

    #def capture_images(self):
    #    log("Capture Images selected")

    def connectButtonPressed(self):
        self.init_hardware()
        self.gui ("Enable")
        self.updateGUI("Connect")

    def inputValuesChanged(self, event):
        auto_delay = int(self.timerInput.get())
        if auto_delay in range(0, 6000):
            self.timerController.auto_delay = auto_delay
            log.debug ("Valid delay: " + unicode (auto_delay))
        else:
            log.error ("Invalid delay: " + unicode (auto_delay))

        start_slot = int(self.start_slot_input.get())
        if start_slot in range(1, 140):
            self.timerController.start_slot = start_slot
            log.debug ("Start slot: " + unicode (start_slot))
        else:
            log.error ("Start slot: " + unicode (start_slot))

        end_slot = int(self.end_slot_input.get())
        if end_slot in range(1, 140):
            self.timerController.end_slot = end_slot
            log.debug ("End slot: " + unicode (end_slot))
        else:
            log.error ("End slot: " + unicode (end_slot))
            
        self.updateGUI()

    
    def gui (self, state):
        if (state == "Enable"):
            self.gotoSlideScale.config(state=NORMAL)
            self.nextButton.config(state=NORMAL)
            self.prevButton.config(state=NORMAL)
            self.startButton.config(state=NORMAL)
            self.timerInput.config(state=NORMAL)
            self.syncButton.config(state=NORMAL)
            self.statusButton.config(state=NORMAL)
        if (state == "Disable"):
            self.gotoSlideScale.config(state=DISABLED)
            self.nextButton.config(state=DISABLED)
            self.prevButton.config(state=DISABLED)
            self.startButton.config(state=DISABLED)
            self.stopButton.config(state=DISABLED)
            self.timerInput.config(state=DISABLED)
            self.syncButton.config(state=DISABLED)
            self.statusButton.config(state=DISABLED)

    def status (self):
        self.tpt.get_status()
    
    def sync(self):
        self.tpt.sync()
        self.updateGUI()

    def reconnect(self):
        self.tpt.close()
        self.tpt.init()
        self.updateGUI()

    def updateGUI(self, event=None):
        if self.tpt == None:
            return
        self.slide = self.tpt.slide
        self.gotoSlideScale.set(self.slide)

    def gotoSlideChanged(self, event):
        if self.tpt is None:
            return
        newSlide = self.gotoSlideScale.get()
        if not self.slide == newSlide:
            self.tpt.select(newSlide)
            self.slide = newSlide

    def nextPressed(self):
        log.debug ("next pressed")
        if self.startButton.config()["state"][4] == "disabled":
            self.pauseTimer()
        else:
            self.next()

    def prevPressed(self):
        log.debug ("prev pressed")
        if self.startButton.config()["state"][4] == "disabled":
            self.toggleStandby()
        else:
            self.prev()

    def next(self):
        if self.tpt is None:
            return
        self.timerController.next()
        self.updateGUI()

    def prev(self):
        if self.tpt is None:
            return
        self.timerController.prev()
        self.updateGUI()

    def startTimer(self):
        self.stopButton.config(state=NORMAL)
        self.startButton.config(state=DISABLED)
        self.timerController.start_auto()

    def pauseTimer(self):
        if self.timerController.pause_auto:
            self.pauseButton.config(text="II")
            self.timerController.resume()
            self.updateGUI()
        else:
            self.pauseButton.config(text="->")
            self.timerController.pause()
            self.updateGUI()

    def stopTimer(self):
        self.pauseButton.config(text="Pause")
        self.stopButton.config(state=DISABLED)
        self.startButton.config(state=NORMAL)
        self.timerController.stop_auto()
        self.updateGUI()

    def enable_camera_toggle(self):
       #self.enable_camera.cycle = True if self.cycle.get() == 1 else False
        log.info("Camera enabled")

    def toggleStandby(self):
        if self.pauseButton.config()["text"][4] == "pause" \
           and self.pauseButton.config()["state"][4] == "normal":
            self.pauseTimer()
        self.tpt.toggleStandby()
    
    def init_hardware (self):
        #gardasoft setup
        self.led.open(None)
        try:
            self.led.version()
        except:
            log.warn ("LED device not connected")
        self.led.strobe(1,0,4000,4)
        self.led.continuous (1, 200)
        
        #ektapro setup
        self.tpt.open(None)
        #log.info (str(self.tpt))
        self.tpt.reset()
       
        #camera setup
        #none required

    def onQuit(self):
        self.tpt.close()
        self.led.close()
        self.cam.close()
        self.destroy()

if __name__ == '__main__':
    mainWindow = EktaproGUI()
    mainWindow.mainloop()
