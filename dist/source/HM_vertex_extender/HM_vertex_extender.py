import maya.cmds as cmds
import math
import HM_vertex_extender as vExt


#呼び出し関数
def HM_vertex_extender():

    #頂点選択確認
    if cmds.selectType(q=True, vertex=True) and len(cmds.ls(sl=True, fl=True)) == 1:

        #グローバル変数宣言
        global vPosition0, vertex0

        #1つ目の頂点を記憶
        vertex0 = cmds.ls(sl=True, fl=True)

        #1つ目の頂点の座標取得
        vObject0 = cmds.ls(sl=True)
        vPosition0 = cmds.pointPosition(vObject0, w=True)

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
    cmds.button(label=u'実行', command='vExt.vertex_extend_processer()')
    cmds.text(label=u'2つ目の頂点のみ選択して"実行"')
    cmds.showWindow('verExtWin')


#処理実行関数
def vertex_extend_processer():

    #グローバル変数宣言
    global vPosition0, vertex0

    #2つ目の頂点の座標取得
    vObject1 = cmds.ls(sl=True)
    vPosition1 = cmds.pointPosition(vObject1, w=True)

    #座標設定
    x0, y0, z0 = vPosition0
    x1, y1, z1 = vPosition1

    #計算
    delta_x = x1 - x0
    delta_y = y1 - y0
    delta_z = z1 - z0

    #0を除く
    if delta_x == 0 and delta_y == 0 and delta_z == 0:
        cmds.error(u'頂点が同じ位置にあります。')
        cmds.select(vertex0)
    else:
        r = math.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
        theta = math.degrees(math.acos(delta_z / r))
        phi = math.degrees(math.atan2(delta_y,delta_x))

        #元の頂点を選択
        cmds.select(vertex0)

        #マニピュレータの編集
        cmds.manipPivot(p=(x0, y0, z0), o=(0, theta, phi))

    #ウィンドウ削除
    cmds.deleteUI('verExtWin')