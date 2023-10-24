import maya.cmds as cmds
#import maya.mel as mel

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

class HM_AnimTools(MayaQWidgetDockableMixin, QWidget):
    title = 'HM_AnimTools'

    def __init__(self, parent = None):
        super(HM_AnimTools, self).__init__(parent)

        self.setObjectName(self.title)
        self.setWindowTitle(self.title)

        self.centralwidget = QWidget(self)
        self.lSpacer = QSpacerItem(self)
        self.cLayout = QHBoxLayout(self)

        self.playButton = QPushButton(self)
        self.revButton = QPushButton(self)

        self.playButton.setIcon(QIcon(':/timeplay.png'))
        self.revButton.setIcon(QIcon(':/timerev.png'))
        
        self.rSpacer = QSpacerItem(self)
'''
class HM_AnimTools(MayaQWidgetDockableMixin, QWidget):
    title = 'HM_AnimTools'

    def __init__(self, parent = None):
        super(HM_AnimTools, self).__init__(parent)

        self.setObjectName(self.title)
        self.setWindowTitle(self.title)

        self.centralwidget = QWidget(self)
        #self.pLayout = QHBoxLayout(self)
        #self.lLayout = QHBoxLayout(self)
        self.cLayout = QHBoxLayout(self)
        #self.rLayout = QHBoxLayout(self)

        #self.pLayout.setParent(self.centralwidget)
        #self.lLayout.setParent(self.pLayout)
        self.cLayout.setParent(self.centralwidget)
        #self.rLayout.setParent(self.pLayout)

        self.playButton = QPushButton(self)
        self.revButton = QPushButton(self)

        #self.playButton.setGeometry(20, 0, 20, 20)
        #self.revButton.setGeometry(0, 0, 20, 20)

        #self.playButton.setParent(self.cLayout)
        #self.revButton.setParent(self.cLayout)

        self.playButton.setIcon(QIcon(':/timeplay.png'))
        self.revButton.setIcon(QIcon(':/timerev.png'))
'''
custom_mixin_widget = None


def show_ui(restore=False):
    global custom_mixin_widget

    if not custom_mixin_widget:
        custom_mixin_widget = HM_AnimTools()
        custom_mixin_widget.setObjectName('HM_AnimTools')

    if restore:
        restored_control = omui.MQtUtil.getCurrentParent()
        mixin_ptr = omui.MQtUtil.findControl(custom_mixin_widget.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(int(mixin_ptr), int(restored_control))
    else:
        workspace_control_name = custom_mixin_widget.objectName() + 'WorkspaceControl'
        if cmds.workspaceControl(workspace_control_name, exists=True):
            cmds.deleteUI(workspace_control_name)

        _ui_script = f'import {__name__}; {__name__}.show_ui(restore=True)'
        custom_mixin_widget.show(dockable=True, uiScript=_ui_script)

    return custom_mixin_widget


def main():
    show_ui()

if __name__ == "__main__": 
    main()