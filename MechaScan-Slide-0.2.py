#!/usr/bin/env python
"""
   MechaScan-Slide
   
   Copyright (C) 2014,2015 Breager Pty. Ltd.

   This program serves as a controller for the ektapro slide projector
   devices. It searches for slide projector devices on the serial
   ports on startup, and presents a GUI to manually control
   the projectors or use a timer for automatic slideshows.
   One projector per serial port is supported.
"""


from Tkconstants import SINGLE, END, DISABLED, HORIZONTAL, BOTTOM, W, X, LEFT, \
    BOTH, RIGHT, N, TOP, NORMAL
from Tkinter import Tk, Frame, Listbox, Button, Label, Entry, IntVar, \
    Checkbutton, Scale, Menu
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

class EktaproGUI(Tk):
    #Constructs the main program window and interfaces with the EktaproDevice
    def __init__(self):
        self.tpt = EktaproDevice()
        self.led = GardasoftDevice()
        self.cam = CameraDevice()
        Tk.__init__(self)
        self.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.wm_title("Mechascan Slide")
        self.bind("<Prior>", self.prevPressed)
        self.bind("<Next>", self.nextPressed)

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
        self.startButton = Button(self.controlPanel, text="Start Scanning", command=self.start_scan)
        self.pauseButton = Button(self.controlPanel, text="II", command=self.pause_scan)
        self.stopButton = Button(self.controlPanel, text="Stop Scanning", command=self.stop_scan)

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
        self.update_clock()

    #def capture_images(self):
    #    log("Capture Images selected")

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.statusLabel.configure(text=now)
        self.after(1000, self.update_clock)
        self.updateGUI()

    def connectButtonPressed(self):
        self.init_hardware()
        self.gui ("Enable")
        self.updateGUI("Connect")

    def inputValuesChanged(self, event):
        auto_delay = int(self.timerInput.get())
        if auto_delay in range(0, 6000):
            self.auto_delay = auto_delay
            log.debug ("Valid delay: " + unicode (auto_delay))
        else:
            log.error ("Invalid delay: " + unicode (auto_delay))

        start_slot = int(self.start_slot_input.get())
        if start_slot in range(1, 140):
            self.start_slot = start_slot
            log.debug ("Start slot: " + unicode (start_slot))
        else:
            log.error ("Start slot: " + unicode (start_slot))

        end_slot = int(self.end_slot_input.get())
        if end_slot in range(1, 140):
            self.end_slot = end_slot
            log.debug ("End slot: " + unicode (end_slot))
        else:
            log.error ("End slot: " + unicode (end_slot))
        self.updateGUI()

    def start_scan(self):
        self.stopButton.config(state=NORMAL)
        self.startButton.config(state=DISABLED)
        self.scan()
        
    def pause_scan(self):
        self.pauseButton.config(text="->")
        self.updateGUI()

    def stop_scan(self):
        self.pauseButton.config(text="Pause")
        self.stopButton.config(state=DISABLED)
        self.startButton.config(state=NORMAL)
        self.updateGUI()

    def scan(self):
        self.stopButton.config(state=NORMAL)
        self.startButton.config(state=DISABLED)
        #self.tpt.next(post_timeout = 2.0) 
        ok = False
        for slide in range(1, 80):
            log.debug("Scanning count: " + str (slide)) 
            if self.tpt == None:
                return
            while (self.tpt.get_status(busy = True, debug = False)):
                self.updateGUI()
                self.update()
            self.led.continuous (1, 2000)
            try:
                self.cam.open()
            except:
                pass
            try:
                ok = self.cam.capture()
            except:
                pass
            self.led.continuous (1, 200)
            if (ok):
                f = "/home/dan/pics/" + str(slide) + ".jpg"
                log.debug ("Capture complete - Now save" + f )
                self.cam.save(f)
                self.cam.close()
            self.tpt.next(post_timeout = 0)  #do the move - do not wait after starting move
            self.updateGUI()
            
    ##        if self.auto_active:
    ##            self.lock.acquire()
    ##            if not self.timer_active:
    ##                self.timer_active = True
    ##                log.debug ("Start Delay(ms): " + self.auto_delay)
    ##                self.gui.after(int (self.auto_delay), self.timer_event)
    ##            self.lock.release()
            #self.count = self.count + 1
            #if (self.count >= 81): self.stop_auto()

    
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
        self.gotoSlideScale.set(self.tpt.slide)

    def gotoSlideChanged(self, event):
        newSlide = self.gotoSlideScale.get()
        self.tpt.select(newSlide)

    def nextPressed(self):
        log.debug ("next pressed")
        #if self.startButton.config()["state"][4] == "disabled":
        self.next()
        self.updateGUI()

    def prevPressed(self):
        log.debug ("prev pressed")
        if self.startButton.config()["state"][4] == "disabled":
            self.toggleStandby()
        else:
            self.prev()
            self.updateGUI()
        
    def next(self):
        self.tpt.next(pre_timeout = 1.5, post_timeout = 1.5)
        
    def prev(self):
        self.tpt.prev(pre_timeout = 1.5, post_timeout = 1.5)

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
        self.led.continuous (1, 100)
        
        #ektapro setup
        self.tpt.open(None)
        self.tpt.reset()
       
        #camera setup #none required

    def onQuit(self):
        self.tpt.close()
        self.led.close()
        self.cam.close()
        self.destroy()

if __name__ == '__main__':
    mainWindow = EktaproGUI()
    mainWindow.mainloop()
