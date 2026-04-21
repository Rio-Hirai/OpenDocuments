# 画像リサイズツール使い方

`crop_to_1280x800.py` は、入力画像を左上基準で 16:10 に最大切り抜きして `1280x800` の `jpg` に変換するスクリプト

## 事前準備

Python 3.10 以上を想定  
以下をインストール

```bash
pip install pillow tkinterdnd2
```

- `pillow`：画像処理に使用
- `tkinterdnd2`：ドラッグ＆ドロップ用ウィンドウに使用

## 基本動作

### 1) ドラッグ＆ドロップGUI

引数なしで起動するとドラッグ専用ウィンドウが表示

```bash
python "crop_to_1280x800.py"
```

使い方:

1. 表示されたウィンドウに画像ファイルをドラッグ＆ドロップ
2. 同じフォルダに `-resize.jpg` を付けた名前で出力
   - 例: `sample.png` -> `sample-resize.jpg`

### 2) コマンドライン

#### 単一画像

```bash
python "crop_to_1280x800.py" "C:\path\to\input.png"
```

出力先を明示する場合：

```bash
python "crop_to_1280x800.py" "C:\path\to\input.png" -o "C:\path\to\output.jpg"
```

#### 複数画像

```bash
python "crop_to_1280x800.py" "a.png" "b.jpg" "c.webp"
```

各ファイルに対して同じ場所へ `-resize.jpg` で保存

## 変換仕様

- 切り抜き基準：入力画像の左上端固定
- アスペクト比：16:10 を維持して最大範囲を切り抜き
- 出力サイズ：`1280x800`
- 出力形式：JPG（`*.jpg`）

## 対応拡張子（GUIドロップ）

`.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif`, `.tiff`

## 想定トラブル

### `Operation cancelled by user`

`pip install tkinterdnd2` の途中キャンセルなので再実行

```bash
pip install tkinterdnd2
```

### `tkinterdnd2` が見つからないエラー

以下で導入確認

```bash
python -c "import tkinterdnd2; print('ok')"
```

必要に応じて再インストール

```bash
python -m pip install --no-cache-dir tkinterdnd2
```
