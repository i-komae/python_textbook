"""章末課題の Notebook をそれぞれ新しいカーネルで検証する。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient


def output_path_replacements(root: Path) -> dict[str, str]:
    """公開する出力のパス表記を、実行環境から独立させる。"""
    replacements = {}
    for path, label in (
        (root, "[教材フォルダー]"),
        (Path(sys.base_prefix), "[Python本体]"),
        (Path.home(), "[ホーム]"),
        (Path(tempfile.gettempdir()), "[一時フォルダー]"),
    ):
        for variant in (path, path.resolve()):
            if variant.is_absolute() and variant != Path(variant.anchor):
                for value in (str(variant), variant.as_posix()):
                    replacements.setdefault(value, label)
    return replacements


def sanitize_output_paths(nb, replacements: dict[str, str]) -> None:
    """テキスト出力だけを処理し、教材のソースと画像を保持する。"""
    paths = sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True)

    def replace(value):
        if isinstance(value, str):
            for path, label in paths:
                value = value.replace(path, label)
            return value
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, dict):
            return {key: replace(item) for key, item in value.items()}
        return value

    for cell in nb.cells:
        for output in cell.get("outputs", []):
            for key in ("text", "evalue", "traceback"):
                if key in output:
                    output[key] = replace(output[key])
            for mime, value in output.get("data", {}).items():
                if mime.startswith("text/") or mime == "application/json":
                    output.data[mime] = replace(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebooks", nargs="*", type=Path)
    parser.add_argument("--save", action="store_true", help="成功した実行結果を元の Notebook に保存する")
    parser.add_argument("--full", action="store_true", help="総合課題の全500日も処理する")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    paths = args.notebooks or sorted((root / "notebooks").glob("*.ipynb"))
    if not paths:
        parser.error("検証する Notebook がありません。")
    runtime = root / "build" / "notebook-validation"
    kernel_dir = runtime / "kernels" / "python3"
    kernel_dir.mkdir(parents=True, exist_ok=True)
    (kernel_dir / "kernel.json").write_text(
        json.dumps({"argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                    "display_name": "Python 3", "language": "python"}), encoding="utf-8")
    environment = os.environ.copy()
    for name, directory in {"MPLCONFIGDIR": "matplotlib", "IPYTHONDIR": "ipython",
                            "JUPYTER_RUNTIME_DIR": "jupyter"}.items():
        location = runtime / directory
        location.mkdir(exist_ok=True)
        environment[name] = str(location)
    for path in paths:
        path = path.resolve()
        nb = nbformat.read(path, as_version=4)
        nbformat.validate(nb)
        if args.full and path.stem == "13_assignment":
            for cell in nb.cells:
                if cell.cell_type == "code":
                    cell.source = cell.source.replace("RUN_FULL = False", "RUN_FULL = True")
        manager = KernelManager(kernel_name="python3", kernel_spec_manager=KernelSpecManager(
            kernel_dirs=[str(runtime / "kernels")]))
        started = time.perf_counter()
        try:
            NotebookClient(nb, km=manager, timeout=300, record_timing=False,
                           resources={"metadata": {"path": str(path.parent)}},
                           allow_errors=False).execute(env=environment)
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        if args.save:
            sanitize_output_paths(nb, output_path_replacements(root))
            nbformat.write(nb, path)
        print(f"OK {path.name} ({time.perf_counter() - started:.1f} s)", flush=True)


if __name__ == "__main__":
    main()
