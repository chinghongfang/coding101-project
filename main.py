# coding=utf-8
import sys
### server library
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.websocket
from tornado.escape import json_decode

# for copy the link  to the clipboard
import pyperclip

import json

##for generating QRCode
import qrcode
# for storing the data from the client
import queue

# import ui files
from ui import Ui_MainWindow
from qrcode_ui import Ui_Dialog
# for the ui style
import qdarkstyle

# gui essential library
from PySide2.QtCore import QTimer, Qt, QPropertyAnimation, QPoint, QEasingCurve, Signal, QObject, QThread
from PySide2.QtGui import QFont, QPainter, QColor, QPainterPath, QFontMetrics, QPen, QBrush, QPixmap, QImage, QCursor
from PySide2.QtWidgets import QLabel, QApplication, QDialog, QMainWindow, QMessageBox, QDesktopWidget

# for translating localhost to public
from pyngrok import ngrok


# stroing the data when receiving
class store_info():
    def __init__(self, str, color):
        self.text = str
        self.color = color


# it is a global signal for hiding the finished danmaku
class MySignal(QObject):
    sig = Signal(str, str)


signal = MySignal()


class serverThread(QThread):
    def __init__(self, window):
        QThread.__init__(self)

        self.window = window
        self.application = tornado.web.Application(
            handlers=[(r"/", self.MainHandler),
                      (r"/sendBox.html", self.SendHandler),
                      (r"/room.html", self.RoomHandler),
                      (r"/response", self.ResponseHandler)])

    def run(self):
        http_server = tornado.httpserver.HTTPServer(self.application)
        http_server.listen(8888)
        self.ioloop = tornado.ioloop.IOLoop.instance()
        self.ioloop.start()

    def stop(self):
        self.ioloop.stop()
        self.quit()
        while not self.isFinished():
            pass

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.render('index.html')

        def post(self):
            pass

    class SendHandler(tornado.web.RequestHandler):
        def get(self):
            self.render('sendBox.html')

        def post(self):
            pass

    class RoomHandler(tornado.web.RequestHandler):
        def get(self):
            self.render('room.html')

        def post(self):
            pass

    class ResponseHandler(tornado.web.RequestHandler):

        def post(self):
            # data
            # import gloal signal
            global signal

            t = json_decode(self.request.body)  # type is dic
            string = t[u'text']
            color = t[u'color']
            if string == '':
                pass
            else:
                signal.sig.emit(string, color)


class scrollTextLabel(QLabel):
    deletesig = Signal()

    def __init__(self, text, Rect, scale, speed, line, color, bold, parent=None):
        super(scrollTextLabel, self).__init__(parent)

        if color == 'red':
            self.color = QColor(231, 0, 18, 255)  # red
        elif color == 'white':
            self.color = QColor(255, 255, 246, 255)  # white
        elif color == 'Grass':
            self.color = QColor(144, 195, 32, 255)  # Grass
        elif color == 'Blue':
            self.color = QColor(0, 160, 234, 255)  # Blue
        if bold:
            self.font = QFont("Helvetica", scale, QFont.Bold)  # 20 25 30 粗體
        else:
            self.font = QFont("Helvetica", scale)
        self.txt = text
        self.speed = speed  # between 50 ~ 120

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)  # 隱藏 FramelessWindow

        self.metrics = QFontMetrics(self.font)
        self.setFixedWidth(self.metrics.width(self.txt) + 10)
        self.setFixedHeight(self.metrics.height() + 5)

        # self.move(Rect.x() + Rect.width() * 0.97, Rect.y() + 50 * line)
        self.setFocusPolicy(Qt.NoFocus)
        self.hide()
        self.anim = QPropertyAnimation(self, 'pos')
        self.anim.setDuration(self.speed * 100)
        self.anim.setStartValue(QPoint(Rect.x() + Rect.width() * 0.95, Rect.y() + 50 * line))
        self.anim.setEndValue(QPoint(-self.width() + Rect.x(), Rect.y() + 50 * line))
        self.anim.setEasingCurve(QEasingCurve.Linear)

        self.show()
        self.repaint()
        self.anim.start()
        self.anim.finished.connect(self.sendslot)

    def sendslot(self):
        self.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.save()
        path = QPainterPath()

        painter.setFont(self.font)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen(QColor(0, 0, 0, 230))
        pen_width = 3
        pen.setWidth(pen_width)

        len = self.metrics.width(self.txt)
        w = self.width()
        px = (len - w) / 2
        if px < 0:
            px = -px
        py = (self.height() - self.metrics.height()) / 2 + self.metrics.ascent()
        if py < 0:
            py = -py

        path.addText(px + 2, py + 2, self.font, self.txt)
        painter.strokePath(path, pen)
        painter.drawPath(path)
        painter.fillPath(path, QBrush(self.color))
        painter.restore()


