import maya.cmds as cmds
import json
import os
import pathlib
import shutil

def onMayaDroppedPythonFile(*args, **kwargs):
    HM_installer()


def HM_installer():

    #スクリプトの存在場所
    import_path = os.path.dirname(__file__) + '/'
    user_scriptDir = cmds.internalVar(userScriptDir = True)
    HM_scriptDir = user_scriptDir# + 'HM_Scripts/'

    #インストール元フォルダ一覧の取得
    install_scriptDir = [f for f in os.listdir(import_path) if os.path.isdir(os.path.join(import_path, f))]
    install_scriptDir.remove('__pycache__')

    #既定の形式かどうか
    if len(install_scriptDir) == 1:
        import_path += f'{install_scriptDir[0]}/'
    else:
        cmds.error('Script files not found.')
        return

    #フォルダが存在しなければ作成
    if not os.path.isdir(HM_scriptDir):
        os.makedirs(HM_scriptDir)
        print('mkdir "' + HM_scriptDir + '"')
        initFile = pathlib.Path(HM_scriptDir + '__init__.py')
        initFile.touch()
    
    #jsonの読み込み処理
    loadSetting = openJson(import_path + 'installConfig.hmd')

    #インストールデータ確認
    if 'dataType' in loadSetting['Properties']:
        if loadSetting['Properties'].get('dataType') == 'HM_mayaScriptInstallData':
            pass
        else:
            cmds.error('Script install error.')
            return
    else:
        cmds.error('Script install error.')
        return
    
    #フォルダ作成
    mkDir = loadSetting['Properties'].get('mkdir')
    for directory in mkDir:
        dirPath = HM_scriptDir + directory
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

    #ファイルコピー
    scriptFiles = loadSetting['Properties'].get('scriptFiles')
    for copyFile in scriptFiles:
        copyFile_path = import_path + copyFile
        saveFile_path = HM_scriptDir + copyFile
        shutil.copy(copyFile_path, saveFile_path)
        print('Copy', copyFile, 'to', saveFile_path)

    
    #シェルフボタン登録
    _parent = cmds.shelfTabLayout("ShelfLayout", query=True, selectTab=True)

    buttonNum = loadSetting['Properties'].get('buttonNum')
    if buttonNum >= 1:
        for i in range(buttonNum):
            buttonName = loadSetting['Properties'].get('buttonName')[i]
            _command = loadSetting['Properties'].get('command')[i]
            _image = loadSetting['Properties'].get('image')[i]
            _annotation = loadSetting['Properties'].get('annotation')[i]
            label = loadSetting['Properties'].get('label')[i]
            _sourceType = loadSetting['Properties'].get('sourceType')[i]
            if cmds.shelfButton(buttonName, exists = True):
                cmds.shelfButton(
                    buttonName,
                    e = True,
                    command = _command,
                    image = _image,
                    annotation = _annotation,
                    label = label,
                    imageOverlayLabel = label,
                    sourceType = _sourceType,
                    parent = _parent
                )
            else:
                cmds.shelfButton(
                    buttonName,
                    command = _command,
                    image = _image,
                    annotation = _annotation,
                    label = label,
                    imageOverlayLabel = label,
                    sourceType = _sourceType,
                    parent = _parent
                )
    
    #終了メッセージ
    print('Installing completed.')
    cmds.confirmDialog(title = 'Message', icon = 'information', button = 'OK', db = 'OK',
                       message = 'スクリプトのインストールが完了しました。\nMayaを再起動してください。')


def openJson(filePath):
    with open(filePath, 'r') as fileOpen:
        fileLoad = json.load(fileOpen)
    return fileLoad
        

if __name__ == "__main__": 
    HM_installer()