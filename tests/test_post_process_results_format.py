import unittest

import pandas as pd
from pheval.post_processing.post_processing import PhEvalGeneResult

from pheval_gado.post_process.post_process_results_format import PhEvalGeneResultFromGADOCreator

gado_result = pd.DataFrame(
    {
        "Ensg": {
            0: "ENSG00000105607",
            1: "ENSG00000091483",
            2: "ENSG00000156709",
            3: "ENSG00000171503",
        },
        "Hgnc": {0: "GCDH", 1: "FH", 2: "AIFM1", 3: "ETFDH"},
        "Rank": {0: 1, 1: 2, 2: 3, 3: 4},
        "Zscore": {0: 8.588, 1: 8.53, 2: 8.47, 3: 8.317},
        "HP:0000256": {0: 3.0, 1: 3.0, 2: 2.67, 3: 3.0},
        "HP:0002059": {0: 3.159, 1: 3.0, 2: 3.0, 3: 1.549},
        "HP:0002170": {0: 3.0, 1: 3.0, 2: 2.98, 3: 1.622},
        "HP:0003215": {0: 5.55, 1: 5.962, 2: 5.668, 3: 7.842},
        "HP:0001332": {0: 4.494, 1: 4.111, 2: 4.621, 3: 4.585},
    }
)

gado_entry = gado_result.iloc[0]


class TestPhEvalGeneResultFromGADOCreator(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.gado_converter = PhEvalGeneResultFromGADOCreator(gado_result)

    def test__find_gene_identifier(self):
        self.assertEqual(self.gado_converter._find_gene_identifier(gado_entry), "ENSG00000105607")

    def test__find_gene_symbol(self):
        self.assertEqual(self.gado_converter._find_gene_symbol(gado_entry), "GCDH")

    def test__find_score(self):
        self.assertEqual(self.gado_converter._find_score(gado_entry), 8.588)

    def test_extract_pheval_gene_requirements(self):
        self.assertEqual(
            self.gado_converter.extract_pheval_gene_requirements(),
            [
                PhEvalGeneResult(
                    gene_symbol="GCDH", gene_identifier="ENSG00000105607", score=8.588
                ),
                PhEvalGeneResult(gene_symbol="FH", gene_identifier="ENSG00000091483", score=8.53),
                PhEvalGeneResult(
                    gene_symbol="AIFM1", gene_identifier="ENSG00000156709", score=8.47
                ),
                PhEvalGeneResult(
                    gene_symbol="ETFDH", gene_identifier="ENSG00000171503", score=8.317
                ),
            ],
        )
