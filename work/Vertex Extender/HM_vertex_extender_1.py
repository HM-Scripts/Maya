import maya.cmds as cmds
import math
import HM_vertex_extender as vExt

#改修前の不完全なコード

global vPosition0, vPosition1

def HM_vertex_extender():
    #頂点選択確認
    if cmds.selectType(q=True, vertex=True) and len(cmds.ls(sl=True, fl=True)) == 1:

        #座標取得
        vObjects = cmds.ls(sl=True)
        vPosition0 = cmds.pointPosition(vObjects[0], w=True)
        vPosition1 = cmds.pointPosition(vObjects[1], w=True)

        #座標設定
        x0, y0, z0 = vPosition0
        x1, y1, z1 = vPosition1
        print(x0, y0, z0, x1, y1, z1)

        #計算
        delta_x = x1 - x0
        delta_y = y1 - y0
        delta_z = z1 - z0
        r = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
        theta = math.degrees(math.acos(delta_z / r))
        phi = math.degrees(math.atan2(delta_y,delta_x))

        #1つ目の頂点のみ選択
        vertex0 = cmds.ls(sl=True, fl=True)[0]
        cmds.select(vertex0)

        #マニピュレータの編集
        cmds.manipPivot(p=(x0, y0, z0), o=(0, theta, phi))

    else:
        cmds.warning(u"頂点を1つ選択してください")

def vertex_extender_UI():
    if cmds.window("verExtWin", exists=True):
        cmds.deleteUI("verExtWin")
    cmds.window("verExtWin", title="頂点の選択", width=300)
    cmds.columnLayout(columnAttach=("both", 5), rowSpacing=5, columnWidth=300)
    cmds.button(label=u'', command='実行')

HM_vertex_extender()