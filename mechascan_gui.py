from PyQt5.QtCore import Qt, QDir, QRect, QTimer
from PyQt5.QtGui import QImage, QPixmap, QTransform, QPainter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem,
                             QMenu, QDialog, QFileDialog, QMessageBox, QFrame, QRubberBand, QLabel,
                             QProgressBar)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from functools import partial
import os
from random import random
import editimage
import preferences
from fileimage import read_list  # write_list
import logging
import mechascan_process
from mechascan_process import ScanType
from queue import Queue
# ui generated code
from main_window import *

# external libs
#import exifread


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s.%(msecs)d-%(name)s-%(threadName)s-%(levelname)s %(message)s",
                    datefmt='%M:%S')
log = logging.getLogger(__name__)
# shut up gphoto
logit = logging.getLogger('gphoto2')
logit.setLevel(logging.INFO)


class MechascanSlideGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MechascanSlideGUI, self).__init__()
        self.fname = ''
        self.lbl_led_status = ''
        self.lbl_tpt_status = ''
        self.lbl_cam_status = ''
        self.lbl_slot_status = ''
        self.auto_orient = True
        self.slide_delay = 0
        self.quality = 0

        self.progress = None
        self.popup = None
        self.pixmap = None
        self.ss_timer = None

        self.filelist = []
        self.img_index = 0
        self.last_file = 0
        self.slides_next = True

        self.msg_queue = Queue()
        self.file_queue = Queue()
        self.msp = mechascan_process.Process(self.msg_queue, self.file_queue)
        self.msp.connect_hardware_threaded()

        self.setupUi(self)
        self.printer = QPrinter()
        self.load_img = self.load_img_fit  # default load type

        # to make this work in qtdesigner add a widget to the central abd then use a horizontal layout
        # then delete the widget

        self.scene = QGraphicsScene()
        # self.img_view = ImageView(self.centralwidget)
        self.img_view = ImageView(self)
        self.img_view.setScene(self.scene)
        self.horizontalLayout.addWidget(self.img_view)  # add widget to uic generated form

        self.reload_img = self.reload_auto
        # self.open_new = self.parent.open_win
        # self.exit = self.parent().closeAllWindows
        self.create_actions()
        self.create_menu()
        self.orient_dict = self.create_dict()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested.connect(self.show_menu)
        self.read_prefs()
        # noinspection PyTypeChecker,PyCallByClass
        self.pics_dir = os.path.expanduser('~/Pictures') or QDir.currentPath(self)
        # we use a timer to process status updates from the process module
        #we could have used signals but I did not want to make the module dependant on qt
        self.timer = QtCore.QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(5)
        self.resize(1000, 600)

    # scan functions

    def scan(self):
        if self.msp_update_from_gui():
            self.msp.scan_threaded(scan_type=ScanType.start_end,
                                   start=self.sb_start_slot.value(),
                                   end=self.sb_end_slot.value())
            # self.msp.scan()

    def scan_next(self):
        if self.msp_update_from_gui():
            self.msp.scan_threaded(scan_type=ScanType.next)

    def scan_prev(self):
        if self.msp_update_from_gui():
            self.msp.scan_threaded(scan_type=ScanType.prev)

    def scan_current(self):
        if self.msp_update_from_gui():
            self.msp.scan_threaded(scan_type=ScanType.current)

    def scan_stop(self):
        self.msp.stop_scan()

    def tpt_slot_current(self, x):
        self.msp.select_slot(x)

    def lamp_on(self, checked):
        if checked:
            self.msp.led_on()
        else:
            self.msp.led_off()

    def update_gui(self):

        # empty msg queue - just grab the last message for display as user will
        # only be able to see the last message
        msg = ""
        while not self.msg_queue.empty():
            try:
                msg = self.msg_queue.get_nowait()
                log.info(msg)
                self.msg_queue.task_done()
            except:
                raise
        if msg:
            self.statusbar.showMessage(msg, 1000)

        file = ""
        while not self.file_queue.empty():
            try:
                file = self.file_queue.get_nowait()
                log.info("File on disk: " + file)
                self.file_queue.task_done()
            except:
                raise
        if file:
            self.fname = file
            self.reload_img()

        # noinspection PyUnresolvedReferences
        self.lbl_led_status.setText("LED: " + self.msp.led_port)
        # noinspection PyUnresolvedReferences
        self.lbl_tpt_status.setText("Transport: " + self.msp.tpt_port)
        # noinspection PyUnresolvedReferences
        self.lbl_cam_status.setText("Camera: " + self.msp.cam_port)
        # noinspection PyUnresolvedReferences
        self.lbl_slot_status.setText("Slot: " + str(self.msp.get_slot()))
        if self.sb_start_slot.maximum() != self.msp.tpt.tray_size:
            self.sb_start_slot.setMaximum(self.msp.tpt.tray_size)
            self.sb_start_slot.setValue(1)
            self.sb_end_slot.setMaximum(self.msp.tpt.tray_size)
            self.sb_end_slot.setValue(self.msp.tpt.tray_size)

    def msp_update_from_gui(self):
        self.msp.led_enabled = self.check_led.isChecked()
        self.msp.cam_enabled = self.check_cam.isChecked()
        self.msp.tpt_enabled = self.check_tpt.isChecked()
        self.msp.auto_home_enabled = self.cb_auto_home.isChecked()
        self.msp.capture_settle_delay = self.sb_settle_delay.value()

        # check if ok to start
        msg = ""
        if self.msp.led_enabled and not self.msp.led.connected:
            msg = "Lamp not connected\n\n"
        if self.msp.tpt_enabled and not self.msp.tpt.connected:
            msg += "Transport not connected\n\n"
        if self.msp.cam_enabled and not self.msp.cam.connected:
            msg += "Camera not connected"
        if msg:
            # noinspection PyCallByClass,PyArgumentList,PyTypeChecker
            QMessageBox.information(self, 'Can not start scanning', msg)
            return False
        else:
            return True

    # noinspection PyUnresolvedReferences
    def create_actions(self):
        # connect to uic generated objects
        self.tb_play.clicked.connect(self.scan)
        self.tb_stop.clicked.connect(self.scan_stop)
        self.tb_next.clicked.connect(self.scan_next)
        self.tb_prev.clicked.connect(self.scan_prev)

        self.pushButton_capture.clicked.connect(self.scan_current)

        self.pushButton_lamp.clicked.connect(self.lamp_on)
        self.pushButton_tpt_home.clicked.connect(partial(self.msp.select_slot, 1))
        self.pushButton_tpt_reset.clicked.connect(self.msp.tpt_reset)

        self.open_act.triggered.connect(self.open)
        self.open_new_act.triggered.connect(partial(self.open, True))
        self.reload_act.triggered.connect(self.reload_img)
        self.print_act.triggered.connect(self.print_img)
        self.save_act.triggered.connect(self.save_img)
        self.close_act.triggered.connect(self.close)
        # self.exit_act.triggered.connect(self.exit)
        self.fulls_act.triggered.connect(self.toggle_fs)
        self.ss_act.triggered.connect(self.toggle_slideshow)
        self.ss_next_act.triggered.connect(self.set_slide_type)
        self.next_act.triggered.connect(self.go_next_img)
        self.prev_act.triggered.connect(self.go_prev_img)
        self.rotleft_act.triggered.connect(partial(self.img_rotate, 270))
        self.rotright_act.triggered.connect(partial(self.img_rotate, 90))
        self.fliph_act.triggered.connect(partial(self.img_flip, -1, 1))
        self.flipv_act.triggered.connect(partial(self.img_flip, 1, -1))
        self.resize_act.triggered.connect(self.resize_image)
        self.crop_act.triggered.connect(self.crop_image)
        self.zin_act.triggered.connect(partial(self.img_view.zoom, 1.1))
        self.zout_act.triggered.connect(partial(self.img_view.zoom, 1 / 1.1))
        self.fit_win_act.triggered.connect(self.zoom_default)
        self.fit_win_act.setChecked(True)
        self.prefs_act.triggered.connect(self.set_prefs)
        self.props_act.triggered.connect(self.get_props)
        self.help_act.triggered.connect(self.help_page)
        self.about_act.triggered.connect(self.about_cm)
        self.sb_current_slot.valueChanged.connect(self.tpt_slot_current)

        self.lbl_led_status = QLabel(self)
        self.statusbar.addPermanentWidget(self.lbl_led_status)
        self.lbl_led_status.setText("Led: Not connected")
        self.lbl_tpt_status = QLabel(self)
        self.statusbar.addPermanentWidget(self.lbl_tpt_status)
        self.lbl_tpt_status.setText("Transport: Not connected")
        self.lbl_cam_status = QLabel(self)
        self.statusbar.addPermanentWidget(self.lbl_cam_status)
        self.lbl_cam_status.setText("Camera: Not connected")
        self.lbl_slot_status = QLabel(self)
        self.statusbar.addPermanentWidget(self.lbl_slot_status)
        self.lbl_slot_status.setText("Slot: N/A")
        self.progress = QProgressBar(self)
        self.progress.setMaximumSize(170, 19)
        self.statusbar.addPermanentWidget(self.progress)

    def create_menu(self):
        self.popup = QMenu(self)
        main_acts = [self.open_act, self.open_new_act, self.reload_act, self.print_act, self.save_act]
        edit_acts1 = [self.rotleft_act, self.rotright_act, self.fliph_act, self.flipv_act]
        edit_acts2 = [self.resize_act, self.crop_act]
        view_acts = [self.next_act, self.prev_act, self.zin_act, self.zout_act, self.fit_win_act, self.fulls_act,
                     self.ss_act, self.ss_next_act]
        help_acts = [self.help_act, self.about_act]
        end_acts = [self.prefs_act, self.props_act, self.close_act, self.exit_act]
        for act in main_acts:
            self.popup.addAction(act)
        edit_menu = QMenu(self.popup)
        edit_menu.setTitle('&Edit')
        for act in edit_acts1:
            edit_menu.addAction(act)
        edit_menu.addSeparator()
        for act in edit_acts2:
            edit_menu.addAction(act)
        self.popup.addMenu(edit_menu)
        view_menu = QMenu(self.popup)
        view_menu.setTitle('&View')
        for act in view_acts:
            view_menu.addAction(act)
        self.popup.addMenu(view_menu)
        help_menu = QMenu(self.popup)
        help_menu.setTitle('&Help')
        for act in help_acts:
            help_menu.addAction(act)
        self.popup.addMenu(help_menu)
        for act in end_acts:
            self.popup.addAction(act)

        # was self.
        action_list = main_acts + edit_acts1 + edit_acts2 + view_acts + help_acts + end_acts
        for act in action_list:
            self.addAction(act)

    def show_menu(self, pos):
        self.popup.popup(self.mapToGlobal(pos))

    def read_prefs(self):
        """Parse the preferences from the config file, or set default values."""
        conf = preferences.Config(__name__ + ".ini")
        try:
            values = conf.read_config()
            self.auto_orient = values[0]
            self.slide_delay = values[1]
            self.quality = values[2]
        except KeyError:
            self.auto_orient = True
            self.slide_delay = 5
            self.quality = 90
        except:
            log.error("Unexpected error:", sys.exc_info()[0])
            raise
        self.reload_img = self.reload_auto if self.auto_orient else self.reload_nonauto

    def set_prefs(self):
        """Write preferences to the config file."""
        dialog = preferences.PrefsDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.auto_orient = dialog.auto_orient
            self.slide_delay = dialog.delay_spinb.value()
            self.quality = dialog.qual_spinb.value()
            conf = preferences.Config(__name__ + '.ini')
            conf.write_config(self.auto_orient, self.slide_delay, self.quality)
        self.reload_img = self.reload_auto if self.auto_orient else self.reload_nonauto

    # def open_dir(self):
    # # noinspection PyCallByClass,PyTypeChecker
    # fname = QFileDialog.getExistingDirectory(self)
    #     # .getOpenFileName(self, 'Open File', self.pics_dir)[0]
    #     if fname:
    #         if fname.lower().endswith(read_list()):
    #             if new_win:
    #                 self.open_new(fname)
    #             else:
    #                 self.open_img(fname)
    #         else:
    #             # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
    #             QMessageBox.information(self, 'Error', 'Cannot load {} images.'.format(fname.rsplit('.', 1)[1]))

    def open(self, new_win=False):
        # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
        fname = QFileDialog.getOpenFileName(self, 'Open File', self.pics_dir)[0]
        if fname:
            if fname.lower().endswith(read_list()):
                if new_win:
                    self.open_new(fname)
                else:
                    self.open_img(fname)
            else:
                # noinspection PyArgumentList,PyCallByClass,PyTypeChecker
                QMessageBox.information(self, 'Error', 'Cannot load {} images.'.format(fname.rsplit('.', 1)[1]))

    def open_img(self, fname):
        self.fname = fname
        self.reload_img()
        dirname = os.path.dirname(self.fname)
        self.set_img_list(dirname)
        self.img_index = self.filelist.index(self.fname)
        self.statusbar.showMessage(fname, 2000)

    def set_img_list(self, dirname):
        """Create a list of readable images from the current directory."""
        filelist = os.listdir(dirname)
        self.filelist = [os.path.join(dirname, fname) for fname in filelist
                         if fname.lower().endswith(read_list())]
        self.filelist.sort()
        self.last_file = len(self.filelist) - 1

    def get_img(self):
        """Get image from fname and create pixmap."""
        # noinspection PyCallByClass,PyArgumentList,PyTypeChecker
        self.pixmap = QPixmap.fromImage(QImage(self.fname))
        self.setWindowTitle(self.fname.rsplit('/', 1)[1])

    def create_dict(self):
        """Create a dictionary to handle auto-orientation."""
        return {None: self.load_img,
                '1': self.load_img,
                '2': partial(self.img_flip, -1, 1),
                '3': partial(self.img_rotate, 180),
                '4': partial(self.img_flip, -1, 1),
                '5': self.img_rotate_flip_horizontal,
                '6': partial(self.img_rotate, 90),
                '7': self.img_rotate_flip_vertical,
                '8': partial(self.img_rotate, 270)}

    def reload_auto(self):
        """Load a new image with auto-orientation."""
        self.get_img()
        # try:
        # f = open(self.fname, 'rb')
        #tags = exifread.process_file(f, stop_tag='Image Orientation', details=False)
        #orient = tags.key('Image Orientation')
        #tags = exifread.process_file(f, ')
        #exif = GExiv2.Metadata(self.fname)
        #exif.get_exif_tags()
        #orient = GExiv2.Metadata()
        #orient. self.fname)['Exif.Image.Orientation']
        #self.orient_dict[orient]()
        #except:
        self.load_img()

    def reload_nonauto(self):
        """Load a new image without auto-orientation."""
        self.get_img()
        self.load_img()

    def load_img_fit(self):
        """Load the image to fit the window."""
        self.scene.clear()
        #todo
        self.scene.addPixmap(self.pixmap)
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        self.img_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def load_img_1to1(self):
        """Load the image at its original size."""
        self.scene.clear()
        self.img_view.resetTransform()
        self.scene.addPixmap(self.pixmap)
        self.scene.setSceneRect(0, 0, self.pixmap.width(), self.pixmap.height())
        pixitem = QGraphicsPixmapItem(self.pixmap)
        self.img_view.centerOn(pixitem)

    def go_next_img(self):
        self.img_index = self.img_index + 1 if self.img_index < self.last_file else 0
        self.fname = self.filelist[self.img_index]
        self.reload_img()

    def go_prev_img(self):
        self.img_index = self.img_index - 1 if self.img_index else self.last_file
        self.fname = self.filelist[self.img_index]
        self.reload_img()

    def zoom_default(self):
        """Toggle best fit / original size loading."""
        if self.fit_win_act.isChecked():
            self.load_img = self.load_img_fit
            #self.create_dict()
            self.load_img()
        else:
            self.load_img = self.load_img_1to1
            #self.create_dict()
            self.load_img()

    def img_rotate(self, angle):
        self.pixmap = self.pixmap.transformed(QTransform().rotate(angle))
        self.load_img()

    def img_flip(self, x, y):
        self.pixmap = self.pixmap.transformed(QTransform().scale(x, y))
        self.load_img()

    def img_rotate_flip_horizontal(self):
        self.img_rotate(90)
        self.img_flip(-1, 1)

    def img_rotate_flip_vertical(self):
        self.img_rotate(90)
        self.img_flip(1, -1)

    def resize_image(self):
        dialog = editimage.ResizeDialog(self, self.pixmap.width(), self.pixmap.height())
        if dialog.exec_() == QDialog.Accepted:
            width = dialog.get_width.value()
            height = dialog.get_height.value()
            self.pixmap = self.pixmap.scaled(width, height, Qt.IgnoreAspectRatio,
                                             Qt.SmoothTransformation)
            self.save_img()

    def crop_image(self):
        self.img_view.setup_crop(self.pixmap.width(), self.pixmap.height())
        dialog = editimage.CropDialog(self, self.pixmap.width(), self.pixmap.height())
        if dialog.exec_() == QDialog.Accepted:
            coords = self.img_view.get_coords()
            self.pixmap = self.pixmap.copy(*coords)
            self.load_img()
        self.img_view.rubber_band.hide()

    def toggle_fs(self):
        if self.fulls_act.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()

    def toggle_slideshow(self):
        if self.ss_act.isChecked():
            self.showFullScreen()
            self.start_ss()
        else:
            self.toggle_fs()
            self.timer.stop()
            self.ss_timer.stop()

    def start_ss(self):
        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.update_img)
        self.timer.start(self.slide_delay * 1000)
        self.ss_timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.ss_timer.timeout.connect(self.update_img)
        self.ss_timer.start(60000)

    def update_img(self):
        if self.slides_next:
            self.go_next_img()
        else:
            self.fname = random.choice(self.filelist)
            self.reload_img()

    def set_slide_type(self):
        self.slides_next = self.ss_next_act.isChecked()

    def save_img(self):
        pass

    # # noinspection PyCallByClass,PyTypeChecker
    #     fname = QFileDialog.getSaveFileName(self, 'Save your image', self.fname)[0]
    #     if fname:
    #         if fname.lower().endswith(write_list()):
    #             # noinspection PyCallByClass,PyTypeChecker
    #             keep_exif = QMessageBox.question(self, 'Save exif data',
    #                                              'Do you want to save the picture metadata?', QMessageBox.Yes |
    #                                              QMessageBox.No, QMessageBox.Yes)
    #             if keep_exif == QMessageBox.Yes:
    #                 self.pixmap.save(fname, None, self.quality)
    #                 exif = GExiv2.Metadata(self.fname)
    #                 if exif:
    #                     saved_exif = GExiv2.Metadata(fname)
    #                     for tag in exif.get_exif_tags():
    #                         saved_exif[tag] = exif[tag]
    #                     saved_exif.set_orientation(GExiv2.Orientation.NORMAL)
    #                     saved_exif.save_file()
    #         else:
    #             # noinspection PyCallByClass,PyArgumentList,PyTypeChecker
    #             QMessageBox.information(self, 'Error', 'Cannot save {} images.'.format(fname.rsplit('.', 1)[1]))

    def print_img(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            if self.pixmap.width() > self.pixmap.height():
                self.pixmap = self.pixmap.transformed(QTransform().rotate(90))
            size = self.pixmap.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.pixmap.rect())
            painter.drawPixmap(0, 0, self.pixmap)

    def resizeEvent(self, event=None):
        # originally no check for valid image file resulted in errors
        if self.fit_win_act.isChecked() and len(self.fname):
            self.load_img()

    def get_props(self):
        """Get the properties of the current image."""
        image = QImage(self.fname)
        preferences.PropsDialog(self, self.fname.rsplit('/', 1)[1], image.width(), image.height())

    def help_page(self):
        preferences.HelpDialog(self)

    def about_cm(self):
        about_message = 'Version: 0.0.0\nAuthor: Dan Tyrrell\nwww.breager.com'
        # noinspection PyCallByClass,PyArgumentList,PyTypeChecker
        QMessageBox.about(self, 'About Mechaslide', about_message)


