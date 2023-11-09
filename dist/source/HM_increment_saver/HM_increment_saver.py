# coding: utf-8
import maya.cmds as cmds
import maya.mel as mel
import os
import re
from functools import partial

#メイン関数
def main():

    #ファイル名・タイプ取得
    current_file = cmds.file(q = True, sceneName = True, shortName = True)
    current_file_type = cmds.file(q = True, type = True)

    #正規表現に沿ってファイルをリネーム
    rename_str = file_renamer(current_file)

    #名前が変更されていなかったらUIで設定
    if rename_str == current_file:
        increment_saver_UI(current_file, current_file_type)
    
    #名前が変更されていたら保存
    else:
        cmds.file(rename = rename_str)
        current_file_type = str(current_file_type).replace("['", '').replace("']", '')
        current_file_new = cmds.file(q = True, sceneName = True)
        if os.path.exists(current_file_new):
            message_Dialog = cmds.confirmDialog(title = lText('overwrite_title'), message = lText('overwrite_text1') + '\n' + lText('overwrite_text2'),
                                                button = [lText('sel_Yes'), lText('sel_No')], defaultButton = lText('sel_Yes'), cancelButton = lText('sel_No'), dismissString = lText('sel_No'))
            if message_Dialog == lText('sel_No'):
                cmds.file(rename = current_file)
                return
        cmds.file(save = True, type = current_file_type, force = True)
        result = lText('result') + current_file_new
        mel.eval('print "' + result + '"')


#ファイル名リネーム
def file_renamer(input_string):

    #正規表現
    pattern = '_(\d+)\.ma$|\.(\d+)\.ma$|-(\d+)\.ma$|_(\d+)\.mb$|\.(\d+)\.mb$|-(\d+)\.mb$|^(\d+)\.|^(\d+)_|^(\d+)-'
    match = re.search(pattern, input_string)

    #変数を宣言
    match_case = None
    num_str_f = None

    #正規表現に一致する場合は数字に加算
    if match:
        for i in range(1, 9):
            if match.group(i):
                match_case = i
                number = int(match.group(i)) + 1
                num_len = str(0) + str(len(match.group(i)))
                num_str_f = format(number, num_len)
                break
        if match_case == 1:
            return re.sub(pattern, "_" + num_str_f + ".ma", input_string)
        elif match_case == 2:
            return re.sub(pattern, "." + num_str_f + ".ma", input_string)
        elif match_case == 3:
            return re.sub(pattern, "-" + num_str_f + ".ma", input_string)
        elif match_case == 4:
            return re.sub(pattern, "_" + num_str_f + ".mb", input_string)
        elif match_case == 5:
            return re.sub(pattern, "." + num_str_f + ".mb", input_string)
        elif match_case == 6:
            return re.sub(pattern, "-" + num_str_f + ".mb", input_string)
        elif match_case == 7:
            return re.sub(pattern, num_str_f + ".", input_string)
        elif match_case == 8:
            return re.sub(pattern, num_str_f + "_", input_string)
        elif match_case == 9:
            return re.sub(pattern, num_str_f + "-", input_string)
        else:
            return input_string
        
    #一致しない場合は
    else:
        return input_string


#ファイル名を作成し保存
def file_renamer_and_saver(*args):
    new_file_name = str(cmds.textField('file_rename', q = True, text = True)).replace('.ma', '').replace('.mb', '')
    if new_file_name == '':
        cmds.warning(lText('noFileName'))
    else:
        num_len = str(0) + str(cmds.intField('file_num_len', q = True, value = True))
        num_len_f = format(1, num_len)
        cmds.optionVar(iv = ('HM_Increment_Saver_numValue', cmds.intField('file_num_len', q = True, value = True)))
        string_radio_selected = cmds.radioCollection('string_radio', q = True, select = True)
        if string_radio_selected == 'radio_dot':
            punctuation = '.'
        elif string_radio_selected == 'radio_hyp':
            punctuation = '-'
        else:
            punctuation = '_'
        cmds.optionVar(sv = ('HM_Increment_Saver_str', punctuation))
        position_selected = cmds.radioCollection('position_radio', q = True, select = True)
        if position_selected == 'radio_before':
            new_file_name = num_len_f + punctuation + new_file_name
            cmds.optionVar(sv = ('HM_Increment_Saver_position', 'before'))
        else:
            new_file_name = new_file_name + punctuation + num_len_f
            cmds.optionVar(sv = ('HM_Increment_Saver_position', 'after'))
        fileType_selected = cmds.radioCollection('filetype_radio', q = True, select = True)
        if fileType_selected == 'radio_mb':
            new_file_type = 'mayaBinary'
            new_file_name += '.mb'
        else:
            new_file_type = 'mayaAscii'
            new_file_name += '.ma'
        cmds.file(rename = new_file_name)
        saving_file = cmds.file(q = True, sceneName = True)
        if os.path.exists(saving_file):
            cmds.confirmDialog(title = lText('warning'), message = lText('cantSave'))
            return
        cmds.file(save = True, type = new_file_type, force = True)
        result = lText('result') + saving_file
        mel.eval('print "' + result + '"')
        cmds.deleteUI('incSaverWin')


#保存されたウィンドウ情報
def saved_value():
    if cmds.optionVar(ex = 'HM_Increment_Saver_numValue'):
        return cmds.optionVar(q = 'HM_Increment_Saver_numValue')
    else:
        return 3


