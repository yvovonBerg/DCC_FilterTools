from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2 import QtGui
import pymel.core as pm
import math

import logging
logger = logging.getLogger(__name__)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)


class MainWindow(QDialog):
    def __init__(self, MainFilter):  
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)

        self.setWindowTitle('FilterBySize')
        self.setModal(False)

        self.setFixedHeight(200)
        self.setFixedWidth(210)

        # spinboxes
        self.sizeX_input = QDoubleSpinBox(self)
        self.sizeX_input.setGeometry(0, 50, 70, 50)

        self.sizeY_input = QDoubleSpinBox(self)
        self.sizeY_input.setGeometry(70, 50, 70, 50)

        self.sizeZ_input = QDoubleSpinBox(self)
        self.sizeZ_input.setGeometry(140, 50, 70, 50)

        # greater than 
        self.xGreater_input = QComboBox(self)
        self.xGreater_input.addItems(['<','>'])
        self.xGreater_input.setGeometry(0, 100, 70, 50)

        self.yGreater_input = QComboBox(self)
        self.yGreater_input.addItems(['<','>'])
        self.yGreater_input.setGeometry(70, 100, 70, 50)

        self.zGreater_input = QComboBox(self)
        self.zGreater_input.addItems(['<','>'])
        self.zGreater_input.setGeometry(140, 100, 70, 50)

        # get measure button
        measure_btn = QPushButton('Measure selected', self)
        measure_btn.setGeometry(0,0,210,50)
        measure_btn.clicked.connect( MainFilter.measureInput )

        # filter button
        filter_btn = QPushButton('Filterrr!!', self)
        filter_btn.setGeometry(0, 150, 210, 50)
        filter_btn.clicked.connect( MainFilter.setValues )

class MainFilter(object):

    def __init__(self):

        self.filteredObjects = []

    def getGreater(self, combobox):
        if combobox.currentText() == '<':
            value = False
        else:
            value = True

        return value

    def measureInput(self):

        sel = pm.selected()
        if len(sel) > 0:
            x,y,z = self.getDimensions(sel[0])

            UI.sizeX_input.setValue(x)
            UI.sizeY_input.setValue(y)
            UI.sizeZ_input.setValue(z)
        else:
            logger.warning('select something')

    def setValues(self):

        # clear previous filteredObjects
        self.filteredObjects = []

        # call filter function
        self.doFilter()

    def getXYZvalues(self):
        # custom size values
        xValue = UI.sizeX_input.value()
        yValue = UI.sizeY_input.value()
        zValue = UI.sizeZ_input.value()

        return xValue, yValue, zValue

    def getDimensions(self, mesh):
        # [minX, minY, minZ, maxX, maxY, maxZ]
        bbox = pm.exactWorldBoundingBox(mesh)

        measureX = bbox[3] - bbox[0]
        measureY = bbox[4] - bbox[1]
        measureZ = bbox[5] - bbox[2]

        return measureX, measureY, measureZ

    def doFilter(self):
        # get selection
        sel =  pm.selected()

        # get the user xyz values
        userX, userY, userZ = self.getXYZvalues()

        # get the greater value from spinbox as boolean
        xGreater = self.getGreater( UI.xGreater_input )
        yGreater = self.getGreater( UI.yGreater_input )
        zGreater = self.getGreater( UI.zGreater_input )

        # loop through every selected object
        for obj in sel:
            # get dimensions for current object
            x,y,z = self.getDimensions(obj)
            
            if (xGreater and yGreater and zGreater) and ((x > userX) and (y > userY) and (z > userZ)) or \
            ((not xGreater and not yGreater and not zGreater) and (x < userX) and (y < userY) and (z < userZ)):
                self.filteredObjects.append(obj)

        objCount = len(self.filteredObjects)

        if objCount > 0:
            logger.info('Found ' + str(objCount))
            self.addToLayer(self.filteredObjects)
        else:
            logger.warning('No objects found!')


    def addToLayer(self, allObjects):
        # create new display layer
        layer = pm.createDisplayLayer( empty=True, name='Filterrr_layer_' )
        for obj in allObjects:
            pm.editDisplayLayerMembers( layer, obj )


if __name__ == "__main__":
    filterClass = MainFilter()
    UI = MainWindow(filterClass)
    UI.show()
