import maya.cmds as cmds
import maya.mel as mel
import os
import glob
from functools import partial

def fbx_exporter(*args):
    global start_time, end_time, save_path
    selected_objects = cmds.ls(sl=True)

    #オブジェクト選択確認
    if not selected_objects:
        cmds.warning(u'書き出すオブジェクトを1つ以上選択してください')
        return
    
    #ファイル重複確認
    cutno_str = cmds.textField('cutno_str', q=True, text=True)
    verno_str = format(cmds.intField('verno_int', q=True, value=True), '02')
    file_path = save_path + 'c' + cutno_str + '_v' + verno_str + '.fbx'
    if os.path.isfile(file_path):
        message_Dialog = cmds.confirmDialog(title=u'上書き確認', message=u'同じ名前のファイルが存在します。\r\n上書きしますか？', button=['Yes', 'Cancel'], defaultButton='Yes', cancelButton='Cancel', dismissString='no')
        if message_Dialog != 'Yes':
            cmds.warning(u'キャンセルしました')
            return
    
    #FBX 書き出しオプション
    cmds.FBXPushSettings()
    try:
        cmds.FBXExportAxisConversionMethod('addFbxRoot')
        cmds.FBXExportEmbeddedTextures('-v', True) #テクスチャを含める
        cmds.FBXExportBakeComplexAnimation('-v', True) #アニメーションをベイク
        cmds.FBXExportBakeComplexStart('-v', start_time) #アニメーション開始フレーム
        cmds.FBXExportBakeComplexEnd('-v', end_time) #アニメーション終了フレーム
        cmds.FBXExportBakeComplexStep('-v', 1) #ステップ数
        cmds.FBXExportSkins('-v', True) #変形したモデル（ブレンドシェイプ）
        cmds.FBXExportShapes('-v', True) #変形したモデル（スキン）
        cmds.FBXExportCameras('-v', True) #カメラを含める
        cmds.FBXExportLights('-v', True) #ライトを含める
        cmds.FBXExportInAscii('-v', True) #Asciiで書き出す
        cmds.FBXExportScaleFactor(100.0)
        cmds.FBXExportConvertUnitString('-v', 'cm') #単位をセンチメートルに変換
        #cmds.FBXExport('-f', file_path, '-s')
        cmds.file(file_path, ch=True, chn=True, exp=True, con=True, f=True, op='v=0', typ='FBX export', es=True)
        change_Take_Name(file_path, 'c' + cutno_str + 'v' + verno_str)
    finally:
        cmds.deleteUI('FBX_Exporter_UI_Win')
        result = u'結果:' + file_path
        mel.eval('print "' + result + '"')


#ファイル名設定UI
def fbx_exporter_UI(start_time, end_time, save_path, file_count):

    if cmds.window('FBX_Exporter_UI_Win', exists=True):
        cmds.deleteUI('FBX_Exporter_UI_Win')
    
    cmds.window('FBX_Exporter_UI_Win', title=u'FBX書き出し設定', width=250)
    cmds.columnLayout(columnAttach=("both", 5), rowSpacing=5, columnWidth=250)
    cmds.text(label=u'カット番号', align='left')
    cmds.textField('cutno_str', text='00', width=100)
    cmds.text(label=u'バージョン番号', align='left')
    cmds.intField('verno_int', minValue=1, value=file_count, step=1, width=100)
    cmds.button(label=u'FBXに書き出し', command=partial(fbx_exporter))
    cmds.scrollField(text=u'保存場所:' + save_path + u'\r\n開始フレーム:' + str(start_time) + u'\r\n終了フレーム:' + str(end_time), ed=False, height=70)
    cmds.text(label='version:' + version(), align='right')
    cmds.showWindow('FBX_Exporter_UI_Win')

#メイン関数
def HM_maya_fbx_exporter_for_unity():
    global start_time, end_time, save_path

    #タイムスライダからフレーム取得
    start_time = cmds.playbackOptions(query=True, ast=True)
    end_time = cmds.playbackOptions(query=True, aet=True)

    project_path = str(cmds.workspace(query=True, rootDirectory=True))
    save_path = project_path + 'FBX/'

    if not os.path.isdir(save_path):
        os.makedirs(save_path)
        file_count = 0
    else:
        file_count = len(glob.glob(save_path + 'c*_v*.fbx'))

    file_count += 1

    fbx_exporter_UI(start_time, end_time, save_path, file_count)

#Take名変更
def change_Take_Name(filepath,filename):
    with open(filepath + '.temp', 'w') as temp_file:
        with open(filepath, 'r') as input_file:
            for line in input_file:
                new_line = line.replace('Take', filename + '_Take')
                temp_file.write(new_line)
    os.remove(filepath)
    os.rename(filepath + '.temp', filepath)

#バージョン情報
def version():
    version = "1.1.2"
    return version