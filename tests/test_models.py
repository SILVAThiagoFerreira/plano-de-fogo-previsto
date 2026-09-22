import re
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


MODEL_CASES = {
    "Plano de Fogo - Secundários - .xlsx": (
        "assets/modelos/Plano%20de%20Fogo%20-%20Secund%C3%A1rios%20-%20.xlsx",
        "Modelo - BLOCOS - SEM FUROS",
    ),
    "Plano de Fogo Previsto - .xlsx": (
        "assets/modelos/Plano%20de%20Fogo%20Previsto%20-%20.xlsx",
        "Plano Previsto - Produção",
    ),
}


class ModelDownloadTest(unittest.TestCase):
    def test_model_files_are_valid_xlsx_and_keep_source_names(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")

        for filename, (href, label) in MODEL_CASES.items():
            escaped_href = re.escape(href)
            escaped_filename = re.escape(filename)
            self.assertRegex(
                html,
                rf'<a class="model-option" href="{escaped_href}" download="{escaped_filename}">',
            )
            self.assertIn(f"<strong>{label}</strong>", html)

            model_path = ROOT / "assets" / "modelos" / filename
            self.assertTrue(model_path.is_file(), model_path)
            with zipfile.ZipFile(model_path) as workbook:
                self.assertIsNone(workbook.testzip(), model_path)
                self.assertIn("xl/workbook.xml", workbook.namelist())


if __name__ == "__main__":
    unittest.main()
