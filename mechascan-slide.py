#!/usr/bin/env python3
"""
   MechaScan-Slide
   
   Copyright (C) 2014,2015 Breager 
   One projector per serial port is supported.
"""

from tkinter.constants import SINGLE, END, DISABLED, HORIZONTAL, BOTTOM, W, X, LEFT, BOTH, RIGHT, N, TOP, NORMAL
from tkinter import * 
import tkinter.messagebox
import tkinter.simpledialog
#import tkinter.scolledtext
import yaml, argparse, pprint, os, logging , fcntl, threading
from enum import Enum
from ektapro import *
from cam import *
from gardasoft import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)d %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
logit = logging.getLogger('gphoto2')
logit.setLevel(logging.INFO)

class scan_state (Enum):
    stopped = 1
    scanning = 2

class Main():
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
        self.cam = CameraDevice()
        self.led = GardasoftDevice()
        self.tpt = EktaproDevice()
        self.create_gui()
        self.gui ("Enable")
        self.update_clock()         #this creates tk callback and time to update gui
        thread = threading.Thread(target=self.init_hardware, args = (self.led, self.tpt, self.cam ))
        thread.daemon = True        # thread dies when main thread (only non-daemon thread) exits.
        thread.start()
        self.t.mainloop()
    
    def scan(self):
        self.t.stopButton.config(state=NORMAL)
        self.t.startButton.config(state=DISABLED)
        if not self.enable_led.get(): self.led.continuous (1,0)
        self.scan_state = scan_state.scanning 
        ok = False
        if self.enable_tpt.get(): self.tpt.select(self.slot_start)
        for slide in range(self.slot_start, self.slot_end + 1):
            ts = time.time()
            log.debug("Scanning count: " + str (slide))
            self.update_gui()
            if (self.scan_state == scan_state.stopped): break
            if self.enable_tpt.get():  
                while (self.tpt.get_status(busy = True, debug = False)):
                    self.update_gui()
                if (self.capture_delay > 0 ):
                    tcd = time.time()
                    while 1:
                        self.update_gui()
                        if (time.time () - tcd > (self.capture_delay /1000)):
                            break
                    log.debug ( "Delay for: " + str(time.time () - tcd))            
            if self.enable_led.get(): self.led.continuous (1, self.led_flash)
            self.update_gui()    
            if (self.enable_cam.get() == True):
                try:
                    self.cam.open()
                except:
                    pass
                try:
                    ok = self.cam.capture()
                except:
                    pass
            self.update_gui()    
            if self.enable_led.get(): self.led.continuous (1, self.led_rest)
            self.update_gui()
            if self.enable_tpt.get():  
                self.tpt.next(post_timeout = 0)
                self.update_gui()
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
            warn ("LED device not connected")
        led.strobe(1,0,4000,4)
        led.continuous (1, self.led_rest)
        
        #ektapro setup
        tpt.open(None)
        tpt.reset()


    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.t.time_label.configure(text=now)
        if (self.tpt.get_status_busy()):
            self.t.busy_label.configure(text= "Transport Busy")
        else:
            self.t.busy_label.configure(text= "Transport Rest")
        self.t.update()
        self.t.after(100, self.update_clock)
        
    def connect_press(self):
        init_hardware()
        self.gui ("Enable")

    def inputs_change(self, event=None):
        try:
            log.error ("Event " + event.type )
        except:
            pass
        if self.scan_state == scan_state.stopped:
            try:
                capture_delay = int(self.t.capture_delay_input.get())
            except:
                capture_delay = -1
            if capture_delay in range(self.capture_delay_min, self.capture_delay_max):
                self.capture_delay = capture_delay
                log.debug ("Valid delay: " + str (capture_delay))
            else:
                log.error ("Invalid delay: " + str (capture_delay))
                self.capture_delay = self.capture_delay_min
                self.t.capture_delay_input.delete(0, END)
                self.t.capture_delay_input.insert(0, self.capture_delay)

            log.debug ("Start slot: " + str (self.t.slot_start_input.get()))
            try:
                slot_start = int(self.t.slot_start_input.get())
            except:
                slot_start = -1
            if slot_start in range(1, self.slot_max):
                self.slot_start = slot_start
                log.debug ("Valid Start slot: " + str (self.slot_start))

            else:
                self.slot_start = self.slot_min
                log.error ("Start slot: " + str (self.slot_start))
                self.t.slot_start_input.delete(0, END)
                self.t.slot_start_input.insert(0, self.slot_start)

            try:
                slot_end = int(self.t.slot_end_input.get())
            except:
                slot_end = -1
            if slot_end in range(1, 140):
                self.slot_end = slot_end
                log.debug ("Valid End slot: " + str (self.slot_end))
            else:
                self.slot_end = self.slot_max
                log.error ("End slot: " + str (self.slot_end))
                self.t.slot_end_input.delete(0, END)
                self.t.slot_end_input.insert(0, self.slot_end)

    def start_scan_press(self):
        self.t.stopButton.config(state=NORMAL)
        self.t.startButton.config(state=DISABLED)
        self.scan()
        
    def stop_scan_press(self):
        self.stop_scan()

    def stop_scan (self):
        self.scan_state = scan_state.stopped
        self.t.stopButton.config(state=DISABLED)
        self.t.startButton.config(state=NORMAL)

    def gui (self, state):
        if (state == "Enable"):
            self.t.gotoSlideScale.config(state=NORMAL)
            self.t.nextButton.config(state=NORMAL)
            self.t.prevButton.config(state=NORMAL)
            self.t.startButton.config(state=NORMAL)
            self.t.capture_delay_input.config(state=NORMAL)
            self.t.syncButton.config(state=NORMAL)
            self.t.statusButton.config(state=NORMAL)
            
        if (state == "Disable"):
            self.t.gotoSlideScale.config(state=DISABLED)
            self.t.nextButton.config(state=DISABLED)
            self.t.prevButton.config(state=DISABLED)
            self.t.startButton.config(state=DISABLED)
            self.t.stopButton.config(state=DISABLED)
            self.t.capture_delay_input.config(state=DISABLED)
            self.t.syncButton.config(state=DISABLED)
            self.t.statusButton.config(state=DISABLED)

    def enable_camera_press(self):
        pass

    def status_press (self):
        self.tpt.get_status()

    def sync_press(self):
        self.tpt.sync()

    def home_press(self):
        self.tpt.select(0)
        self.t.gotoSlideScale.set(self.tpt.slide)
        
    def gotoSlideChanged(self, event):
        newSlide = self.t.gotoSlideScale.get()
        self.tpt.select(newSlide)
        self.t.gotoSlideScale.set(self.tpt.slide)

    def next_press(self):
        next(self)
        self.t.gotoSlideScale.set(self.tpt.slide)

    def prev_press(self):
        self.prev()
        self.t.gotoSlideScale.set(self.tpt.slide)

    def __next__(self):
        self.tpt.next(pre_timeout = 0, post_timeout = 0)
        
    def prev(self):
        self.tpt.prev(pre_timeout = 1.5, post_timeout = 1.5)
       
    def update_gui(self):
        #log.debug("Update GUI")
        self.t.gotoSlideScale.set(self.tpt.slide)
        #self.inputs_change()
        self.t.update()

    def onQuit(self):
        try:
            led.close()
        except:
            pass
        try:
            self.cam.close()
        except:
            pass
        try:
            self.tpt.reset()
            self.tpt.close()
        except:
            pass
        #self.t.destroy()