def saved_position():
    if cmds.optionVar(ex = 'HM_Increment_Saver_position'):
        if cmds.optionVar(q = 'HM_Increment_Saver_position') == 'before':
            cmds.radioButton('radio_before', e = True, select = True)
        else:
            cmds.radioButton('radio_after', e = True, select = True)
    else:
        cmds.radioButton('radio_after', e = True, select = True)


def saved_str():
    if cmds.optionVar(ex = 'HM_Increment_Saver_str'):
        if cmds.optionVar(q = 'HM_Increment_Saver_str') == '.':
            cmds.radioButton('radio_dot', e = True, select = True)
        elif cmds.optionVar(q = 'HM_Increment_Saver_str') == '-':
            cmds.radioButton('radio_hyp', e = True, select = True)
        else:
            cmds.radioButton('radio_und', e = True, select = True)
    else:
        cmds.radioButton('radio_und', e = True, select = True)


#ファイル名設定UI
def increment_saver_UI(filename, filetype):

    #ウィンドウ初期化
    if cmds.window('incSaverWin', exists = True):
        cmds.deleteUI('incSaverWin')
    
    cmds.window('incSaverWin', title = lText('uiTitle'), width = 400)
    base_layout = cmds.columnLayout(columnAttach = ('both', 5), rowSpacing = 5, columnWidth = 400)
    layout1 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (90, 310), p = base_layout)
    cmds.text(label = lText('fName'), p = layout1, al = 'center', width = 90)
    cmds.textField('file_rename', text = filename, p = layout1, width = 295)
    layout3 = cmds.rowLayout(numberOfColumns = 3, columnWidth3 = (130, 140, 130), p = base_layout)
    layout2 = cmds.rowColumnLayout(numberOfRows = 3, p = layout3)
    cmds.text(label = lText('fType'), p = layout2)
    cmds.radioCollection('filetype_radio')
    cmds.radioButton('radio_ma', label = 'Maya ASCII', p = layout2)
    cmds.radioButton('radio_mb', label = 'Maya Binary', p = layout2)
    if filetype == ['mayaBinary']:
        cmds.radioButton('radio_mb', e = True, select = True)
    else:
        cmds.radioButton('radio_ma', e = True, select = True)
    layout4 = cmds.rowColumnLayout(numberOfRows = 4, p = layout3)
    cmds.text(label = lText('aboutNum'), p = layout4)
    layout5 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (30, 70), p = layout4)
    cmds.text(label = lText('digits'), p = layout5)
    cmds.intField('file_num_len', minValue = 1, value = saved_value(), step = 1, p = layout5, width = 60)
    cmds.radioCollection('position_radio')
    cmds.radioButton('radio_before', label = lText('before'), p = layout4)
    cmds.radioButton('radio_after', label = lText('after'), p = layout4)
    saved_position()
    layout6 = cmds.rowColumnLayout(numberOfRows = 4, p = layout3)
    cmds.text(label = lText('delimiter'), p = layout6)
    cmds.radioCollection('string_radio')
    cmds.radioButton('radio_dot', label = lText('dot'), p = layout6)
    cmds.radioButton('radio_und', label = lText('underscore'), p = layout6)
    cmds.radioButton('radio_hyp', label = lText('hyphen'), p = layout6)
    saved_str()
    cmds.button(label = lText('save'), p = base_layout, command = partial(file_renamer_and_saver))
    cmds.text(label = 'version: ' + version(), p = base_layout, width = 380, align = 'right')
    cmds.showWindow('incSaverWin')


#文字列の表示
def lText(inputText):

    #言語別の表記用辞書
    localizationDict = {
        "en_US": {
            "overwrite_title": "Increment Saver", "overwrite_text1": "A file with the same name already exists.",
            "overwrite_text2": "Do you want to replace it?", "sel_Yes": "Yes", "sel_No": "No", "result": "Result: ",
            "noFileName": "No file name entered.", "warning": "Warning",
            "cantSave": "Cannot save because a file with the same name already exists.",
            "uiTitle": "Setting Incremental Saver", "fName": "File Name", "fType": "File Type", "aboutNum": "Digits and Position",
            "digits": "Digits", "before": "Before the name", "after": "After the name", "delimiter": "Delimiter",
            "dot": ". (dot)", "underscore": "_ (underscore)", "hyphen": "- (hyphen)", "save": "Save"
        },
        "ja_JP": {
            "overwrite_title": u"増分保存", "overwrite_text1": u"同じ名前のファイルが既に存在します。",
            "overwrite_text2": u"上書きしますか？", "sel_Yes": u"はい", "sel_No": u"いいえ", "result": u"結果: ",
            "noFileName": u"ファイル名が入力されていません。", "warning": u"警告",
            "cantSave": u"既に同じ名前のファイルが存在するため、保存できません。",
            "uiTitle": u"増分保存の設定", "fName": u"ファイル名", "fType": u"ファイルの種類", "aboutNum": u"連番の桁数と位置",
            "digits": u"桁数", "before": u"名前の前", "after": u"名前の後", "delimiter": u"連番の区切り文字",
            "dot": u". (ドット)", "underscore": u"_ (アンダーバー)", "hyphen": u"- (ハイフン)", "save": u"保存"
        }
    }
    return localizationDict[maya_Language()][inputText]


#Language
def maya_Language():
    lang = cmds.about(uil = True)
    return lang


#version
def version():
    version = '2.1.1'
    return version


def HM_increment_saver():
    main()

if __name__ == "__main__": 
    main()