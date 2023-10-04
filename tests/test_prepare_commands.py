import shutil
import tempfile
import unittest
from pathlib import Path

from pheval_gado.prepare.prepare_commands import CommandWriter, GADOProcessCLIArguments, GADOPrioritiseCLIArguments


class TestCommandWriter(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp()
        self.process_file_path = Path(self.test_dir).joinpath("process-command.txt")
        self.process_command_writer = CommandWriter(output_file=self.process_file_path)
        self.process_command_arguments = GADOProcessCLIArguments(input_output_dir=Path(self.test_dir),
                                                                 data_dir=Path("/data_dir"),
                                                                 gado_jar=Path("GADO/GADO.jar"),
                                                                 hpo_ontology=Path("hp.obo"),
                                                                 hpo_predictions_info=Path("predictions_auc_bonf.txt")
                                                                 )
        self.prioritise_file_path = Path(self.test_dir).joinpath("prioritise-command.txt")
        self.prioritise_command_writer = CommandWriter(output_file=self.prioritise_file_path)
        self.prioritise_command_arguments = GADOPrioritiseCLIArguments(input_output_dir=Path(self.test_dir),
                                                                       data_dir=Path("/data_dir"),
                                                                       gado_jar=Path("GADO/GADO.jar"),
                                                                       hpo_predictions=Path(
                                                                           "genenetwork_bonf_spiked/genenetwork_bonf_spiked.dat"),
                                                                       genes=Path("hpo_prediction_genes.txt"),
                                                                       results_dir=Path("results_dir")

                                                                       )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_write_process_command(self):
        self.process_command_writer.write_process_command(self.process_command_arguments)
        self.process_command_writer.file.close()
        with open(self.process_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, ['java -jar /data_dir/GADO/GADO.jar --mode PROCESS --output '
                                   f'{self.test_dir}/hpoProcessed.txt '
                                   '--caseHpo '
                                   f'{self.test_dir}/input_cases.txt '
                                   '--hpoOntology /data_dir/hp.obo --hpoPredictionsInfo '
                                   '/data_dir/predictions_auc_bonf.txt\n'])

    def test_write_prioritise_command(self):
        self.prioritise_command_writer.write_prioritise_command(self.prioritise_command_arguments)
        self.prioritise_command_writer.file.close()
        with open(self.prioritise_file_path) as f:
            content = f.readlines()
        f.close()
        self.assertEqual(content, ['java -jar /data_dir/GADO/GADO.jar --mode PRIORITIZE --output results_dir '
                                   '--caseHpoProcessed '
                                   f'{self.test_dir}/hpoProcessed.txt '
                                   '--genes /data_dir/hpo_prediction_genes.txt --hpoPredictions '
                                   '/data_dir/genenetwork_bonf_spiked/genenetwork_bonf_spiked.dat\n'])

    def test_close(self):
        self.prioritise_command_writer.close()
        self.assertTrue(self.prioritise_command_writer.file.closed)
        self.process_command_writer.close()
        self.assertTrue(self.process_command_writer.file.closed)
