import unittest

import pandas as pd

from src.processor import build_output_dataframe
from src.validator import validate_input_dataframe, validate_output_schema


class SmokeTest(unittest.TestCase):
    def test_output_schema(self):
        df = pd.DataFrame(
            {
                "Number": [1],
                "X": [10.0],
                "Y": [20.0],
                "Z": [30.0],
                "Z_Toe": [29.0],
                "Length": [1.0],
                "Azimuth": [2.0],
                "Angle": [3.0],
                "DesignCharge": [4.0],
                "Stemming": [5.0],
                "Subdrilling": [6.0],
                "DetonatingTime": [7.0],
            }
        )
        output_columns = [
            {"name": "Plano", "source": "plan_id"},
            {"name": "Tipo", "source": "plan_type_label"},
            {"name": "id", "source": "Number"},
            {"name": "y", "source": "Y"},
            {"name": "x", "source": "X"},
            {"name": "z (crest)", "source": "Z"},
            {"name": "z (toe)", "source": "Z_Toe"},
            {"name": "profundidade prevista", "source": "Length"},
            {"name": "azimute", "source": "Azimuth"},
            {"name": "inclinacao", "source": "Angle"},
            {"name": "cargas previstas", "source": "DesignCharge"},
            {"name": "tampao previsto", "source": "Stemming"},
            {"name": "subperfuracao", "source": "Subdrilling"},
            {"name": "DetonatingTime", "source": "DetonatingTime"},
        ]
        result = build_output_dataframe(df, output_columns, "0190326", "Production", 1)
        validate_output_schema(list(result.columns), [item["name"] for item in output_columns])
        self.assertEqual(result.iloc[0]["Plano"], "0190326")
        self.assertEqual(result.iloc[0]["Tipo"], "Production")

    def test_rejects_zero_number(self):
        df = pd.DataFrame(
            {
                "Number": [0],
                "X": [10.0],
                "Y": [20.0],
                "Z": [30.0],
                "Z_Toe": [29.0],
                "Length": [1.0],
                "Azimuth": [2.0],
                "Angle": [3.0],
                "DesignCharge": [4.0],
                "Stemming": [5.0],
                "Subdrilling": [6.0],
                "DetonatingTime": [7.0],
            }
        )

        with self.assertRaises(ValueError):
            validate_input_dataframe(
                df,
                [
                    "Number",
                    "X",
                    "Y",
                    "Z",
                    "Z_Toe",
                    "Length",
                    "Azimuth",
                    "Angle",
                    "DesignCharge",
                    "Stemming",
                    "Subdrilling",
                    "DetonatingTime",
                ],
            )


if __name__ == "__main__":
    unittest.main()
