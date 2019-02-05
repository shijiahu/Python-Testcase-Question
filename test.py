from PyQt5 import QtCore, QtGui, QtWidgets
import sys, re
import numpy as np
from my_ui import Ui_MainWindow


import matplotlib
matplotlib.use("Qt5Agg")  # declare using QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class Mainwindow(QtWidgets.QMainWindow,Ui_MainWindow):

    def __init__(self):
        super(Mainwindow, self).__init__()
        # initialize class Ui_MainWindow(in my_ui.py)
        self.setupUi(self)
        self.setWindowTitle("Testcases")

        self.pushButton_2.clicked.connect(self.passed)
        self.pushButton_3.clicked.connect(self.failed)
        self.pushButton.clicked.connect(self.show_chart)

    # show passed logs in listwidget
    def passed(self):
        self.listWidget.clear()
        with open('tempest.txt') as fh:
            test_file = fh.read()
            passed = re.findall(r'\{0\}.*\.\.\. ok', test_file)
        for x in passed:
            self.listWidget.addItem(x)

    # show failed logs in listwidget
    def failed(self):
        self.listWidget.clear()
        with open('tempest.txt') as fh:
            test_file = fh.read()
            failed = re.findall(r'\{0\}.*\.\.\. FAILED', test_file)
        # num_of_passed = len(passed)
        # num_of_failed = len(failed)
        for x in failed:
            self.listWidget.addItem(x)

    def show_chart(self):
        # FigureCanvas
        dr = Figure_Canvas()
        dr.test()  # draw chart
        graphicscene = QtWidgets.QGraphicsScene()  # create QGraphicsScene，cause FigureCanvas cannot be directly put in graphicview
        graphicscene.addWidget(dr)  
        self.graphicsView.setScene(graphicscene)  # put QGraphicsScene into QGraphicsView 


class Figure_Canvas(FigureCanvas):                                         

    def __init__(self, parent=None, width=4, height=3, dpi=85):
        fig = Figure(figsize=(width, height), dpi=85)  

        FigureCanvas.__init__(self, fig) 
        self.setParent(parent)

        self.axes = fig.add_subplot(111) 

    def test(self):
        # get data
        with open('tempest.txt') as fh:
            test_file = fh.read()
            passed = re.findall(r'\{0\}.*\.\.\. ok', test_file)
            failed = re.findall(r'\{0\}.*\.\.\. FAILED', test_file)
        num_of_passed = len(passed)
        num_of_failed = len(failed)


        name_list = ['Passed','Failed']
        num_list = [num_of_passed, num_of_failed]
        x = list(range(len(num_list)))
        total_width, n = 0.8, 2
        width = total_width / n

        # for legend
        color = ['g', 'r']
        patches = [ mpatches.Patch(color=color[i], label="{:s}".format(name_list[i]) ) for i in range(len(color)) ] 
        # ax = plt.gca()
        # box = ax.get_position()
        # ax.set_position([box.x0, box.y0, box.width , box.height* 0.8])
        # ax.legend( handles = patches, loc = 'upper right')
        self.axes.legend( handles = patches, loc = 'upper right')

        # draw label
        for a,b in zip(x,num_list):
            self.axes.text(a, b + 0.05, '%.0f' %b, ha = 'center', va = 'bottom', fontsize=7)

        self.axes.set_title('Testcases')
        self.axes.bar(x, num_list, width = width, tick_label = name_list, color = color)
        



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win=Mainwindow()  
    win.show()
    sys.exit(app.exec_()) 
