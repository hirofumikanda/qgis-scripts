# QGIS Scripts

QGISの Python コンソール内で実行するためのユーティリティスクリプト集です。地図表示やタイル操作に関する便利な機能を提供します。

## 概要

このプロジェクトは、QGIS（Quantum GIS）環境で直接実行可能なPythonスクリプトのコレクションです。各スクリプトはQGISのPythonコンソールで実行され、`iface`オブジェクトを通じてマップキャンバスとのインタラクションを行います。

## 必要な環境

- **QGIS**: 3.40.5 以上
- **Python**: 3.12（QGIS付属のPython）
- **依存関係**: PyQGIS API、PyQt5/PyQt6

## スクリプト一覧

### `create_tile_layer.py`
指定したズームレベルでのWebメルカトルタイル境界を可視化するメモリレイヤーを作成します。

**機能:**
- 現在の地図表示範囲に対応するタイル境界の表示
- EPSG:3857（Webメルカトル）座標系でのタイル計算
- カスタマイズ可能なズームレベル設定
- 透明な塗りつぶしと黒い境界線でのスタイリング

**使用方法:**
1. QGISでプロジェクトを開く
2. Pythonコンソールを開く（プラグイン → Pythonコンソール）
3. スクリプトファイルを読み込んで実行

### `display_zoom_level.py`
ステータスバーに現在のズームレベルをリアルタイム表示するウィジェットを追加します。

**機能:**
- 地図のスケールからWebメルカトルズームレベルを計算
- ステータスバーへの永続的な表示
- 地図移動・拡大縮小時の自動更新
- スクリプト再実行時の既存ウィジェット自動削除

## 開発環境設定

### VS Code設定
`.vscode/settings.json`でQGIS固有のPython環境が設定されています：

```json
{
  "python.defaultInterpreterPath": "C:\\Program Files\\QGIS 3.40.5\\apps\\Python312\\python3.exe",
  "python.analysis.extraPaths": [
    "C:\\Program Files\\QGIS 3.40.5\\apps\\qgis-ltr\\python",
    "C:\\Program Files\\QGIS 3.40.5\\apps\\Python312\\Lib\\site-packages"
  ]
}
```

## 使用方法

1. **QGISを起動**してプロジェクトを開く

2. **Pythonコンソールを開く**
   - メニューバー: `プラグイン` → `Pythonコンソール`
   - または `Ctrl+Alt+P`

3. **スクリプトを実行**
   ```python
   # ファイルから読み込んで実行
   exec(open('path/to/script.py').read())
   
   # または直接コピー&ペースト
   ```

## ライセンス

このプロジェクトはMITライセンスです。