class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QImage(
            size, size, QImage.Format_RGB16)
        self._image.fill(Qt.white)

    def pixmap(self):
        return QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            Qt.black)


class MyPopup(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyPopup, self).__init__(parent)
        self.setupUi(self)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyside2()
        self.setStyleSheet(dark_stylesheet)
        self.setWindowTitle(" ")
        self.link = ''
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.WindowCloseButtonHint)  # 隱藏 FramelessWindow

        self.btn_copy.clicked.connect(self.copy_url)
        self.btn_ok.clicked.connect(self.hide)

    def copy_url(self):
        pyperclip.copy(self.link)
        self.messagebox = QMessageBox(self)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyside2()
        self.messagebox.setStyleSheet(dark_stylesheet)
        self.messagebox.setText("The link is copyed!!!")
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

    def setLink(self, str):
        self.link = str
        self.label_http.setText(str)
        self.generateQr()

    def generateQr(self):
        pixmap = qrcode.make(self.link, image_factory=Image).pixmap()
        self.label_QRcode.setScaledContents(True)
        self.label_QRcode.setPixmap(pixmap)
        self.update()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        global signal
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        self.window_list = []
        self.timer = QTimer()

        self.timer.timeout.connect(self.pop_msg)
        self.init()
        self.timer.start(1500)  # 2 seconds
        # self.popupMsg('hihi') # for testing the danmaku

    def change_transparent(self):
        self.setWindowOpacity(self.transparent_slider.value() / 100.0)

    def pop_msg(self):
        if not self.Msg_queue.empty():
            tmp = self.Msg_queue.get()
            str = tmp.text
            color = tmp.color
            self.popupMsg(str, color)
        else:
            pass

    def add_to_queue(self, str, color):
        tmp = store_info(str, color)
        self.Msg_queue.put(tmp)

    # generating the danmaku (產生彈幕）
    def popupMsg(self, str, color):
        color = color
        # 以白色來顯示
        bold = self
        self.textEdit.insertHtml("<p style='color:white;'>" + str + "</p>")
        self.textEdit.append('')
        w = scrollTextLabel(str, self.screenRect, self.scale, self.speed, self.line, color, self.isBold.isChecked())
        self.window_list.append(w)
        if self.line == 0:
            self.line = 1
        else:
            self.line = 0
        w.show()

    def init(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowCloseButtonHint)

        # default setting

        self.screen_num = 0  # default setting is main screen
        self.line = 0
        #######

        try:
            read_file = open("record.json", "r")
            dic_data = json.load(read_file)
            read_file.close()
            self.speed = dic_data['speed']
            self.scale = dic_data['scale']
            if self.scale == 20:
                self.checkBox_1.setCheckState(Qt.Checked)
            elif self.scale == 25:
                self.checkBox_2.setCheckState(Qt.Checked)
            elif self.scale == 30:
                self.checkBox_3.setCheckState(Qt.Checked)
            else:
                self.checkBox_2.setCheckState(Qt.Checked)

            self.transparent_slider.setValue(dic_data['transparent'])
            if dic_data['bold']:
                self.isBold.setChecked(Qt.Checked)

        except:
            self.checkBox_2.setCheckState(Qt.Checked)  # for scale middle (中)
            self.speed = 50  # between 50 ~ 120
            self.scale = 25  # 20 25 30
            self.transparent_slider.setValue(100)

        self.Speed_Slider.setValue(self.speed)

        self.is_save = True

        self.Qrcode_msg = MyPopup()
        self.Qrcode_msg.hide()

        self.serverThread = serverThread(self.window())
        self.serverThread.start()
        self.public_url = ngrok.connect(8888)
        self.Qrcode_msg.setLink(self.public_url)

        self.textEdit.setReadOnly(True)
        self.textEdit.insertHtml(
            "<p style='color:red;'>--------------------------Connected!--------------------------</p>")
        self.textEdit.append('')

        self.Msg_queue = queue.Queue()

        self.desktopWidget = QDesktopWidget(QApplication.desktop)
        self.screenRect = self.desktopWidget.screenGeometry(self.screen_num)

        screen = QDesktopWidget().screenGeometry(0)
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

        self.detect_screen()

        self.btn_detect_sreen.clicked.connect(self.detect_screen)
        # when the server gets the msg from the client, then pop up the danmaku
        # sig is the global signal
        # signal.sig.connect(self.popupMsg)
        signal.sig.connect(self.add_to_queue)
        self.onBindingUI()
        # self.setting_info()

    def save(self):
        if self.auto_save.isChecked():
            self.is_save = True
        else:
            self.is_save = False

    def write(self):
        fp = open("record.json", "w")

        data = {'speed': self.speed, 'scale': self.scale, 'bold': self.isBold.isChecked(),
                'transparent': self.transparent_slider.value()}
        ret = json.dumps(data)
        fp.write(ret)
        fp.close()

    def setting_info(self):
        print('speed ' + str(self.speed))
        print ('scale ' + str(self.scale))
        print ('bold ' + str(self.isBold.isChecked()))
        print ('transparent ' + str(self.transparent_slider.value()))

    def onBindingUI(self):
        ###init ui default setting and connect the signals with ui

        self.auto_save.setChecked(Qt.Checked)
        self.auto_save.clicked.connect(self.save)

        self.checkBox_1.stateChanged.connect(self.checkbox1_changed)
        self.checkBox_2.stateChanged.connect(self.checkbox2_changed)
        self.checkBox_3.stateChanged.connect(self.checkbox3_changed)
        self.Speed_Slider.valueChanged.connect(self.change_label_speed)
        self.Speed_Slider.setMaximum(120)
        self.Speed_Slider.setMinimum(50)
        self.btn_close.clicked.connect(self.close_the_app)

        self.transparent_slider.setTickInterval(100)
        self.transparent_slider.setMinimum(50)
        self.transparent_slider.setMaximum(100)

        self.transparent_slider.valueChanged.connect(self.change_transparent)
        #
        self.cbb_screen.currentIndexChanged.connect(self.set_screen_current_index)
        self.btn_qrcode.clicked.connect(self.qrcode_msg_show)
        self.btn_testing.clicked.connect(self.preview)
        ##美化 ui
        self.setWindowOpacity(self.transparent_slider.value() / 100.0)
        dark_stylesheet = qdarkstyle.load_stylesheet_pyside2()
        self.setStyleSheet(dark_stylesheet)
        self.setFixedSize(640, 600)

    def detect_screen(self):
        self.cbb_screen.clear()
        screen_count = self.desktopWidget.screenCount()
        for index in range(screen_count):
            self.cbb_screen.addItem('第' + str(index + 1) + "螢幕")

    def close_the_app(self):

        self.reply = QMessageBox.information(self,
                                             "User Interface",
                                             "Are you sure you want to quit?",
                                             QMessageBox.Yes | QMessageBox.No,
                                             QMessageBox.No)
        if self.reply == QMessageBox.Yes:
            if self.is_save:
                self.write()

            ngrok.disconnect(self.public_url)
            self.serverThread.stop()
            self.Qrcode_msg.close()
            self.close()

    def set_screen_current_index(self):
        self.screen_num = self.cbb_screen.currentIndex()
        self.screenRect = self.desktopWidget.screenGeometry(self.screen_num)

    def preview(self):
        self.w = scrollTextLabel('測試', self.screenRect, self.scale, self.speed, 0, 'Blue', self.isBold.isChecked())

    def qrcode_msg_show(self):
        size = self.Qrcode_msg.geometry()
        self.Qrcode_msg.move(self.screenRect.x() + (self.screenRect.width() - size.width()) / 2,
                             self.screenRect.y() + (self.screenRect.height() - size.height()) / 2)
        self.Qrcode_msg.show()

    def checkbox1_changed(self):
        if self.checkBox_1.checkState() == Qt.Checked:
            self.checkBox_2.setCheckState(Qt.Unchecked)
            self.checkBox_3.setCheckState(Qt.Unchecked)
        self.set_checkbox_val()

    def checkbox2_changed(self):
        if self.checkBox_2.checkState() == Qt.Checked:
            self.checkBox_1.setCheckState(Qt.Unchecked)
            self.checkBox_3.setCheckState(Qt.Unchecked)
        self.set_checkbox_val()

    def checkbox3_changed(self):
        if self.checkBox_3.checkState() == Qt.Checked:
            self.checkBox_1.setCheckState(Qt.Unchecked)
            self.checkBox_2.setCheckState(Qt.Unchecked)
        self.set_checkbox_val()

    def set_checkbox_val(self):
        if self.checkBox_1.checkState() == Qt.Checked:
            self.scale = 30  # 大
        if self.checkBox_2.checkState() == Qt.Checked:
            self.scale = 25  # 中
        if self.checkBox_3.checkState() == Qt.Checked:
            self.scale = 20  # 小

    def change_label_speed(self):
        self.speed = self.Speed_Slider.value()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
