import maya.cmds as cmds
import maya.mel as mel
import os
import re
from functools import partial

def HM_increment_saver():
    current_file = cmds.file(q = True, sceneName = True, shortName = True)
    current_file_type = cmds.file(q = True, type = True)
    rename_str = file_renamer(current_file)
    if rename_str == current_file:
        increment_saver_UI(current_file, current_file_type)
    else:
        cmds.file(rename = rename_str)
        current_file_type = str(current_file_type).replace("['", '').replace("']", '')
        current_file_new = cmds.file(q = True, sceneName = True)
        if os.path.exists(current_file_new):
            message_Dialog = cmds.confirmDialog(title = u'上書き確認', message = '同じ名前のファイルが既に存在します。\n上書きしますか？',
                                                button = ['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
            if message_Dialog == 'No':
                cmds.file(rename = current_file)
                cmds.warning(u'キャンセルしました')
                return
        cmds.file(save = True, type = current_file_type, force = True)
        result = '結果: ' + current_file_new
        mel.eval('print "' + result + '"')


def file_renamer(input_string):
    pattern = '_(\d+)\.ma$|\.(\d+)\.ma$|-(\d+)\.ma$|_(\d+)\.mb$|\.(\d+)\.mb$|-(\d+)\.mb$|^(\d+)\.|^(\d+)_|^(\d+)-'
    match = re.search(pattern, input_string)
    match_case = None
    num_str_f = None
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
            return re.sub(pattern, "-" + num_str_f + ".mb", input_string)
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


def file_renamer_and_saver(*args):
    new_file_name = str(cmds.textField('file_rename', q = True, text = True)).replace('.ma', '').replace('.mb', '')
    if new_file_name == '':
        cmds.warning(u'ファイル名が入力されていません')
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
            cmds.confirmDialog(title = u'警告', message = u'既に同じファイル名が存在するため、保存できません。')
            return
        cmds.file(save = True, type = new_file_type, force = True)
        result = '結果: ' + saving_file
        mel.eval('print "' + result + '"')
        cmds.deleteUI('incSaverWin')


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


def increment_saver_UI(filename, filetype):
    if cmds.window('incSaverWin', exists = True):
        cmds.deleteUI('incSaverWin')
    cmds.window('incSaverWin', title = '増分保存の設定', width = 400)
    base_layout = cmds.columnLayout(columnAttach = ('both', 5), rowSpacing = 5, columnWidth = 400)
    layout1 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (90, 310), p = base_layout)
    cmds.text(label = u'ファイル名', p = layout1, al = 'center', width = 90)
    cmds.textField('file_rename', text = filename, p = layout1, width = 295)
    layout3 = cmds.rowLayout(numberOfColumns = 3, columnWidth3 = (130, 140, 130), p = base_layout)
    layout2 = cmds.rowColumnLayout(numberOfRows = 3, p = layout3)
    cmds.text(label = u'ファイルの種類', p = layout2)
    cmds.radioCollection('filetype_radio')
    cmds.radioButton('radio_ma', label = 'Maya ASCII', p = layout2)
    cmds.radioButton('radio_mb', label = 'Maya Binary', p = layout2)
    if filetype == ['mayaBinary']:
        cmds.radioButton('radio_mb', e = True, select = True)
    else:
        cmds.radioButton('radio_ma', e = True, select = True)
    layout4 = cmds.rowColumnLayout(numberOfRows = 4, p = layout3)
    cmds.text(label = u'連番の桁数と位置', p = layout4)
    layout5 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (30, 70), p = layout4)
    cmds.text(label = u'桁数', p = layout5)
    cmds.intField('file_num_len', minValue = 1, value = saved_value(), step = 1, p = layout5, width = 60)
    cmds.radioCollection('position_radio')
    cmds.radioButton('radio_before', label = u'名前の前', p = layout4)
    cmds.radioButton('radio_after', label = u'名前の後', p = layout4)
    saved_position()
    layout6 = cmds.rowColumnLayout(numberOfRows = 4, p = layout3)
    cmds.text(label = u'連番の区切り文字', p = layout6)
    cmds.radioCollection('string_radio')
    cmds.radioButton('radio_dot', label = u'. (ドット)', p = layout6)
    cmds.radioButton('radio_und', label = u'_ (アンダーバー)', p = layout6)
    cmds.radioButton('radio_hyp', label = u'- (ハイフン)', p = layout6)
    saved_str()
    cmds.button(label = u'保存', p = base_layout, command = partial(file_renamer_and_saver))
    cmds.text(label = 'version: ' + version(), p = base_layout, width = 380, align = 'right')
    cmds.showWindow('incSaverWin')


def version():
    version = '2.0.0'
    return version