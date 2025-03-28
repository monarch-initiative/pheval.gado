import unittest

import polars as pl

from pheval_gado.post_process.post_process_results_format import extract_gene_results

gado_result = pl.DataFrame(
    {
        "Ensg": ["ENSG00000105607", "ENSG00000091483", "ENSG00000156709", "ENSG00000171503"],
        "Hgnc": ["GCDH", "FH", "AIFM1", "ETFDH"],
        "Rank": [1, 2, 3, 4],
        "Zscore": [8.588, 8.53, 8.47, 8.317],
        "HP:0000256": [3.0, 3.0, 2.67, 3.0],
        "HP:0002059": [3.159, 3.0, 3.0, 1.549],
        "HP:0002170": [3.0, 3.0, 2.98, 1.622],
        "HP:0003215": [5.55, 5.962, 5.668, 7.842],
        "HP:0001332": [4.494, 4.111, 4.621, 4.585],
    }
)


class TestPostProcessResultsFormat(unittest.TestCase):
    def test_extract_gene_results(self):
        self.assertTrue(
            extract_gene_results(gado_result).equals(
                pl.DataFrame(
                    [
                        {
                            "gene_identifier": "ENSG00000105607",
                            "gene_symbol": "GCDH",
                            "score": 8.588,
                        },
                        {"gene_identifier": "ENSG00000091483", "gene_symbol": "FH", "score": 8.53},
                        {
                            "gene_identifier": "ENSG00000156709",
                            "gene_symbol": "AIFM1",
                            "score": 8.47,
                        },
                        {
                            "gene_identifier": "ENSG00000171503",
                            "gene_symbol": "ETFDH",
                            "score": 8.317,
                        },
                    ]
                )
            )
        )