##    def create_gui_image_viewer(self):
##        self.tiv = Toplevel()
##        self.tiv.geometry("1920x1080+130+0")
##        self.tiv.protocol('WM_DELETE_WINDOW', self.onQuit)
##        self.tiv.wm_title("Image View")
##        canvas = Canvas(self.tiv, width=400, height=300,  background=BLACK )
##        canvas.pack()
##
##        # Load the image file
##        im = Image.open("./images/ektachrome-kodak.jpg")
##        # Put the image into a canvas compatible class, and stick in an
##        # arbitrary variable to the garbage collector doesn't destroy it
##        canvas.image = ImageTk.PhotoImage(im)
##        # Add the image to the canvas, 
##        canvas.create_image(0, 0, image=canvas.image)
##      
##        self.t.bind("<Prior>", self.prev_press)
##        self.t.bind("<Next>", self.next_press)

        
    def create_gui(self):
        self.t = Tk()
        self.t.geometry("1920x1080+130+0")
        self.t.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.t.wm_title("Mechascan Slide")

        self.t.bind("<Prior>", self.prev_press)
        self.t.bind("<Next>", self.next_press)

        self.t.status_panel = Frame(self.t, borderwidth=2,  relief="sunken")
        self.t.settings_panel = Frame(self.t)
        self.t.control_panel = Frame(self.t)

        self.t.manual_panel = Frame(self.t)
        #self.t.log_panel = Frame(self.t)
              
        self.t.manual_panel.grid (row=0, column=0, sticky='ew' )
        self.t.status_panel.grid (row=4, column=0, sticky='ew' )
        self.t.settings_panel.grid (row=1, column=0, sticky='ew' )
        self.t.control_panel.grid (row=2, column=0, sticky='ew' )
        #self.t.log_panel.grid (row=3, column=0, sticky='nsew' )

        self.t.grid_rowconfigure(3, weight=1)
        self.t.grid_columnconfigure(3, weight=1)

        #self.t.txt = ScrolledText(self.t.log_panel, undo=True)
        #self.t.txt['font'] = ('consolas', '12')
        #self.t.txt.pack(expand=True, fill='both')

        self.t.time_label = Label(self.t.status_panel, text="Busy", borderwidth=2,  relief="sunken")
        self.t.time_label.pack(side=RIGHT, anchor=N, padx=1, pady=1)
        self.t.statusLabel = Label(self.t.status_panel, text="Status", borderwidth=2,  relief="sunken")
        self.t.statusLabel.pack(side=RIGHT, anchor=N, padx=1, pady=1)
        self.t.busy_label = Label(self.t.status_panel, text="Busy", borderwidth=2,  relief="sunken")
        self.t.busy_label.pack(side=RIGHT, anchor=N, padx=1, pady=1)
        self.t.led_type_label = Label(self.t.status_panel, text="Led Type", borderwidth=2,  relief="sunken")
        self.t.led_type_label.pack(side=RIGHT, anchor=N, padx=1, pady=1)
        self.t.led_port_label = Label(self.t.status_panel, text="Led Port", borderwidth=2,  relief="sunken")
        self.t.led_port_label.pack(side=RIGHT, anchor=N, padx=1, pady=1)
        self.t.led_value_label = Label(self.t.status_panel, text="Led Value", borderwidth=2,  relief="sunken")
        self.t.led_value_label.pack(side=RIGHT, anchor=N, padx=1, pady=1)
        self.t.cam_type_label = Label(self.t.status_panel, text="Cam Type", borderwidth=2,  relief="sunken")
        self.t.cam_type_label.pack(side=RIGHT, anchor=N, padx=1, pady=1)
      
        self.t.connectButton = Button(self.t.control_panel, text="Connect Transport", command=self.connect_press)
        self.t.nextButton = Button(self.t.control_panel, text=" > ", command=self.next_press)
        self.t.prevButton = Button(self.t.control_panel, text=" < ", command=self.prev_press)
        self.t.startButton = Button(self.t.control_panel, text="Start Scanning", command=self.start_scan_press)
        self.t.stopButton = Button(self.t.control_panel, text="Stop Scanning", command=self.stop_scan_press)
        self.t.homeButton = Button(self.t.control_panel, text="Home", command=self.home_press)
        self.t.syncButton = Button(self.t.control_panel, text="Get Position", command=self.sync_press)
        self.t.statusButton = Button(self.t.control_panel,text="Status", command=self.status_press)

        self.t.capture_delay_label = Label(self.t.settings_panel, text="Pre capture delay")
        self.t.capture_delay_input = Entry(self.t.settings_panel, width=3)
        self.t.capture_delay_input.insert(0, self.capture_delay)
        self.t.capture_delay_input.bind("<KeyPress-Return>", self.inputs_change)
        self.t.capture_delay_input.bind("<Leave>", self.inputs_change)
        self.t.capture_delay_input.bind("<ButtonRelease>", self.inputs_change)
        
        self.t.slot_start_label = Label(self.t.settings_panel, text="Starting at slot")
        self.t.slot_start_input = Entry(self.t.settings_panel, width=3)
        self.t.slot_start_input.insert(0, "1")
        self.t.slot_start_input.bind("<KeyPress-Return>", self.inputs_change)
        self.t.slot_start_input.bind("<Leave>", self.inputs_change)
        self.t.slot_start_input.bind("<ButtonRelease>", self.inputs_change)

        self.t.slot_end_label = Label(self.t.settings_panel, text="Ending at slot")
        self.t.slot_end_input = Entry(self.t.settings_panel, width=3)
        self.t.slot_end_input.insert(0, "80")
        self.t.slot_end_input.bind("<KeyPress-Return>", self.inputs_change)
        self.t.slot_end_input.bind("<Leave>", self.inputs_change)
        self.t.slot_end_input.bind("<ButtonRelease>", self.inputs_change)

        self.enable_cam = BooleanVar()
        self.t.enable_cam = Checkbutton(self.t.settings_panel, 
                                         text="Use camera", 
                                         variable=self.enable_cam)
        self.t.enable_cam.select()
                
        self.auto_home = BooleanVar()
        self.t.auto_home = Checkbutton(self.t.settings_panel,
                                       text="Auto return to 0 slot",
                                       variable=self.auto_home)
        self.t.auto_home.select()

        self.enable_led = BooleanVar()
        self.t.enable_led = Checkbutton(self.t.settings_panel,
                                       text="Use lamp",
                                       variable=self.enable_led)
        self.t.enable_led.select()

        self.enable_tpt = BooleanVar()
        self.t.enable_tpt = Checkbutton(self.t.settings_panel,
                                       text="Use transport",
                                       variable=self.enable_tpt)
        self.t.enable_tpt.select()
               
        self.t.gotoSlideScale = Scale(self.t.manual_panel, from_=0, to=self.slot_max, label="Select slide")
        self.t.gotoSlideScale.bind("<ButtonRelease>", self.gotoSlideChanged)
        self.t.gotoSlideScale.config(orient=HORIZONTAL)
        self.t.gotoSlideScale.config(length=400)


        #layout panels
        self.t.connectButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.t.prevButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.t.homeButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.t.nextButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.t.startButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
                       
        self.t.stopButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.t.syncButton.pack(side=LEFT, anchor=N, padx=4, pady=4)
        self.t.statusButton.pack(side=LEFT, anchor=N, padx=4, pady=4)

        #settings
        self.t.capture_delay_input.pack(side=RIGHT, anchor=N, padx=1, pady=4)
        self.t.capture_delay_label.pack(side=RIGHT, anchor=N, padx=4, pady=4)

        self.t.slot_end_input.pack(side=RIGHT, anchor=N, padx=1, pady=4)
        self.t.slot_end_label.pack(side=RIGHT, anchor=N, padx=1, pady=4)
        self.t.slot_start_input.pack(side=RIGHT, anchor=N, padx=1, pady=4)
        self.t.slot_start_label.pack(side=RIGHT, anchor=N, padx=1, pady=4)
        
        self.t.enable_cam.pack(side=RIGHT, anchor=N, padx=4, pady=3)
        self.t.enable_led.pack(side=RIGHT, anchor=N, padx=4, pady=3)
        self.t.enable_tpt.pack(side=RIGHT, anchor=N, padx=4, pady=3)
        self.t.auto_home.pack(side=RIGHT, anchor=N, padx=4, pady=3)
                
        self.t.gotoSlideScale.pack(side=TOP, anchor=W, expand=1, fill=X)
        
        self.t.menubar = Menu(self.t)
        self.t.toolsmenu = Menu(self.t.menubar)
        self.t.helpmenu = Menu(self.t.menubar)
        self.t.filemenu = Menu(self.t.menubar)

        self.t.helpmenu.add_command(label="About MechaScan", command=lambda: tkMessageBox.showinfo(
                                      "About MechaScan","MechaScan 0.1 (C)opyright Breager 2014"))
        self.t.filemenu.add_command(label="Exit", command=self.onQuit)
        self.t.menubar.add_cascade(label="File", menu=self.t.filemenu)
        self.t.menubar.add_cascade(label="Help", menu=self.t.helpmenu)
        self.t.configure(menu=self.t.menubar)

if __name__ == '__main__':
    Main()


