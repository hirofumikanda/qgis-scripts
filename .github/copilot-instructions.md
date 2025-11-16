# QGIS Scripts Project - AI Coding Assistant Instructions

## Project Overview
This is a collection of Python scripts designed to run within QGIS (Quantum GIS) environment. Scripts are executed directly in the QGIS Python console and have access to the global `iface` object for map canvas interaction. Scripts feature real-time map interaction and event-driven architecture.

## Development Environment
- **Python Path**: `C:\Program Files\QGIS 3.40.5\apps\Python312\python3.exe`
- **Key Dependencies**: PyQGIS API, PyQt5/PyQt6 for UI components
- **Execution Context**: QGIS Python Console (not standalone Python)
- **Language**: Mixed English/Japanese - code in English, user messages in Japanese

## Core Architecture Patterns

### Event-Driven QObject Pattern
Scripts use QObject inheritance for real-time map interaction:
```python
class TileLayerManager(QObject):
    def __init__(self, iface):
        super().__init__()
        self.canvas = iface.mapCanvas()
        # Connect to map change events
        self.canvas.extentsChanged.connect(self.update_tile_layer)
        self.canvas.scaleChanged.connect(self.update_tile_layer)
    
    def disconnect_signals(self):
        """Critical cleanup method for script reloading"""
        try:
            self.canvas.extentsChanged.disconnect(self.update_tile_layer)
            self.canvas.scaleChanged.disconnect(self.update_tile_layer)
        except:
            pass
```

### Global Instance Management Pattern
Handle script reloading with global singleton cleanup:
```python
# Global variable for manager instance
tile_layer_manager = None

# Cleanup existing instance before creating new one
try:
    if tile_layer_manager:
        tile_layer_manager.disconnect_signals()
        tile_layer_manager.remove_current_layer()
except:
    pass

# Create new instance
tile_layer_manager = TileLayerManager(iface)
```

### Coordinate System Handling
- All scripts work with Web Mercator (EPSG:3857) as base coordinate system
- Always handle CRS transformations when canvas uses different projections:
```python
if canvas_crs != epsg3857:
    xfm = QgsCoordinateTransform(canvas_crs, epsg3857, QgsProject.instance())
    ext = xfm.transformBoundingBox(extent)
```

### Memory Layer Creation Pattern
Use QGIS memory layers for dynamic/computed data:
```python
vl = QgsVectorLayer("Polygon?crs=EPSG:3857", "tile_boundary", "memory")
pr = vl.dataProvider()
pr.addAttributes([QgsField("z", QVariant.Int), QgsField("x", QVariant.Int)])
vl.updateFields()
```

## Key Development Practices

### Import Strategy
- Import specific QGIS classes rather than using wildcards
- Group imports: PyQt classes first, then qgis.core classes
- Always include QObject import for event-driven scripts

### Canvas Zoom Detection
Use DPI-aware zoom level calculation from map scale:
```python
def get_canvas_zoom(iface) -> int:
    canvas = iface.mapCanvas()
    scale = canvas.scale()
    dpi = iface.mainWindow().physicalDpiX()
    meters_per_pixel = scale / (39.37 * dpi)
    z_float = math.log2((2 * ORIGIN_SHIFT) / (TILE_SIZE * meters_per_pixel))
    return int(round(z_float))
```

### Dynamic Layer Management
Layers automatically update on map changes and clean up properly:
```python
def remove_current_layer(self):
    if self.current_layer:
        QgsProject.instance().removeMapLayer(self.current_layer)
        self.current_layer = None
```

### User Interface Patterns
- Status bar widgets: `iface.statusBarIface().addPermanentWidget(widget)`
- Japanese user messages: `print("タイルレイヤを更新しました")`
- Buffer text styling for readable labels over map background

### Map Tile Calculations
Project uses standard Web Mercator tile scheme:
- Origin shift: 20037508.342789244 (half of Web Mercator extent)
- Tile size: 256 pixels, resolution decreases by factor of 2 per zoom level

## Critical Script Reloading Pattern
All scripts must handle clean reloading when re-executed in console:
```python
# At script end - cleanup pattern
try:
    if existing_instance:
        existing_instance.disconnect_signals()
        existing_instance.cleanup_resources()
except:
    pass
```

## Debugging and Testing
- Test scripts directly in QGIS Python Console
- Use `print()` with Japanese messages for user feedback
- Access map canvas properties via `iface.mapCanvas()`
- Signal/slot connections require proper disconnection for cleanup