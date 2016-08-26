# Filter by Size 
# Tested on 3Ds Max 2017
# Yvo von Berg / Technical Artist
# 2016, yvovonberg.nl

from PySide.QtCore import *
from PySide.QtGui import *

class MainWindow(QDialog):
    def __init__(self, MainFilter):  
        MaxPlus.CUI.DisableAccelerators()
        QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)

        self.setWindowTitle('FilterBySize')
        self.setModal(False)

        self.setFixedHeight(200)
        self.setFixedWidth(210)

        # spinboxes
        self.sizeX_input = QDoubleSpinBox(self)
        self.sizeX_input.setGeometry(0, 50, 70, 50)
        self.sizeX_input.setMaximum(1000)

        self.sizeY_input = QDoubleSpinBox(self)
        self.sizeY_input.setGeometry(70, 50, 70, 50)
        self.sizeY_input.setMaximum(1000)

        self.sizeZ_input = QDoubleSpinBox(self)
        self.sizeZ_input.setGeometry(140, 50, 70, 50)
        self.sizeZ_input.setMaximum(1000)

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

        sel = list(MaxPlus.SelectionManager.Nodes)
        if len(sel) > 0:
            x,y,z = self.getDimensions(sel[0])

            UI.sizeX_input.setValue(x)
            UI.sizeY_input.setValue(y)
            UI.sizeZ_input.setValue(z)
        else:
            print 'select something'

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

    def GetWorldBoundBox(self, node):
        '''
             Gets world boundingbox of node
        '''
        vm = MaxPlus.ViewportManager
        av = vm.GetActiveViewport()

        return node.GetBaseObject().GetWorldBoundBox(node, av)

    def getDimensions(self, iNode):

        bbox = self.GetWorldBoundBox(iNode)
        # [minX, minY, minZ, maxX, maxY, maxZ]
        measureX = bbox.Max.X - bbox.Min.X
        measureY = bbox.Max.Y - bbox.Min.Y
        measureZ = bbox.Max.Z - bbox.Min.Z

        return measureX, measureY, measureZ

    def doFilter(self):

        
        # get selection
        sel = MaxPlus.SelectionManager.Nodes

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

            if (xGreater and (x > userX)) or (not xGreater and (x < userX)) and \
            (yGreater and (y > userY)) or (not yGreater and (y < userY)) and \
            (zGreater and (z > userZ)) or (not zGreater and (z < userZ)):
                self.filteredObjects.append(obj)                

        objCount = len(self.filteredObjects)

        if objCount > 0:
            print 'Found ' + str(objCount)
            self.addToLayer(self.filteredObjects)
        else:
            print 'no objects found'


    def addToLayer(self, allObjects):
        # create new layer
        layer = MaxPlus.LayerManager.CreateLayer("Filterrr_layer_")
        for obj in allObjects:
            layer.AddToLayer(obj)

if __name__ == "__main__":
    filterClass = MainFilter()
    UI = MainWindow(filterClass)
    UI.show()
