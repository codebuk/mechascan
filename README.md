mechascan
=========

## Fedora 25 install
```
dnf install dconf-editor
dnf install gphoto2
dnf install libgphoto2
dnf install libgphoto2-devel
sudo dnf install python3-devel   #gphoto2 python bindings require this
sudo dnf install python3-pyserial
sudo dnf install python3-exif
dnf install darktable   # decent RAW viewer

? sudo pip install exifread  #use pip install --user` 
sudo pip install gphoto2

### to stop gvfd mounting
sudo dnf remove gvfs-gphoto2
/usr/lib/udev/rules.d/40-libgphoto2.rules
```
```
sudo vi /etc/ld.so.conf
```
add /usr/local/lib/ to top of file 

As root run
``` 
ldconfig --verbose | grep gpho
```
eg:
```
[root@spain-dnt-com-au ~]# ldconfig --verbose | grep gph
ldconfig: Can't stat /usr/lib64/nx/X11: No such file or directory
ldconfig: Can't stat /libx32: No such file or directory
ldconfig: Path `/usr/lib' given more than once
ldconfig: Path `/usr/lib64' given more than once
ldconfig: Can't stat /usr/libx32: No such file or directory
	libgphoto2_port.so.12 -> libgphoto2_port.so.12.0.0
	libgphoto2.so.6 -> libgphoto2.so.6.0.0
	libgphoto2_port.so.10 -> libgphoto2_port.so.10.1.1
	libgphoto2.so.6 -> libgphoto2.so.6.0.0
	libgphoto2_port.so.10 -> libgphoto2_port.so.10.1.1
	libgphoto2.so.6 -> libgphoto2.so.6.0.0
	libgphoto2_port.so.10 -> libgphoto2_port.so.10.1.1
[root@spain-dnt-com-au ~]# exit
```
then 
```
su
```
add path 
``PKG_CONFIG_PATH="/usr/local/lib/pkgconfig/"; export PKG_CONFIG_PATH``
install 
`pip install gphoto2`
or manually >python3 setup.py install

You can list the directories pkg-config looks in by default using:

>pkg-config --variable pc_path pkg-config
and....
>pkg-config --libs --cflags libgphoto2

##Focus examples

https://github.com/fape/libgphoto2/blob/master/examples/focus.c

https://zoetrope.io/tech-blog/pursuit-better-tethered-autofocus

##Example Nikon D800E settings

High ISO NR - Off

##todo

30 seconds for projector to report a jam. eg slide stuck in slot
```
21:10.155-ektapro-Thread-1-DEBUG Busy: 1 Home: 0 Reset:0 F2:0 SLME:0 TTME:1 CE:0 BOE:0 OE:0 FE:0 L1:1 L2:1
 Model: Kodak Ektapro model: 5020 Id: 0 Version: 4.80 Slot: 6 Tray size: 80 Slide in gate: Yes Standby: Off Active lamp: L2 Standby: Off Power frequency: 50Hz Autofocus: Off Autozero: Off Low lamp mode: Off High light: Off
Exception in thread Thread-1:
Traceback (most recent call last):
  File "/usr/lib64/python3.4/threading.py", line 921, in _bootstrap_inner
    self.run()
  File "/usr/lib64/python3.4/threading.py", line 869, in run
    self._target(*self._args, **self._kwargs)
  File "/home/dan/PycharmProjects/mechascan/mechascan_process.py", line 104, in work
    job()
  File "/home/dan/PycharmProjects/mechascan/mechascan_gui.py", line 111, in <lambda>
    end=self.sb_end_slot.value()))
  File "/home/dan/PycharmProjects/mechascan/mechascan_process.py", line 245, in scan
    self.select_slot(0)
  File "/home/dan/PycharmProjects/mechascan/mechascan_process.py", line 271, in select_slot
    self._tpt.select(slot)
  File "/home/dan/PycharmProjects/mechascan/ektapro.py", line 204, in select
    self.comms(EktaproCommand(self.id).param_random_access(slide), pre_timeout=0, post_timeout=10)
  File "/home/dan/PycharmProjects/mechascan/ektapro.py", line 437, in comms
    self.poll_busy(post_timeout, desc="post timeout ")
  File "/home/dan/PycharmProjects/mechascan/ektapro.py", line 247, in poll_busy
    busy = self.get_status(busy_check=True)
  File "/home/dan/PycharmProjects/mechascan/ektapro.py", line 275, in get_status
    raise EktaproError(msg)
ektapro.EktaproError: tray_transport_motor_error
21:49.899-__main__-MainThread-DEBUG clearing task off queue
```









