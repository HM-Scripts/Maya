import maya.cmds as cmds
import maya.mel as mel

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

class HM_AnimTools(MayaQWidgetDockableMixin, QMainWindow):
    title = 'HM_AnimTools'

    def __init__(self, parent = None):
        super(HM_AnimTools, self).__init__(parent)

        self.setObjectName(self.title)
        self.setWindowTitle(self.title)

        self.playButton = QPushButton(self)
        self.revButton = QPushButton(self)
        self.nextButton = QPushButton(self)
        self.prevButton = QPushButton(self)
        self.startButton = QPushButton(self)
        self.endButton = QPushButton(self)
        self.fwdButton = QPushButton(self)
        self.rewButton = QPushButton(self)

        self.playButton.setIcon(QIcon(':/timeplay.png'))
        self.revButton.setIcon(QIcon(':/timerev.png'))
        self.nextButton.setIcon(QIcon(':/timenext.png'))
        self.prevButton.setIcon(QIcon(':/timeprev.png'))
        self.startButton.setIcon(QIcon(':/timeend.png'))
        self.endButton.setIcon(QIcon(':/timestart.png'))
        self.fwdButton.setIcon(QIcon(':/timefwd.png'))
        self.rewButton.setIcon(QIcon(':/timerew.png'))

        self.playButton.setGeometry(300, 20, 60, 60)
        self.revButton.setGeometry(230, 20, 60, 60)
        self.nextButton.setGeometry(370, 20, 60, 60)
        self.prevButton.setGeometry(160, 20, 60, 60)
        self.startButton.setGeometry(90, 20, 60, 60)
        self.endButton.setGeometry(440, 20, 60, 60)
        self.fwdButton.setGeometry(510, 20, 60, 60)
        self.rewButton.setGeometry(20, 20, 60, 60)

        self.playButton.clicked.connect(self.pushed_play)
    
    def pushed_play(self):
        mel.eval('playButtonForward;')


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