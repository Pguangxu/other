# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Administrator\eric_projects\ControlPanelPosStop.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import multiprocessing

from Record import Record
from Ui_StopDialog import Ui_StopDialog
class Ui_ControlPanelPosStop(QtWidgets.QWidget):
    def __init__(self,msg_quenen, record):
        super().__init__()
        self.__msg_quenen=msg_quenen
        self.__record=record
        self.__ui_stopdialog= Ui_StopDialog(self.__msg_quenen,self.__record)
        self.setupUi()
        self.pushButton_stop.clicked.connect(self.stop_heat)
    def __second_to_time(self, i_seconds):
        m, s = divmod(i_seconds, 60)
        h, m = divmod(m, 60) 
        return ("%02d:%02d:%02d" % (h, m, s))
    def stop_heat(self):
        #i_box_number,i_layer_number,i_pos_number, str_state, str_msg
        self.__ui_stopdialog.show()
    def setupUi(self):
        self.setFixedSize(200,200)
        
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setWindowTitle("")
        self.setWindowOpacity(1.0)
        
        
        self.main_widget = QtWidgets.QWidget(self)
        self.main_widget.setFixedSize(200,200)
        self.main_widget.setStyleSheet("QWidget{background-color:rgba(195,214,155,255);"                               
                                "border-top-left-radius:10px;"
                                "border-bottom-left-radius:10px;"
                                "border-top-right-radius:10px;"
                                "border-bottom-right-radius:10px;"
                                "border-bottom:4px solid gray;"
                                "border-top:1px solid gray;  "
                                "border-right:2px solid gray;  "
                                "border-left:1px solid gray;}" 
                                "QLabel{border:none;color:gray;}")
        self.setObjectName("self")

        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        self.main_widget.setFont(font)
        self.main_widget.setWindowTitle("")
        self.main_widget.setWindowOpacity(1.0)
        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_duration_node = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        self.label_duration_node.setFont(font)
        self.label_duration_node.setObjectName("label_duration_node")
        self.gridLayout.addWidget(self.label_duration_node, 0, 0, 1, 2)
        self.label_barcode_node = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        self.label_barcode_node.setFont(font)
        self.label_barcode_node.setObjectName("label_barcode_node")
        self.gridLayout.addWidget(self.label_barcode_node, 1, 0, 1, 2)
        self.label_countback_node = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        self.label_countback_node.setFont(font)
        self.label_countback_node.setObjectName("label_countback_node")
        self.gridLayout.addWidget(self.label_countback_node, 2, 0, 1, 1)
        self.label_countback = QtWidgets.QLabel(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_countback.sizePolicy().hasHeightForWidth())
        self.label_countback.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Dutch801 XBd BT")
        font.setPointSize(16)
        self.label_countback.setFont(font)
        self.label_countback.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_countback.setObjectName("label_countback")
        self.gridLayout.addWidget(self.label_countback, 2, 1, 1, 1)
        self.label_countback_node_2 = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑 Light")
        font.setPointSize(12)
        self.label_countback_node_2.setFont(font)
        self.label_countback_node_2.setText("")
        self.label_countback_node_2.setObjectName("label_countback_node_2")
        self.gridLayout.addWidget(self.label_countback_node_2, 3, 0, 1, 1)
        self.pushButton_stop = QtWidgets.QPushButton(self.main_widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(128)
        sizePolicy.setHeightForWidth(self.pushButton_stop.sizePolicy().hasHeightForWidth())
        self.pushButton_stop.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_stop.setFont(font)
        self.pushButton_stop.hide()
        self.pushButton_stop.setFlat(False)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.gridLayout.addWidget(self.pushButton_stop, 3, 0, 1, 2)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main_widget)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        str_duration=self.__second_to_time( self.__record.i_duration )
        self.label_duration_node.setText(_translate("self.main_widget", "定时时长："+str_duration))
        self.label_barcode_node.setText(_translate("self.main_widget", "条      码："+" "*0+str(self.__record.str_barcode)))
        self.label_countback_node.setText(_translate("self.main_widget", "剩余时间："))
        str_countback=self.__second_to_time( self.__record. i_duration)
        self.label_countback.setText(_translate("self.main_widget", str_countback))
        self.pushButton_stop.setText(_translate("self.main_widget", "停止烘烤"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    msg_queue= multiprocessing.Queue(20)
    record=Record(0,1,1,'sd123456789')
    ui1 = Ui_ControlPanelPosStop(msg_queue, record)
    ui1.show()
    sys.exit(app.exec_())

