import maya.cmds as cmds
import maya.mel as mel

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QFont

tool_name = 'HM_AnimTools'
custom_mixin_widget = None
scriptJob_id_anim = None
win = None
ui_size = 60

class HM_AnimTools(MayaQWidgetDockableMixin, QMainWindow):
    title = tool_name

    def __init__(self, parent = None):
        super(HM_AnimTools, self).__init__(parent)
        global win
        win = self

        self.setObjectName(self.title)
        self.setWindowTitle(self.title)

        self._font = QFont()

        self.plusButton = QPushButton(self)
        self.minusButton = QPushButton(self)

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

        self.plusButton.setGeometry(50, 20, 25, 25)
        self.minusButton.setGeometry(20, 20, 25, 25)

        self.plusButton.setText('+')
        self.minusButton.setText('-')

        self.playButton.setIcon(QIcon(':/timeplay.png'))
        self.revButton.setIcon(QIcon(':/timerev.png'))
        self.nextButton.setIcon(QIcon(':/timenext.png'))
        self.prevButton.setIcon(QIcon(':/timeprev.png'))
        self.startButton.setIcon(QIcon(':/timestart.png'))
        self.endButton.setIcon(QIcon(':/timeend.png'))
        self.fwdButton.setIcon(QIcon(':/timefwd.png'))
        self.rewButton.setIcon(QIcon(':/timerew.png'))

        self.copyButton.setText('Copy')
        self.pasteButton.setText('Paste')
        self.cutButton.setText('Cut')
        self.deleteButton.setText('Delete')

        self.plusButton.clicked.connect(self.push_plus)
        self.minusButton.clicked.connect(self.push_minus)

        self.playButton.clicked.connect(self.push_play)
        self.revButton.clicked.connect(self.push_rev)
        self.nextButton.clicked.connect(self.push_next)
        self.prevButton.clicked.connect(self.push_prev)
        self.startButton.clicked.connect(self.push_start)
        self.endButton.clicked.connect(self.push_end)
        self.fwdButton.clicked.connect(self.push_fwd)
        self.rewButton.clicked.connect(self.push_rew)

        self.copyButton.clicked.connect(self.push_copy)
        self.pasteButton.clicked.connect(self.push_paste)
        self.cutButton.clicked.connect(self.push_cut)
        self.deleteButton.clicked.connect(self.push_delete)

        self.set_buttonsGeo()

    def push_plus(self):
        global ui_size
        ui_size += 10
        self.minusButton.setEnabled(True)
        self.set_buttonsGeo()

    def push_minus(self):
        global ui_size
        if (ui_size > 30):
            ui_size -= 10
            self.set_buttonsGeo()
        if (ui_size == 30):
            self.minusButton.setEnabled(False)

    def set_buttonsGeo(self):
        global ui_size
        self.playButton.setGeometry(ui_size * 4 + 60, 60, ui_size, ui_size)
        self.revButton.setGeometry(ui_size * 3 + 50, 60, ui_size, ui_size)
        self.nextButton.setGeometry(ui_size * 5 + 70, 60, ui_size, ui_size)
        self.prevButton.setGeometry(ui_size * 2 + 40, 60, ui_size, ui_size)
        self.startButton.setGeometry(ui_size * 6 + 80, 60, ui_size, ui_size)
        self.endButton.setGeometry(ui_size + 30, 60, ui_size, ui_size)
        self.fwdButton.setGeometry(ui_size * 7 + 90, 60, ui_size, ui_size)
        self.rewButton.setGeometry(20, 60, ui_size, ui_size)

        self.copyButton.setGeometry(ui_size * 2 + 40, ui_size + 80, ui_size * 2 + 10, ui_size * 2 / 3)
        self.pasteButton.setGeometry(ui_size * 4 + 60, ui_size + 80, ui_size * 2 + 10, ui_size * 2 / 3)
        self.cutButton.setGeometry(20, ui_size + 80, ui_size * 2 + 10, ui_size * 2 / 3)
        self.deleteButton.setGeometry(ui_size * 6 + 80, ui_size + 80, ui_size * 2 + 10, ui_size * 2 / 3)

        fontScale = ui_size / 60
        self._font.setPixelSize(20 * fontScale)

        self.copyButton.setFont(self._font)
        self.pasteButton.setFont(self._font)
        self.cutButton.setFont(self._font)
        self.deleteButton.setFont(self._font)
    
    def push_play(self):
        is_anim_playing = cmds.play(q = True, state = True)
    
        if is_anim_playing:
            cmds.play(state = False)
        else:
            cmds.play(forward = True, state = True)
            self.playButton.setIcon(QIcon(':/timestop.png'))
    
    def push_rev(self):
        is_anim_playing = cmds.play(q = True, state = True)
    
        if is_anim_playing:
            cmds.play(state = False)
        else:
            cmds.play(forward = False, state = True)
            self.revButton.setIcon(QIcon(':/timestop.png'))
    
    def push_next(self):
        mel.eval('NextKey;')
    
    def push_prev(self):
        mel.eval('PreviousKey;')
    
    def push_start(self):
        mel.eval('playButtonStepForward;')
    
    def push_end(self):
        mel.eval('playButtonStepBackward;')
    
    def push_fwd(self):
        mel.eval('playButtonEnd;')
    
    def push_rew(self):
        mel.eval('playButtonStart;')
    
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