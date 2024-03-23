import maya.cmds as cmds
import datetime
import json
import re
from PySide2 import QtWidgets, QtCore
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

renderQueueList = None

class localRenderQUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    renderList = None
    renderProperties = None
    addScene_Button = None
    deleteScene_Button = None
    clearList_Button = None
    saveQueue_Button = None
    openQueue_Button = None
    render_Button = None
    close_Button = None
    version_Label = None

    def __init__(self, parent = None):
        super(localRenderQUI, self).__init__(parent)
        self.setGeometry(0, 0, 500, 460)
        self.setWindowTitle('HM レンダーキュー')
        self.renderList = QtWidgets.QListWidget(self)
        self.renderList.setGeometry(20, 20, 260, 190)
        self.renderList.itemSelectionChanged.connect(self.changeSelected)
        self.renderProperties = QtWidgets.QTextEdit(self)
        self.renderProperties.setGeometry(20, 230, 460, 150)
        self.renderProperties.setReadOnly(True)
        self.addScene_Button = QtWidgets.QPushButton(self)
        self.addScene_Button.setGeometry(300, 20, 180, 30)
        self.addScene_Button.setText('このシーンを追加')
        self.addScene_Button.clicked.connect(self.addScene)
        self.deleteScene_Button = QtWidgets.QPushButton(self)
        self.deleteScene_Button.setGeometry(300, 60, 180, 30)
        self.deleteScene_Button.setText('選択中のシーンを削除')
        self.deleteScene_Button.clicked.connect(self.delScene)
        self.clearList_Button = QtWidgets.QPushButton(self)
        self.clearList_Button.setGeometry(300, 100, 180, 30)
        self.clearList_Button.setText('一覧をクリア')
        self.clearList_Button.clicked.connect(self.clearList)
        self.saveQueue_Button = QtWidgets.QPushButton(self)
        self.saveQueue_Button.setGeometry(300, 140, 180, 30)
        self.saveQueue_Button.setText('キューを保存')
        self.saveQueue_Button.clicked.connect(self.exportQueue)
        self.openQueue_Button = QtWidgets.QPushButton(self)
        self.openQueue_Button.setGeometry(300, 180, 180, 30)
        self.openQueue_Button.setText('保存したキューを開く')
        self.openQueue_Button.clicked.connect(self.importQueue)
        self.render_Button = QtWidgets.QPushButton(self)
        self.render_Button.setGeometry(20, 400, 220, 30)
        self.render_Button.setText('レンダリング')
        self.render_Button.clicked.connect(self.clickRender)
        self.close_Button = QtWidgets.QPushButton(self)
        self.close_Button.setGeometry(260, 400, 220, 30)
        self.close_Button.setText('閉じる')
        self.close_Button.clicked.connect(self.closeUI)
        self.version_Label = QtWidgets.QLabel(self)
        self.version_Label.setGeometry(10, 430, 480, 30)
        self.version_Label.setText('version: ' + version())
        self.version_Label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

    # シーンをリストに追加
    def addScene(self):
        global renderQueueList
        scenePath = cmds.file(sceneName = True, q = True)
        projectPath = cmds.workspace(fullName = True, q = True)
        width = cmds.getAttr('defaultResolution.width')
        height = cmds.getAttr('defaultResolution.height')
        renderer = cmds.getAttr('defaultRenderGlobals.currentRenderer')
        startFrame = cmds.getAttr('defaultRenderGlobals.startFrame')
        endFrame = cmds.getAttr('defaultRenderGlobals.endFrame')
        modifyExtension = cmds.getAttr('defaultRenderGlobals.modifyExtension')
        startExtension = ''
        byExtension = ''
        if modifyExtension:
            startExtension = cmds.getAttr('defaultRenderGlobals.startExtension')
            byExtension = cmds.getAttr('defaultRenderGlobals.byExtension')
        addText = cmds.file(sceneName = True, shortName = True, q = True)
        settings = {
            'projectPath': projectPath,
            'scenePath': scenePath,
            'sceneName': addText,
            'width': width,
            'height': height,
            'renderer': renderer,
            'sFrame': startFrame,
            'eFrame': endFrame,
            'mExt': modifyExtension,
            'sExt': startExtension,
            'bExt': byExtension
        }
        if addText in renderQueueList['queue']:
            while True:
                pattern = '(\d+)$'
                match = re.search(pattern, addText)
                if match:
                    number = int(match.group(1)) + 1
                    addText = re.sub(pattern, str(number), addText)
                else:
                    addText += '1'
                if not addText in renderQueueList['queue']:
                    break
        renderQueueList[addText] = settings
        renderQueueList['queue'].append(addText)
        self.renderList.addItem(addText)

    # シーンをリストから削除
    def delScene(self):
        global renderQueueList
        row = self.renderList.currentRow()
        item = self.renderList.item(row)
        if item != None:
            self.renderProperties.setText('')
            text = item.text()
            self.renderList.takeItem(row)
            del renderQueueList[text]
            renderQueueList['queue'].remove(text)

    # リストをクリア
    def clearList(self):
        global renderQueueList
        self.renderList.clear()
        self.renderProperties.setText('')
        renderQueueList = {
            'queue': []
        }

    # UIを閉じる
    def closeUI(self):
        self.close()

    # リスト上の選択を変更するとき
    def changeSelected(self):
        global renderQueueList
        row = self.renderList.currentRow()
        item = self.renderList.item(row)
        if item != None:
            setting = renderQueueList[item.text()]
            text = ('Project: ' + setting['projectPath'] + '\n'
                    + 'Scene: ' + setting['scenePath'] + '\n'
                    + 'Render: ' + setting['renderer'] + '  '
                    + 'Width: ' + str(setting['width']) + 'px  '
                    + 'Height: ' + str(setting['height']) + 'px\n'
                    + 'Start: ' + str(setting['sFrame']) + '  '
                    + 'End: ' + str(setting['eFrame']))
            self.renderProperties.setText(text)

    # キューのリストを書き出し
    def exportQueue(self):
        if self.renderList.count() == 0:
            self.renderProperties.setText('No list exists.')
        else:
            filter = "JSON Files (*.json)"
            filePath = cmds.fileDialog2(fileFilter = filter, dialogStyle = 1, fileMode = 0, dir = cmds.workspace(fullName = True, q = True))
            saveJson(filePath[0])

    # キューのリストの読み込み
    def importQueue(self):
        global renderQueueList
        filter = "JSON Files (*.json)"
        filePath = cmds.fileDialog2(fileFilter = filter, dialogStyle = 1, fileMode = 1, dir = cmds.workspace(fullName = True, q = True))
        openList = openJson(filePath[0])
        if openList == 'dataError':
            self.renderProperties.setText('File error.')
        else:
            self.renderList.clear()
            renderQueueList = openList
            for addText in renderQueueList['queue']:
                self.renderList.addItem(addText)

    def clickRender(self):
        self.addScene_Button.setEnabled(False)
        self.deleteScene_Button.setEnabled(False)
        self.clearList_Button.setEnabled(False)
        self.saveQueue_Button.setEnabled(False)
        self.openQueue_Button.setEnabled(False)
        self.render_Button.setEnabled(False)
        self.close_Button.setEnabled(False)
        result = localRenderQ()
        self.addScene_Button.setEnabled(True)
        self.deleteScene_Button.setEnabled(True)
        self.clearList_Button.setEnabled(True)
        self.saveQueue_Button.setEnabled(True)
        self.openQueue_Button.setEnabled(True)
        self.render_Button.setEnabled(True)
        self.close_Button.setEnabled(True)
        if result == 0:
            self.clearList()
            self.renderProperties.setText('Completed rendering.')
        elif result == 1:
            self.renderProperties.setText('Canceled rendering.')

