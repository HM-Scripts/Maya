import maya.cmds as cmds
import maya.mel as mel
import re
from functools import partial

def create_groupNode(window_mode, *args):

    #選択オブジェクト
    selected = cmds.ls(sl = True)
    selected_lengs = len(cmds.ls(sl = True, fl = True))

    #変換テキスト
    source_Str = cmds.textField('source_Str_BOX', q = True, text = True)
    destination_Str = cmds.textField('destination_Str_BOX', q = True, text = True)

    #選択確認
    if selected_lengs > 0:
        not_joint = []
        for obj in selected:

            jnt_name = str(obj).replace("['","").replace("']","")
            grp_name = str(jnt_name).replace(source_Str, destination_Str)
            
            if check_joint(obj):

                #名前の重複確認
                if jnt_name == grp_name:
                    pattern = '(\d+)$'
                    match = re.search(pattern, jnt_name)
                    if match:
                        number = int(match.group(1)) + 1
                        grp_name = re.sub(pattern, str(number), jnt_name)
                        print(grp_name)
                    else:
                        grp_name = jnt_name + '1'

                #空のグループノード作成
                cmds.group(em = True, name = grp_name)

                #トランスフォームの一致
                cmds.matchTransform(grp_name, jnt_name)

                print('create group: ' + grp_name)

            else:
                not_joint.append(jnt_name)
                print(jnt_name + " is not 'joint'")

        if not_joint:
            print(u'error: 以下のオブジェクトがjointとして認識されませんでした')
            for error_obj in not_joint:
                print(error_obj)
            cmds.warning(u'一部の選択したオブジェクトがジョイントとして認識されませんでした')
        else:
            infomation_text = str(selected_lengs) + u' 個のグループノードを作成しました'
            mel.eval('print "' + infomation_text + '"')
            cmds.text('info_text', e = True, label = infomation_text)
        
        if window_mode:
            cmds.deleteUI('groupNode_Creater_Win')
    
    else:
        cmds.warning(u'一つ以上のジョイントを選択してください')


#設定の保存
def save_settings(self):
    source_Str = cmds.textField('source_Str_BOX', q = True, text = True)
    destination_Str = cmds.textField('destination_Str_BOX', q = True, text = True)
    cmds.optionVar(sv = ('HM_groupNode_Creater_source_Str', source_Str))
    cmds.optionVar(sv = ('HM_groupNode_Creater_destination_Str', destination_Str))
    print('saved setting')
    cmds.text('info_text', e = True, label = u'設定を保存しました')


#ジョイント確認
def check_joint(obj):
    return cmds.nodeType(obj) == 'joint'


#UI
def groupNode_Creater_UI(source_Str, destination_Str):

    #ウィンドウ初期化
    if cmds.window('groupNode_Creater_Win', exists = True):
        cmds.deleteUI('groupNode_Creater_Win')

    #ウィンドウ作成
    cmds.window('groupNode_Creater_Win', title = 'グループノード作成の設定', width = 500)
    base_layout = cmds.columnLayout(columnAttach = ('both', 5), rowSpacing = 5, columnWidth = 500)
    layout1 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (110, 390), p = base_layout)
    layout2 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (110, 390), p = base_layout)
    cmds.text(label = u'検索する文字列', p = layout1, al = 'center', width = 100)
    cmds.textField('source_Str_BOX', text = source_Str, p = layout1, width = 370)
    cmds.text(label = u'置換後の文字列', p = layout2, al = 'center', width = 100)
    cmds.textField('destination_Str_BOX', text = destination_Str, p = layout2, width = 370)
    layout3 = cmds.rowLayout(numberOfColumns = 4, columnWidth4 = (120, 120, 120, 120), columnAttach4 = ('both', 'both', 'both', 'both'), columnOffset4 = (10, 10, 10, 10), p = base_layout)
    cmds.button(label = u'適用', p = layout3, command = partial(create_groupNode, False))
    cmds.button(label = u'作成', p = layout3, command = partial(create_groupNode, False))
    cmds.button(label = u'設定の保存', p = layout3, command = save_settings)
    cmds.button(label = u'閉じる', p = layout3, command = 'cmds.deleteUI("groupNode_Creater_Win")')
    layout4 = cmds.rowLayout(numberOfColumns = 2, columnWidth2 = (400, 100), p = base_layout, columnAlign2 = ('left', 'right'))
    cmds.text('info_text', label = '', p = layout4, align = 'left')
    cmds.text('version_text', label = 'version:' + version(), p = layout4, align = 'right')
    cmds.showWindow('groupNode_Creater_Win')


#メイン関数
def HM_groupNode_Creater():

    #保存データの確認
    #置換元テキスト
    if cmds.optionVar(ex = 'HM_groupNode_Creater_source_Str'):
        source_Str = cmds.optionVar(q = 'HM_groupNode_Creater_source_Str')
    else:
        #存在しなければデフォルトを保存
        source_Str = '_joint'
        cmds.optionVar(sv = ('HM_groupNode_Creater_source_Str', source_Str))

    #置換先テキスト
    if cmds.optionVar(ex = 'HM_groupNode_Creater_destination_Str'):
        destination_Str = cmds.optionVar(q = 'HM_groupNode_Creater_destination_Str')
    else:
        #存在しなければデフォルトを保存
        destination_Str = '_group'
        cmds.optionVar(sv = ('HM_groupNode_Creater_destination_Str', destination_Str))

    #UI起動
    groupNode_Creater_UI(source_Str, destination_Str)


#バージョン情報
def version():
    version = '1.0.3'
    return version