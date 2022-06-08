import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from zaber_motion import Library,Units
from zaber_motion.binary import Connection, BinarySettings
Library.enable_device_db_store()
# https://www.riverbankcomputing.com/static/Docs/PyQt6/sip-classes.html
# https://www.zaber.com/software/docs/motion-library/binary/references/python_binary/

class GUI_main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.show()
        connection = Connection.open_serial_port("/dev/tty.usbserial-A403L6SM")
        self.zaber = connection.detect_devices()[0]
        self.zaber.settings.set(BinarySettings.MICROSTEP_RESOLUTION,128)

        self.setWindowTitle("Zaber Controller")

        main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()

        self.jog_group = QtWidgets.QGroupBox("Jogging")
        self.jog_layout = QtWidgets.QGridLayout()

        home_btn = QtWidgets.QPushButton("Home")
        home_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        home_btn.clicked.connect(self.go_home)

        up_btn = QtWidgets.QPushButton("Up")
        up_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        up_btn.clicked.connect(self.move_up)

        down_btn = QtWidgets.QPushButton("Down")
        down_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        down_btn.clicked.connect(self.move_down)

        self.a_radio = QtWidgets.QRadioButton("0.1 mm")
        self.b_radio = QtWidgets.QRadioButton("0.5 mm")
        self.c_radio = QtWidgets.QRadioButton("1 mm")
        self.c_radio.setChecked(True)
        self.d_radio = QtWidgets.QRadioButton("2 mm")
        self.e_radio = QtWidgets.QRadioButton()

        self.a_radio.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.b_radio.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.c_radio.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.d_radio.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.e_radio.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
  
        self.custom_step = QtWidgets.QDoubleSpinBox()
        self.custom_step.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.custom_step.setSuffix(" mm")
        self.custom_step.setSingleStep(.005)
        self.custom_step.setRange(0,50)
        self.custom_step.setDecimals(3)
        self.custom_step.setValue(0)

        self.jog_layout.addWidget(home_btn,0,2)
        self.jog_layout.addWidget(up_btn,1,2)
        self.jog_layout.addWidget(down_btn,2,2)
        self.jog_layout.addWidget(self.a_radio,0,0,1,2)
        self.jog_layout.addWidget(self.b_radio,1,0,1,2)
        self.jog_layout.addWidget(self.c_radio,2,0,1,2)
        self.jog_layout.addWidget(self.d_radio,3,0,1,2)
        self.jog_layout.addWidget(self.e_radio,4,0)
        self.jog_layout.addWidget(self.custom_step,4,1)

        self.jog_group.setLayout(self.jog_layout)
        #################################

        self.retract_group = QtWidgets.QGroupBox("Etching")
        self.retract_layout = QtWidgets.QGridLayout()

        retract_btn = QtWidgets.QPushButton("Retract")
        retract_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        retract_btn.clicked.connect(self.start_move)

        stop_btn = QtWidgets.QPushButton("Stop")
        stop_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        stop_btn.clicked.connect(self.stop)

        position_btn = QtWidgets.QPushButton("Get Position")
        position_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        position_btn.clicked.connect(self.print_pos)

        self.retract_rate = QtWidgets.QSpinBox()
        self.retract_rate.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.retract_rate.setSuffix(" µm/minute")
        self.retract_rate.setSingleStep(1)
        self.retract_rate.setRange(10,250)
        self.retract_rate.setValue(10)

        self.retract_layout.addWidget(self.retract_rate)
        self.retract_layout.addWidget(retract_btn)
        self.retract_layout.addWidget(stop_btn)
        self.retract_layout.addWidget(position_btn)
        self.retract_layout.setRowStretch(4,1)

        self.retract_group.setLayout(self.retract_layout)
        #################################
        
        self.log = QtWidgets.QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.log.setFont(QtGui.QFont('Courier New',12))

        #################################

        self.main_layout.addWidget(self.jog_group,0,0)
        self.main_layout.addWidget(self.retract_group,0,1)
        self.main_layout.addWidget(self.log,1,0,1,2)
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)
        self.setFixedSize(self.main_layout.sizeHint())

        # Variables
        self.timer = QtCore.QTimer()  # set up your QTimer
        self.timer.timeout.connect(self.alarm)  # connect it to your update function

        self.go_home()

    def go_home(self):
        self.stop_and_clear()
        self.position = self.zaber.home()
        self.log_msg(f"homed\t{self.zaber.get_position(Units.LENGTH_MILLIMETRES):.3f}")

    def move_up(self):
        self.stop_and_clear()
        distance = 0
        if self.a_radio.isChecked():
            distance = 0.1
        elif self.b_radio.isChecked():
            distance = .5
        elif self.c_radio.isChecked():
            distance = 1
        elif self.d_radio.isChecked():
            distance = 2
        elif self.e_radio.isChecked():
            distance = self.custom_step.value()

        try:
            self.zaber.move_relative(-distance, Units.LENGTH_MILLIMETRES)
            self.log_msg(f"+{distance:.3f}\t-{self.zaber.get_position(Units.LENGTH_MILLIMETRES):.3f}")
        except:
            self.log_msg("unable to move")

    def move_down(self):
        self.stop_and_clear()
        distance = 0
        if self.a_radio.isChecked():
            distance = 0.1
        elif self.b_radio.isChecked():
            distance = .5
        elif self.c_radio.isChecked():
            distance = 1
        elif self.d_radio.isChecked():
            distance = 2
        elif self.e_radio.isChecked():
            distance = self.custom_step.value()

        try:
            self.zaber.move_relative(distance, Units.LENGTH_MILLIMETRES)
            self.log_msg(f"-{distance:.3f}\t-{self.zaber.get_position(Units.LENGTH_MILLIMETRES):.3f}")
        except:
            self.log_msg("unable to move")

    def log_msg(self,msg):
        datetime = QtCore.QDateTime.currentDateTime()
        self.log.insertPlainText(f"[{datetime.toString('hh:mm:ss')}]\t{msg}\n")
        self.log.moveCursor(QtGui.QTextCursor.MoveOperation.End)

    def stop_and_clear(self):
        self.timer.stop()
        self.retract_rate.clearFocus()
        self.custom_step.clearFocus()

    
    def start_move(self):
        self.stop_and_clear()
        print("move: ", new_vel := self.retract_rate.value()*1000/60)
        try:
            if new_vel<291:
                delay = 5000/new_vel
                self.timer.start(int(delay)*1000)
                print("delay: ", delay,int(delay))
            else:
                self.zaber.move_velocity(-new_vel, Units.VELOCITY_NANOMETRES_PER_SECOND)
            self.log_msg("moving")
        except:
            self.log_msg("unable to move")
    
    def alarm(self):
        self.zaber.move_relative(-0.005, Units.LENGTH_MILLIMETRES)
        print('moving!')

    def stop(self):
        self.zaber.stop(Units.LENGTH_MILLIMETRES)
        self.stop_and_clear()
        print('stopped')
    
    def print_pos(self):
        self.log_msg(f"\t-{self.zaber.get_position(Units.LENGTH_MILLIMETRES):.3f}")

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key.Key_Up:
            self.move_up()
        if key == QtCore.Qt.Key.Key_Down:
            self.move_down()
        if key == QtCore.Qt.Key.Key_H:
            self.go_home()
    
    def closeEvent(self,_):
        self.zaber.stop()

app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
gui_main = GUI_main()
sys.exit(app.exec())
