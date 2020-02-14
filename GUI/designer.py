# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """
        Simple Window with a table and two buttons to add and remove
        columns
    """

    def setupUi(self, MainWindow):
        """
        UI
        """
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(979, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.add_btn = QtWidgets.QPushButton(self.centralwidget)
        self.add_btn.setGeometry(QtCore.QRect(790, 120, 93, 28))
        self.add_btn.setObjectName("add_btn")
        self.add_btn.clicked.connect(self._add_to_table)
        self.remove_btn = QtWidgets.QPushButton(self.centralwidget)
        self.remove_btn.setGeometry(QtCore.QRect(780, 170, 111, 28))
        self.remove_btn.setObjectName("remove_btn")
        self.remove_btn.clicked.connect(self._remove_table)
        # self.listView = QtWidgets.QListView(self.centralwidget)
        # self.listView.setGeometry(QtCore.QRect(10, 10, 481, 661))
        # self.listView.setObjectName("listView")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 10, 550, 610))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(560, 100, 191, 191))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(1, 1, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.name = QtWidgets.QLabel("name")
        self.age = QtWidgets.QLabel("age")
        self.job = QtWidgets.QLabel("job")
        self.nameLabel = QtWidgets.QLineEdit()
        self.ageLabel = QtWidgets.QLineEdit()
        self.jobLabel = QtWidgets.QLineEdit()
        self.formLayout.addRow(self.name, self.nameLabel)
        self.formLayout.addRow(self.age, self.ageLabel)
        self.formLayout.addRow(self.job, self.jobLabel)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 979, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _remove_table(self):
        """
        removes the first row from the table
        :return:
        """
        self.tableWidget.removeRow(0)

    def _add_to_table(self):
        """
        create a row and add fields to it
        :return:
        """
        name = self.nameLabel.text()
        age = self.ageLabel.text()
        job = self.jobLabel.text()
        table = self.tableWidget
        rowPosition = table.rowCount()
        table.insertRow(rowPosition)
        table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(name))
        table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(age))
        table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(job))
        print(f"added name {name}")
        print(f"added age {age}")
        print(f"added job {job}")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add_btn.setText(_translate("MainWindow", "add to list"))
        self.remove_btn.setText(_translate("MainWindow", "remove from list"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
