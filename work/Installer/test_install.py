import maya.cmds as cmds
import maya.mel as mel
import json
import os
import pathlib
import shutil
#import sys

def onMayaDroppedPythonFile(*args, **kwargs):
    HM_installer()


def HM_installer():
    #script_path = os.path.dirname(__file__) + "/scripts" ==> D:/HAL/scripts/Maya/インストーラー/scripts
    import_path = os.path.dirname(__file__)
    user_scriptDir = cmds.internalVar(userScriptDir = True)
    #maya_lang = cmds.about(uil = True)

    install_scriptDir = [f for f in os.listdir(import_path) if os.path.isdir(os.path.join(import_path, f))]
    install_scriptDir.remove('__pycache__')

    if len(install_scriptDir) == 1:
        import_path += install_scriptDir[0] + '/'
    else:
        cmds.error('Script files not found.')
        return
    
    HM_scriptDir = user_scriptDir + 'HM_Scripts/'
    
    if not os.path.isdir(HM_scriptDir):
        os.makedirs(HM_scriptDir)
        print('mkdir "' + HM_scriptDir + '"')
        initFile = pathlib.Path(HM_scriptDir + '__init__.py')
        initFile.touch()
    
    #jsonの読み込み処理
    loadSetting = openJson(import_path + 'installConfig.hmd')
    if not os.path.isdir(loadSetting):
        cmds.error('Script install error.')
        return

    if 'dataType' in loadSetting['Properties']:
        if loadSetting['Properties'].get('dataType') == 'HM_mayaScriptInstallData':
            pass
        else:
            cmds.error('Script install error.')
            return
    else:
        cmds.error('Script install error.')
        return
    
    #データコピー処理
    mkDir = loadSetting['Properties'].get('mkdir')
    if mkDir != 'None':
        for directory in mkDir:
            dirPath = HM_scriptDir + directory
            if not os.path.exists(dirPath):
                os.makedirs(dirPath)

    scriptFiles = loadSetting['Properties'].get('scriptFiles')
    for copyFile in scriptFiles:
        copyFile_path = import_path + copyFile
        saveFile_path = HM_scriptDir + copyFile
        shutil.copy(copyFile_path, saveFile_path)
        print('Copy', copyFile, 'to', saveFile_path)

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


def openJson(filePath):
    fileOpen = open(filePath, 'r')
    fileLoad = json.load(fileOpen)
    return fileLoad


def saveJson(jsonData, filePath):
    with open(filePath, 'w') as jsonFile:
        json.dump(jsonData, jsonFile, indent = 4)
        

if __name__ == "__main__": 
    HM_installer()