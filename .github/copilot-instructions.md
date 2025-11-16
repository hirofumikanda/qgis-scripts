# QGIS Scripts Project - AI Coding Assistant Instructions

## Project Overview
This is a collection of Python scripts designed to run within QGIS (Quantum GIS) environment. Scripts are executed directly in the QGIS Python console and have access to the global `iface` object for map canvas interaction.

## Development Environment
- **Python Path**: `C:\Program Files\QGIS 3.40.5\apps\Python312\python3.exe`
- **Key Dependencies**: PyQGIS API, PyQt5/PyQt6 for UI components
- **Execution Context**: QGIS Python Console (not standalone Python)

## Core Architecture Patterns

### Script Structure
Scripts follow a procedural pattern optimized for QGIS console execution:
```python
# Configuration constants at top
ZOOM = 10
TILE_SIZE = 256

# Helper functions for calculations
def resolution(z):
    return (2 * ORIGIN_SHIFT) / (TILE_SIZE * 2 ** z)

# Main execution logic (no if __name__ == "__main__")
canvas = iface.mapCanvas()  # Direct access to QGIS interface
```

### Coordinate System Handling
- Scripts work with Web Mercator (EPSG:3857) as the base coordinate system
- Always handle CRS transformations when canvas uses different projections:
```python
if canvas_crs != epsg3857:
    xfm = QgsCoordinateTransform(canvas_crs, epsg3857, QgsProject.instance())
    ext = xfm.transformBoundingBox(extent)
```

### Memory Layer Creation Pattern
Use QGIS memory layers for temporary/computed data:
```python
vl = QgsVectorLayer("Polygon?crs=EPSG:3857", f"layer_name", "memory")
pr = vl.dataProvider()
pr.addAttributes([QgsField("fieldname", QVariant.Int)])
vl.updateFields()
```

### Widget Management for Reloadable Scripts
Handle script reloading by cleaning up existing widgets:
```python
try:
    # Clean up previous instance
    old_instance.disconnect_signals()
    iface.statusBarIface().removeWidget(old_widget)
except:
    pass
# Create new instance
```

## Key Development Practices

### Import Strategy
- Import specific QGIS classes rather than using wildcards
- Group imports: PyQt classes, then qgis.core classes
- Web Mercator constants defined as module-level variables

### Styling and Rendering
Apply styles programmatically using QgsFillSymbol/QgsLineSymbol:
```python
symbol = QgsFillSymbol.createSimple({
    'style': 'no',                  # No fill
    'outline_color': '0,0,0',       # Black outline
    'outline_width': '0.3',         # Line width in mm
})
vl.setRenderer(QgsSingleSymbolRenderer(symbol))
```

### Map Tile Calculations
Project uses standard Web Mercator tile scheme:
- Origin shift: 20037508.342789244 (half of Web Mercator extent)
- Tile size: 256 pixels
- Resolution decreases by factor of 2 per zoom level

## Debugging and Testing
- Test scripts directly in QGIS Python Console
- Use `iface.messageBar().pushMessage()` for user feedback
- Access map canvas properties via `iface.mapCanvas()`
- Check coordinate transformations with small test extents first

## File Organization
- Scripts are standalone - no internal imports between project files
- Each script handles one specific QGIS operation
- Configuration constants at file top for easy modification