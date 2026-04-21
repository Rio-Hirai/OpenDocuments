from pathlib import Path
import argparse
import sys
import tkinter as tk
from tkinter import messagebox

from PIL import Image

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
except ImportError:
    DND_FILES = None
    TkinterDnD = None


TARGET_WIDTH = 1280
TARGET_HEIGHT = 800
TARGET_RATIO_NUM = 16
TARGET_RATIO_DEN = 10
SUPPORTED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def build_default_output_path(input_path: Path) -> Path:
    """入力画像と同じ場所に「-resize」を付けたjpgパスを返す。"""
    return input_path.with_name(f"{input_path.stem}-resize.jpg")


def crop_and_resize_to_16_10_top_left(input_path: Path, output_path: Path) -> None:
    """入力画像を左上基準で16:10に最大切り抜きし、1280x800のJPEGとして保存する。"""
    with Image.open(input_path) as img:
        src_w, src_h = img.size

        # 左上基準で16:10の切り取り範囲を最大化する
        crop_w_by_height = (src_h * TARGET_RATIO_NUM) // TARGET_RATIO_DEN
        if crop_w_by_height <= src_w:
            crop_w = crop_w_by_height
            crop_h = src_h
        else:
            crop_w = src_w
            crop_h = (src_w * TARGET_RATIO_DEN) // TARGET_RATIO_NUM

        cropped = img.crop((0, 0, crop_w, crop_h))
        resized = cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        rgb_img = resized.convert("RGB")
        rgb_img.save(output_path, format="JPEG", quality=95)


def process_paths(input_paths: list[Path], output: Path | None = None) -> None:
    """画像群を処理して出力する。"""
    if output is not None and len(input_paths) != 1:
        raise ValueError("--output は入力画像が1つのときだけ指定できます。")

    for input_path in input_paths:
        output_path = output if output is not None else build_default_output_path(input_path)
        crop_and_resize_to_16_10_top_left(input_path, output_path)


def run_drag_drop_window() -> None:
    """ドラッグ＆ドロップ専用ウィンドウを表示する。"""
    if TkinterDnD is None or DND_FILES is None:
        raise RuntimeError(
            "ドラッグ＆ドロップ機能には tkinterdnd2 が必要です。"
            " `pip install tkinterdnd2` を実行してください。"
        )

    root = TkinterDnD.Tk()
    root.title("画像リサイズ 1280x800")
    root.geometry("520x260")
    root.resizable(False, False)

    instruction = tk.Label(
        root,
        text="ここに画像ファイルをドラッグ＆ドロップしてください\n"
        "同じ場所に「-resize.jpg」で出力します",
        justify="center",
        font=("Yu Gothic UI", 11),
    )
    instruction.pack(pady=(28, 12))

    status_var = tk.StringVar(value="待機中...")
    status_label = tk.Label(root, textvariable=status_var, justify="center")
    status_label.pack(pady=(8, 12))

    drop_area = tk.Label(
        root,
        text="DROP HERE",
        relief="groove",
        width=46,
        height=7,
        bg="#f5f5f5",
    )
    drop_area.pack(padx=16, pady=8, fill="both", expand=True)

    def on_drop(event: object) -> None:
        file_list = root.tk.splitlist(getattr(event, "data", ""))
        paths = [Path(p) for p in file_list]
        image_paths = [p for p in paths if p.suffix.lower() in SUPPORTED_EXTS]

        if not image_paths:
            status_var.set("画像ファイルが見つかりませんでした。")
            return

        try:
            process_paths(image_paths)
            status_var.set(f"{len(image_paths)}件を出力しました。")
            messagebox.showinfo("完了", f"{len(image_paths)}件の画像を出力しました。")
        except Exception as exc:
            status_var.set("エラーが発生しました。")
            messagebox.showerror("エラー", str(exc))

    drop_area.drop_target_register(DND_FILES)
    drop_area.dnd_bind("<<Drop>>", on_drop)
    root.mainloop()


def main() -> None:
    if len(sys.argv) == 1:
        run_drag_drop_window()
        return

    parser = argparse.ArgumentParser(
        description="入力画像を左上基準で16:10に切り取り、1280x800のjpgに変換します。"
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="入力画像パス（複数可）")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="出力jpgパス（単一入力のときのみ指定可能）",
    )
    args = parser.parse_args()

    try:
        process_paths(args.inputs, args.output)
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
