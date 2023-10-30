import maya.cmds as cmds
import maya.mel as mel

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

tool_name = 'HM_AnimTools'
custom_mixin_widget = None
scriptJob_id_anim = None
win = None

class HM_AnimTools(MayaQWidgetDockableMixin, QMainWindow):
    title = tool_name

    def __init__(self, parent = None):
        super(HM_AnimTools, self).__init__(parent)
        global win
        win = self

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

        self.copyButton = QPushButton(self)
        self.pasteButton = QPushButton(self)
        self.cutButton = QPushButton(self)
        self.deleteButton = QPushButton(self)

        self.playButton.setGeometry(300, 20, 60, 60)
        self.revButton.setGeometry(230, 20, 60, 60)
        self.nextButton.setGeometry(370, 20, 60, 60)
        self.prevButton.setGeometry(160, 20, 60, 60)
        self.startButton.setGeometry(90, 20, 60, 60)
        self.endButton.setGeometry(440, 20, 60, 60)
        self.fwdButton.setGeometry(510, 20, 60, 60)
        self.rewButton.setGeometry(20, 20, 60, 60)

        self.copyButton.setGeometry(160, 100, 130, 40)
        self.pasteButton.setGeometry(300, 100, 130, 40)
        self.cutButton.setGeometry(20, 100, 130, 40)
        self.deleteButton.setGeometry(440, 100, 130, 40)

        self.playButton.setIcon(QIcon(':/timeplay.png'))
        self.revButton.setIcon(QIcon(':/timerev.png'))
        self.nextButton.setIcon(QIcon(':/timenext.png'))
        self.prevButton.setIcon(QIcon(':/timeprev.png'))
        self.startButton.setIcon(QIcon(':/timeend.png'))
        self.endButton.setIcon(QIcon(':/timestart.png'))
        self.fwdButton.setIcon(QIcon(':/timefwd.png'))
        self.rewButton.setIcon(QIcon(':/timerew.png'))

        self.copyButton.setText('Copy')
        self.pasteButton.setText('Paste')
        self.cutButton.setText('Cut')
        self.deleteButton.setText('Delete')

        self.playButton.clicked.connect(self.push_play)
        self.copyButton.clicked.connect(self.push_copy)
        self.pasteButton.clicked.connect(self.push_paste)
        self.cutButton.clicked.connect(self.push_cut)
        self.deleteButton.clicked.connect(self.push_delete)
    
    def push_play(self):
        #mel.eval('playButtonForward;')
        is_anim_playing = cmds.play(q = True, state = True)
    
        if is_anim_playing:
            cmds.play(state = False)
        else:
            cmds.play(forward = True, state = True)
            self.playButton.setIcon(QIcon(':/timestop.png'))
    
    def push_copy(self):
        mel.eval('timeSliderCopyKey;')

    def push_paste(self):
        mel.eval('timeSliderPasteKey false;')

    def push_cut(self):
        mel.eval('timeSliderCutKey;')
    
    def push_delete(self):
        mel.eval('timeSliderClearKey;')


def show_ui(restore=False):
    global custom_mixin_widget, scriptJob_id_anim

    if not custom_mixin_widget:
        custom_mixin_widget = HM_AnimTools()
        custom_mixin_widget.setObjectName(tool_name)

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
    
    cmds.scriptJob(uiDeleted = [tool_name, window_closed])
    scriptJob_id_anim = cmds.scriptJob(conditionChange = ['playingBack', playback_changed])

    return custom_mixin_widget


def playback_changed():
    global win
    if cmds.play(q = True, state = True):
        if cmds.play(q = True, forward = True):
            win.playButton.setIcon(QIcon(':/timestop.png'))
        else:
            win.revButton.setIcon(QIcon(':/timestop.png'))
    else:
            win.playButton.setIcon(QIcon(':/timeplay.png'))
            win.revButton.setIcon(QIcon(':/timerev.png'))


def window_closed():
    global scriptJob_id_anim
    cmds.scriptJob(kill = scriptJob_id_anim, force = True)


def main():
    show_ui()


if __name__ == "__main__": 
    main()