class ImageView(QGraphicsView):
    # todo: parent is named - why?
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.rubber_band = None

        self.go_prev_img = parent.go_prev_img
        self.go_next_img = parent.go_next_img

        pal = self.palette()
        pal.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(pal)
        self.setFrameShape(QFrame.NoFrame)

    def mousePressEvent(self, event):
        """Go to the next / previous image, or be able to drag the image with a hand."""
        if event.button() == Qt.LeftButton:
            x = event.x()
            if x < 100:
                self.go_prev_img()
            elif x > self.width() - 100:
                self.go_next_img()
            else:
                self.setDragMode(QGraphicsView.ScrollHandDrag)
        QGraphicsView.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.NoDrag)
        QGraphicsView.mouseReleaseEvent(self, event)

    def zoom(self, zoom_ratio):
        self.scale(zoom_ratio, zoom_ratio)

    def wheelEvent(self, event):
        zoom_ratio = 1.1
        if event.angleDelta().y() < 0:
            zoom_ratio = 1.0 / zoom_ratio
        self.scale(zoom_ratio, zoom_ratio)

    def setup_crop(self, width, height):
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        coords = self.mapFromScene(0, 0, width, height)
        self.rubber_band.setGeometry(QRect(coords.boundingRect()))
        self.rubber_band.show()

    def crop_draw(self, x, y, width, height):
        coords = self.mapFromScene(x, y, width, height)
        self.rubber_band.setGeometry(QRect(coords.boundingRect()))

    def get_coords(self):
        rect = self.rubber_band.geometry()
        size = self.mapToScene(rect).boundingRect()
        x = int(size.x())
        y = int(size.y())
        width = int(size.width())
        height = int(size.height())
        return x, y, width, height


class ImageViewer(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)
        self.win = None
        self.args = args

    def startup(self):
        if len(self.args) > 1:
            files = self.args[1:]
            self.open_files(files)
        else:
            self.open_win(None)

    def open_files(self, files):
        for fname in files:
            if fname.lower().endswith(read_list()):
                self.open_win(fname)

    def open_win(self, fname):
        self.win = MechascanSlideGUI()
        self.win.show()
        if fname:
            self.win.open_img(fname)
        else:
            self.win.open()


if __name__ == '__main__':
    import sys

    app = ImageViewer(sys.argv)
    app.startup()
    app.exec_()
