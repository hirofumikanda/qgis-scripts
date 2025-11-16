from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsVectorLayer,
    QgsField,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsFillSymbol,
    QgsSingleSymbolRenderer
)
import math

# ==== 設定 ==== #
ZOOM = 10

# Webメルカトル定義
ORIGIN_SHIFT = 20037508.342789244
TILE_SIZE = 256

def resolution(z):
    return (2 * ORIGIN_SHIFT) / (TILE_SIZE * 2 ** z)

def mercator_to_tile(mx, my, z):
    res = resolution(z)
    px = (mx + ORIGIN_SHIFT) / res
    py = (ORIGIN_SHIFT - my) / res
    tx = int(px / TILE_SIZE)
    ty = int(py / TILE_SIZE)
    return tx, ty

def tile_bounds(tx, ty, z):
    res = resolution(z)
    minx = tx * TILE_SIZE * res - ORIGIN_SHIFT
    maxx = (tx + 1) * TILE_SIZE * res - ORIGIN_SHIFT
    maxy = ORIGIN_SHIFT - ty * TILE_SIZE * res
    miny = ORIGIN_SHIFT - (ty + 1) * TILE_SIZE * res
    return (minx, miny, maxx, maxy)

# ==== 表示範囲取得 ==== #
canvas = iface.mapCanvas()
extent = canvas.extent()
canvas_crs = canvas.mapSettings().destinationCrs()
epsg3857 = QgsCoordinateReferenceSystem("EPSG:3857")

if canvas_crs != epsg3857:
    xfm = QgsCoordinateTransform(canvas_crs, epsg3857, QgsProject.instance())
    ext = xfm.transformBoundingBox(extent)
else:
    ext = extent

minx, maxx = ext.xMinimum(), ext.xMaximum()
miny, maxy = ext.yMinimum(), ext.yMaximum()

min_tx, max_ty = mercator_to_tile(minx, miny, ZOOM)
max_tx, min_ty = mercator_to_tile(maxx, maxy, ZOOM)
tx0, tx1 = sorted([min_tx, max_tx])
ty0, ty1 = sorted([min_ty, max_ty])

# ==== レイヤ作成 ==== #
vl = QgsVectorLayer("Polygon?crs=EPSG:3857", f"tiles_z{ZOOM}", "memory")
pr = vl.dataProvider()

pr.addAttributes([
    QgsField("z", QVariant.Int),
    QgsField("x", QVariant.Int),
    QgsField("y", QVariant.Int),
])
vl.updateFields()

# ==== タイル境界ポリゴン生成 ==== #
features = []
for tx in range(tx0, tx1 + 1):
    for ty in range(ty0, ty1 + 1):
        minx, miny, maxx, maxy = tile_bounds(tx, ty, ZOOM)
        pts = [
            QgsPointXY(minx, miny),
            QgsPointXY(maxx, miny),
            QgsPointXY(maxx, maxy),
            QgsPointXY(minx, maxy),
            QgsPointXY(minx, miny),
        ]
        feat = QgsFeature(vl.fields())
        feat.setGeometry(QgsGeometry.fromPolygonXY([pts]))
        feat["z"] = ZOOM
        feat["x"] = tx
        feat["y"] = ty
        features.append(feat)

pr.addFeatures(features)
vl.updateExtents()

# ==== ★ デフォルトスタイル（塗りなし ＋ 黒線）を自動適用 ==== #
symbol = QgsFillSymbol.createSimple({
    'style': 'no',                  # 塗りつぶしなし
    'outline_color': '0,0,0',       # 線色（黒）
    'outline_width': '0.3',         # 線の太さ（mm）
})
vl.setRenderer(QgsSingleSymbolRenderer(symbol))

# プロジェクトに追加
QgsProject.instance().addMapLayer(vl)
