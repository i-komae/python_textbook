"""Notebook の公開用出力から環境固有のパスを除けることを確認する。"""

import contextlib
import copy
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import check_notebooks
import nbformat


class OutputPathTests(unittest.TestCase):
    def test_text_paths_change_but_sources_values_and_images_remain(self):
        root = "/home/student/textbook"
        image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB"
        nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(
            f'print("{root}")', execution_count=1, outputs=[
                nbformat.v4.new_output("stream", name="stdout", text=f"{root}/data.csv\n66\n"),
                nbformat.v4.new_output("display_data", data={
                    "text/plain": f"Csv SCAN [{root}/data.csv]",
                    "text/html": f"<pre>{root}/data.csv</pre>",
                    "application/json": {"path": f"{root}/data.csv", "count": 12033},
                    "image/png": image,
                }),
                nbformat.v4.new_output("error", ename="OSError",
                                      evalue=f"{root}/missing.csv",
                                      traceback=[f"File {root}/example.py"]),
            ])])
        original = copy.deepcopy(nb)
        check_notebooks.sanitize_output_paths(nb, {
            "/home/student": "[ホーム]", root: "[教材フォルダー]"})
        outputs = nb.cells[0].outputs
        self.assertEqual(outputs[0].text, "[教材フォルダー]/data.csv\n66\n")
        self.assertEqual(outputs[1].data["text/plain"], "Csv SCAN [[教材フォルダー]/data.csv]")
        self.assertEqual(outputs[1].data["text/html"], "<pre>[教材フォルダー]/data.csv</pre>")
        self.assertEqual(outputs[1].data["application/json"], {
            "path": "[教材フォルダー]/data.csv", "count": 12033})
        self.assertEqual(outputs[1].data["image/png"], image)
        self.assertEqual(outputs[2].evalue, "[教材フォルダー]/missing.csv")
        self.assertEqual(outputs[2].traceback, ["File [教材フォルダー]/example.py"])
        self.assertEqual(nb.cells[0].source, original.cells[0].source)
        self.assertEqual(nb.cells[0].execution_count, original.cells[0].execution_count)
        self.assertEqual(nb.metadata, original.metadata)
        once = copy.deepcopy(nb)
        check_notebooks.sanitize_output_paths(nb, {root: "[教材フォルダー]"})
        self.assertEqual(nb, once)

    def test_windows_output(self):
        nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell(outputs=[
            nbformat.v4.new_output("stream", name="stdout", text=r"C:\Users\student\book\.venv\Scripts\python.exe")])])
        check_notebooks.sanitize_output_paths(nb, {r"C:\Users\student\book": "[教材フォルダー]"})
        self.assertEqual(nb.cells[0].outputs[0].text, r"[教材フォルダー]\.venv\Scripts\python.exe")

    def test_save_sanitizes_executed_output(self):
        root = Path(check_notebooks.__file__).resolve().parents[1]
        runtime = root / "build" / "notebook-validation"
        runtime.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=runtime) as directory:
            path = Path(directory) / "example.ipynb"
            nbformat.write(nbformat.v4.new_notebook(cells=[
                nbformat.v4.new_code_cell("print(12033)")]), path)

            def execute(client_nb, **kwargs):
                client_nb.cells[0].execution_count = 1
                client_nb.cells[0].outputs = [nbformat.v4.new_output(
                    "stream", name="stdout", text=f"{root}/data.csv\n12033\n")]
                return Mock(execute=lambda **kwargs: client_nb)

            with patch.object(check_notebooks, "NotebookClient", side_effect=execute), \
                    patch.object(check_notebooks, "KernelManager") as manager, \
                    patch("sys.argv", ["check_notebooks.py", "--save", str(path)]), \
                    contextlib.redirect_stdout(io.StringIO()):
                manager.return_value.has_kernel = False
                check_notebooks.main()
            saved = nbformat.read(path, as_version=4)
            nbformat.validate(saved)
            self.assertEqual(saved.cells[0].source, "print(12033)")
            self.assertEqual(saved.cells[0].outputs[0].text, "[教材フォルダー]/data.csv\n12033\n")


if __name__ == "__main__":
    unittest.main()
