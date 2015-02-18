mechascan
=========

Slide samples

http://www.quadrumedia.com/film/slides

Fedora 21 install

Manually install libgphoto2 

Edit /etc/ld.so.conf

add /usr/local/lib/ to top of file 

As root run ldconfig --verbose | grep gpho

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


You can list the directories pkg-config looks in by default using:

>pkg-config --variable pc_path pkg-config
and....
>pkg-config --libs --cflags libgphoto2










