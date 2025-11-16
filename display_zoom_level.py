#ステータスバーに表示
from PyQt5.QtWidgets import QLabel
from math import log
from qgis.PyQt.QtCore import QObject

class ZoomLevelDisplay(QObject):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.label = QLabel()
        self.label.setStyleSheet("padding: 2px;")
        self.iface.statusBarIface().addPermanentWidget(self.label)
        self.canvas.extentsChanged.connect(self.update_zoom_level)
        self.update_zoom_level()

    def update_zoom_level(self):
        scale = self.canvas.scale()
        dpi = self.iface.mainWindow().physicalDpiX()
        tile_size = 256
        earth_circumference = 40075016.68557849
        meters_per_pixel = scale / (39.37 * dpi)
        zoom = log(earth_circumference / (tile_size * meters_per_pixel)) / log(2)
        self.label.setText(f"Zoom Level: {round(zoom)}")

# すでにインスタンスが存在する場合は削除（再読み込み用）
try:
    zoom_display.canvas.extentsChanged.disconnect(zoom_display.update_zoom_level)
    iface.statusBarIface().removeWidget(zoom_display.label)
except:
    pass

# 新しく表示を追加
zoom_display = ZoomLevelDisplay(iface)
