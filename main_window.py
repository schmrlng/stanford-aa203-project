from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as MplFigCanvas
import matplotlib.figure

from fsm_state import FsmState

class XyPlot(MplFigCanvas):
    def __init__(self, title, width, height, dpi=100):
        fig = matplotlib.figure.Figure(figsize=(width,height), dpi=dpi)
        self.distance_axes = fig.subplots()
        self.distance_axes.set_xlabel('t')
        self.distance_axes.set_title(title)
        self.angle_axes = self.distance_axes.twinx()
        super().__init__(fig)
    # /__init__()
# /class XyPlot

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, width, height, robot):
        super(MainWindow, self).__init__()
        self.robot = robot
        self.setupUi(width, height)
        self.setupAnimation()
        self.resize(width+800, height)
        self.updateGeometry()
    # /__init__()

    def setupUi(self, width, height):
        hlayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel()
        robot_canvas = QtGui.QPixmap(width, height)
        self.label.setPixmap(robot_canvas)
        hlayout.addWidget(self.label)
        plots_vlayout = QtWidgets.QVBoxLayout()
        self.state_plot = XyPlot('State', 300, self.label.height()//2)
        plots_vlayout.addWidget(self.state_plot)
        self.control_plot = XyPlot('Control', 300, self.label.height()//2)
        plots_vlayout.addWidget(self.control_plot)
        hlayout.addItem(plots_vlayout)
        
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(hlayout)
        self.setCentralWidget(central_widget)
    # /setupUi()

    def setupAnimation(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.render)
        self.counter = 0
        self.timer.start(25) # ms
    # /setupAnimation()

    def render(self):
        qpainter = QtGui.QPainter(self.label.pixmap())

        # background
        bg_brush = QtGui.QBrush()
        bg_brush.setColor(QtCore.Qt.white)
        bg_brush.setStyle(QtCore.Qt.SolidPattern)
        qpainter.setBrush(bg_brush)
        qpainter.drawRect(0,0, self.label.width(), self.label.height())

        # foreground
        if self.robot.fsm_state == FsmState.IDLE:
            self.robot.drive()
        # /if

        # screen coords (top left, downwards) -> math coords (bottom left, upwards)
        qpainter.translate(0, self.label.height()-1)
        qpainter.scale(1, -1)

        self.robot.render(qpainter)

        qpainter.end()
        self.update()
    # /render()

# /class MainWindow
