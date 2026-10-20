"""章末課題の Notebook をそれぞれ新しいカーネルで検証する。"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient


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
                           resources={"metadata": {"path": str(root)}},
                           allow_errors=False).execute(env=environment)
        finally:
            if manager.has_kernel:
                manager.shutdown_kernel(now=True)
        if args.save:
            nbformat.write(nb, path)
        print(f"OK {path.name} ({time.perf_counter() - started:.1f} s)", flush=True)


if __name__ == "__main__":
    main()
