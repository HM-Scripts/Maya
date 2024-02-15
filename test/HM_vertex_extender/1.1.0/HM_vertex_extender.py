import maya.cmds as cmds
import math

#呼び出し関数
def HM_vertex_extender():
    global vertex0

    #選択されている項目
    selected = cmds.ls(sl = True, fl = True)

    #頂点選択確認
    if cmds.selectType(q = True, vertex = True) and len(selected) == 1:

        #1つ目の頂点を記憶
        vertex0 = selected[0]

        #2つ目を選択するウィンドウ表示
        vertex_extender_UI()

    #選択された頂点の数が1以外
    else:
        cmds.warning(u"頂点を1つ選択してください")


#UI表示関数
def vertex_extender_UI():

    #Window初期化
    if cmds.window("verExtWin", exists=True):
        cmds.deleteUI("verExtWin")

    #Window設定
    cmds.window("verExtWin", title="頂点の選択", width=200)
    cmds.columnLayout(columnAttach=("both", 5), rowSpacing=5, columnWidth=200, adjustableColumn=True)
    cmds.text(label=u'エッジの延長スクリプト')
    cmds.button(label=u'実行', command=f'import {__name__};{__name__}.vertex_extend_processer()')
    cmds.text(label=u'2つ目の頂点のみ選択して"実行"')
    cmds.text(label = 'version: ' + version(), width = 180, align = 'right')
    cmds.showWindow('verExtWin')


#処理実行関数
def vertex_extend_processer():
    vertex1 = None
    x, y, z = []

    #選択されている項目
    selected = cmds.ls(sl = True, fl = True)

    #頂点選択確認
    if cmds.selectType(q = True, vertex = True) and len(selected) == 1:

        #1つ目の頂点を記憶
        vertex1 = selected[0]

    #選択された頂点の数が1以外
    else:
        cmds.warning(u"頂点を1つ選択してください")
        return
    
    #頂点座標の取得
    vPosition0 = cmds.pointPosition(vertex0, w=True)
    vPosition1 = cmds.pointPosition(vertex1, w=True)

    #座標設定
    x[0], y[0], z[0] = vPosition0
    x[1], y[1], z[1] = vPosition1

    #計算
    delta_x = x[1] - x[0]
    delta_y = y[1] - y[0]
    delta_z = z[1] - z[0]

    #0を除く
    if delta_x == 0 and delta_y == 0 and delta_z == 0:
        cmds.select(vertex0)
        cmds.deleteUI('verExtWin')
        cmds.error(u'頂点が同じ位置にあります。')
        return

    else:
        r = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
        theta = math.degrees(math.acos(delta_z / r))
        phi = math.degrees(math.atan2(delta_y,delta_x))

        #元の頂点を選択
        cmds.select(vertex0)

        #マニピュレータの編集
        cmds.manipPivot(p = vPosition0, o = (0, theta, phi))

    #ウィンドウ削除
    cmds.deleteUI('verExtWin')

def main():
    HM_vertex_extender()

def version():
    return '1.1.0'