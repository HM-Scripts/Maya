import maya.cmds as cmds
import pymel.core as pm
import re
import os
import HM_increment_saver as isave

def HM_increment_saver():
    current_file = cmds.file(q=True, sceneName=True, shortName=True)
    current_file_type = cmds.file(q=True, type=True)
    if current_file == "":
        increment_saver_UI("", current_file_type)
    else:
        rename_str = file_renamer(current_file)
        if rename_str == current_file:
            increment_saver_UI(current_file, current_file_type)
        else:
            cmds.file(rename=rename_str)
            if current_file_type == ['mayaAscii']:
                current_file_new = cmds.file(q=True, sceneName=True)
                if os.path.exists(current_file_new):
                    message_Dialog = cmds.confirmDialog(title='上書き確認', message='同じ名前のファイルが存在します。\n上書きしますか？', button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
                    if message_Dialog == 'Yes':
                        cmds.file(save=True, type='mayaAscii', force=True)
                        result = "結果:" + current_file_new
                        pm.displayInfo(result)
                    else:
                        cmds.file(rename=current_file)
                        cmds.warning(u'キャンセルしました')
                else:
                    cmds.file(save=True, type='mayaAscii', force=True)
                    result = "結果:" + current_file_new
                    pm.displayInfo(result)
            if current_file_type == ['mayaBinary']:
                current_file_new = cmds.file(q=True, sceneName=True)
                if os.path.exists(current_file_new):
                    message_Dialog = cmds.confirmDialog(title='上書き確認', message='同じ名前のファイルが存在します。\n上書きしますか？', button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
                    if message_Dialog == 'Yes':
                        cmds.file(save=True, type='mayaBinary', force=True)
                        result = "結果:" + current_file_new
                        pm.displayInfo(result)
                    else:
                        cmds.file(rename=current_file)
                        cmds.warning(u'キャンセルしました')
                else:
                    cmds.file(save=True, type='mayaBinary', force=True)
                    result = "結果:" + current_file_new
                    pm.displayInfo(result)


def increment_saver_UI(filename,filetype):
    if cmds.window("incSaverWin", exists=True):
        cmds.deleteUI("incSaverWin")
    global file_rename, file_num_len, radioCollection1, radioCollection2, radioCollection3
    cmds.window("incSaverWin", title="増分保存の設定", width=300)
    cmds.columnLayout(columnAttach=("both", 5), rowSpacing=5, columnWidth=300)
    cmds.text(label=u'ファイル名')
    file_rename = cmds.textField('file_rename',text=filename)
    cmds.text(label=u'ファイルの種類')
    radioCollection3 = cmds.radioCollection()
    if filetype == ['mayaAscii']:
        cmds.radioButton('radioButton3_1', label=u'Maya ASCII', select=True)
        cmds.radioButton('radioButton3_2', label=u'Maya Binary')
    elif filetype == ['mayaBinary']:
        cmds.radioButton('radioButton3_1', label=u'Maya ASCII')
        cmds.radioButton('radioButton3_2', label=u'Maya Binary', select=True)
    else:
        cmds.radioButton('radioButton3_1', label=u'Maya ASCII', select=True)
        cmds.radioButton('radioButton3_2', label=u'Maya Binary')
    cmds.text(label=u'連番の桁数')
    file_num_len = cmds.intField('file_num_len',minValue=1, value=3, step=1)
    cmds.text(label=u'連番の位置')
    radioCollection1 = cmds.radioCollection()
    cmds.radioButton('radioButton1_1', label=u'名前の前')
    cmds.radioButton('radioButton1_2', label=u'名前の後', select=True)
    cmds.text(label=u'連番の区切り文字')
    radioCollection2 = cmds.radioCollection()
    cmds.radioButton('radioButton2_1', label=u'. (ドット)')
    cmds.radioButton('radioButton2_2', label=u'_ (アンダーバー)', select=True)
    cmds.radioButton('radioButton2_3', label=u'- (ハイフン)')
    cmds.button(label=u'保存', command='isave.file_renamer_and_saver()')
    cmds.showWindow("incSaverWin")


def file_renamer_and_saver():
    global file_rename, file_num_len, radioCollection1, radioCollection2, radioCollection3
    new_file_name = cmds.textField('file_rename', q=True, text=True).replace(".ma", "").replace(".mb", "")
    if new_file_name == "":
        cmds.error(u'ファイル名が入力されていません。')
    else:
        print(cmds.intField('file_num_len', query=True, value=True))
        num_len = str(0) + str(cmds.intField('file_num_len', query=True, value=True))
        num_len_f = format(1, num_len)
        kugiri_text = ""
        kugiri_selected = cmds.radioCollection(radioCollection2, q=True, select=True)
        if kugiri_selected == 'radioButton2_1':
            kugiri_text = "."
        elif kugiri_selected == 'radioButton2_2':
            kugiri_text = "_"
        elif kugiri_selected == 'radioButton2_3':
            kugiri_text = "-"
        position_selected = cmds.radioCollection(radioCollection1, q=True, select=True)
        if position_selected == 'radioButton1_1':
            new_file_name = num_len_f + kugiri_text + new_file_name
        elif position_selected == 'radioButton1_2':
            new_file_name = new_file_name + kugiri_text + num_len_f
        file_type_selected = cmds.radioCollection(radioCollection3, q=True, select=True)
        if file_type_selected == 'radioButton3_1':
            new_file_name = new_file_name + ".ma"
            cmds.file(rename=new_file_name)
            current_file_new = cmds.file(q=True, sceneName=True)
            if os.path.exists(current_file_new):
                cmds.confirmDialog(title='警告', message='既に同じファイル名が存在するため、保存できません。', button='OK')
                return
            cmds.file(save=True, type='mayaAscii', force=True)
            result = "結果:" + current_file_new
            pm.displayInfo(result)
            cmds.deleteUI("incSaverWin")
        elif file_type_selected == 'radioButton3_2':
            new_file_name = new_file_name + ".mb"
            cmds.file(rename=new_file_name)
            current_file_new = cmds.file(q=True, sceneName=True)
            if os.path.exists(current_file_new):
                cmds.confirmDialog(title='警告', message='既に同じファイル名が存在するため、保存できません。', button='OK')
                return
            cmds.file(save=True, type='mayaBinary', force=True)
            result = "結果:" + current_file_new
            pm.displayInfo(result)
            cmds.deleteUI("incSaverWin")
    


def file_renamer(input_string):
    #正規表現で数字部分を抽出
    pattern = "_(\d+)\.ma$|\.(\d+)\.ma$|-(\d+)\.ma$|_(\d+)\.mb$|\.(\d+)\.mb$|-(\d+)\.mb$|^(\d+)\.|^(\d+)_|^(\d+)-"
    match = re.search(pattern, input_string)
    if match:
        num_str1 = match.group(1)
        num_str2 = match.group(2)
        num_str3 = match.group(3)
        num_str4 = match.group(4)
        num_str5 = match.group(5)
        num_str6 = match.group(6)
        num_str7 = match.group(7)
        num_str8 = match.group(8)
        num_str9 = match.group(9)
        if num_str1 != None:
            number = int(num_str1) + 1
            num_len = str(0) + str(len(num_str1))
            num_str_f = format(number, num_len)
            return re.sub(pattern, "_" + num_str_f + ".ma", input_string)
        elif num_str2 != None:
            number = int(num_str2) + 1
            num_len = str(0) + str(len(num_str2))
            num_str_f = format(number, num_len)
            return re.sub(pattern, "." + num_str_f + ".ma", input_string)
        elif num_str3 != None:
            number = int(num_str3) + 1
            num_len = str(0) + str(len(num_str3))
            num_str_f = format(number, num_len)
            return re.sub(pattern, "-" + num_str_f + ".ma", input_string)
        elif num_str4 != None:
            number = int(num_str4) + 1
            num_len = str(0) + str(len(num_str4))
            num_str_f = format(number, num_len)
            return re.sub(pattern, "_" + num_str_f + ".mb", input_string)
        elif num_str5 != None:
            number = int(num_str5) + 1
            num_len = str(0) + str(len(num_str5))
            num_str_f = format(number, num_len)
            return re.sub(pattern, "." + num_str_f + ".mb", input_string)
        elif num_str6 != None:
            number = int(num_str6) + 1
            num_len = str(0) + str(len(num_str6))
            num_str_f = format(number, num_len)
            return re.sub(pattern, "-" + num_str_f + ".mb", input_string)
        elif num_str7 != None:
            number = int(num_str7) + 1
            num_len = str(0) + str(len(num_str7))
            num_str_f = format(number, num_len)
            return re.sub(pattern, num_str_f + ".", input_string)
        elif num_str8 != None:
            number = int(num_str8) + 1
            num_len = str(0) + str(len(num_str8))
            num_str_f = format(number, num_len)
            return re.sub(pattern, num_str_f + "_", input_string)
        elif num_str9 != None:
            number = int(num_str9) + 1
            num_len = str(0) + str(len(num_str9))
            num_str_f = format(number, num_len)
            return re.sub(pattern, num_str_f + "-", input_string)
    else:
        return input_string