# レンダリングのメイン関数
def localRenderQ():

    # 変数を定義
    scenePath = None

    # キューに値が存在するか確認
    if len(renderQueueList['queue']) >0:
    
        # シーンごとに処理
        for renderQueue in renderQueueList['queue']:
            queueData = renderQueueList[renderQueue]
            projectPath = queueData['projectPath']
            scenePath = queueData['scenePath']
            width = queueData['width']
            height = queueData['height']
            renderer = queueData['renderer']
            startFrame = queueData['sFrame']
            endFrame = queueData['eFrame']
            modifyExtension = queueData['mExt']
            startExtension = queueData['sExt']
            byExtension = queueData['bExt']

            # プロジェクト設定が異なる場合は更新
            if cmds.workspace(fullName = True, q = True) != projectPath:
                cmds.workspace(projectPath, o = True)
            
            # ファイルを開く
            cmds.file(scenePath, o = True, f = True)

            # レンダラー確認
            if renderer == 'arnold':

                # 現在のレンダラをArnoldに設定
                cmds.setAttr('defaultRenderGlobals.currentRenderer', 'arnold', type='string')
                print('start arnoldRender')

                # プログレスウィンドウを表示
                cmds.progressWindow(isInterruptable = True, title = 'arnoldRender', status = 'Rendering: ' + renderQueue, min = int(startFrame) - 1, max = int(endFrame))

                # フレームごとにレンダリング
                for frameNum in range(int(startFrame), int(endFrame) + 1):

                    # レンダリング
                    arnoldRenderer(frameNum, width, height, modifyExtension, startExtension)

                    # フレーム番号変更
                    if modifyExtension:
                        startExtension += byExtension

                    # キャンセル確認
                    if cmds.progressWindow(query = True, isCancelled = True):
                        cmds.file(scenePath, o = True, f = True)
                        cmds.progressWindow(endProgress = True)
                        return 1

                    # プログレスバー更新
                    cmds.progressWindow(e = True, progress = frameNum)
                
                # プログレスバー終了
                cmds.progressWindow(endProgress = True)
        cmds.file(scenePath, o = True, f = True)
        return 0

# Arnoldレンダリング
def arnoldRenderer(frame, width, height, mExt, extNum):

    # フレームを設定
    cmds.setAttr('defaultRenderGlobals.startFrame', frame)
    cmds.setAttr('defaultRenderGlobals.endFrame', frame)
    cmds.setAttr('defaultRenderGlobals.modifyExtension', mExt)
    if mExt:
        cmds.setAttr('defaultRenderGlobals.startExtension', extNum)

    # レンダーレイヤーを取得
    render_layers = cmds.ls(type='renderLayer')

    # 有効なレンダーレイヤーのみレンダリングを実行
    for render_layer in render_layers:
        if cmds.getAttr(f'{render_layer}.renderable'):
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            cmds.arnoldRender(b = True, w = width, h = height)

#JSONプロパティ
def HM_jsonProperty():
    dt_now = datetime.datetime.utcnow()
    properties = {
        'dataType': 'HM_mayaRenderQueue',
        'exporter': 'HM_renderQueue',
        'exporterVersion': version(),
        'exportTimeStamp': {
            'year': dt_now.year,
            'month': dt_now.month,
            'day': dt_now.day,
            'hour': dt_now.hour,
            'minute': dt_now.minute,
            'second': dt_now.second,
            'microsecond': dt_now.microsecond
        }
    }
    return properties

#JSON書き出し
def saveJson(filePath):
    global renderQueueList
    jsonData = {}
    jsonData['Properties'] = HM_jsonProperty()
    jsonData['renderQueue'] = renderQueueList
    with open(filePath, 'w') as jsonFile:
        json.dump(jsonData, jsonFile, indent = 4)

#JSON読み込み
def openJson(filePath):
    print()
    fileOpen = open(filePath, 'r')
    fileLoad = json.load(fileOpen)
    if 'dataType' in fileLoad['Properties']:
        if fileLoad['Properties'].get('dataType') == 'HM_mayaRenderQueue':
            return fileLoad['renderQueue']
    return 'dataError'

#開始関数
def HM_localRenderQUI():
    global renderQueueList
    renderQueueList = {
        'queue': []
    }
    window = localRenderQUI()
    window.show()

def version():
    version = '0.1.0\N{greek small letter alpha}'
    return version

def main():
    HM_localRenderQUI()

if __name__ == "__main__": 
    HM_localRenderQUI()