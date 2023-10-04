import unittest
from pathlib import Path

from phenopackets import (
    Diagnosis,
    Disease,
    Family,
    File,
    GeneDescriptor,
    GenomicInterpretation,
    Individual,
    Interpretation,
    MetaData,
    OntologyClass,
    Pedigree,
    Phenopacket,
    PhenotypicFeature,
    Resource,
    VariantInterpretation,
    VariationDescriptor,
    VcfRecord,
)
from pheval.utils.phenopacket_utils import PhenopacketUtil

from pheval_gado.prepare.create_input_data import (
    get_list_of_phenotypic_features, create_case_id_from_phenopacket,
    create_entry_for_phenopacket
)

interpretations = [
    Interpretation(
        id="test-subject-1-int",
        progress_status="SOLVED",
        diagnosis=Diagnosis(
            disease=OntologyClass(id="OMIM:219700", label="Cystic Fibrosis"),
            genomic_interpretations=[
                GenomicInterpretation(
                    subject_or_biosample_id="test-subject-1",
                    interpretation_status=4,
                    variant_interpretation=VariantInterpretation(
                        acmg_pathogenicity_classification="NOT_PROVIDED",
                        therapeutic_actionability="UNKNOWN_ACTIONABILITY",
                        variation_descriptor=VariationDescriptor(
                            gene_context=GeneDescriptor(
                                value_id="ENSG00000102302",
                                symbol="FGD1",
                                alternate_ids=[
                                    "HGNC:3663",
                                    "ncbigene:2245",
                                    "ensembl:ENSG00000102302",
                                    "symbol:FGD1",
                                ],
                            ),
                            vcf_record=VcfRecord(
                                genome_assembly="GRCh37",
                                chrom="X",
                                pos=54492285,
                                ref="C",
                                alt="T",
                            ),
                            allelic_state=OntologyClass(
                                id="GENO:0000134",
                                label="hemizygous",
                            ),
                        ),
                    ),
                ),
                GenomicInterpretation(
                    subject_or_biosample_id="test-subject-1",
                    interpretation_status=4,
                    variant_interpretation=VariantInterpretation(
                        acmg_pathogenicity_classification="NOT_PROVIDED",
                        therapeutic_actionability="UNKNOWN_ACTIONABILITY",
                        variation_descriptor=VariationDescriptor(
                            gene_context=GeneDescriptor(
                                value_id="ENSG00000176225",
                                symbol="RTTN",
                                alternate_ids=[
                                    "HGNC:18654",
                                    "ncbigene:25914",
                                    "ensembl:ENSG00000176225",
                                    "symbol:RTTN",
                                ],
                            ),
                            vcf_record=VcfRecord(
                                genome_assembly="GRCh37",
                                chrom="18",
                                pos=67691994,
                                ref="G",
                                alt="A",
                            ),
                            allelic_state=OntologyClass(
                                id="GENO:0000402", label="compound heterozygous"
                            ),
                        ),
                    ),
                ),
            ],
        ),
    )
]
phenotypic_features_with_excluded = [
    PhenotypicFeature(type=OntologyClass(id="HP:0000256", label="Macrocephaly")),
    PhenotypicFeature(type=OntologyClass(id="HP:0002059", label="Cerebral atrophy")),
    PhenotypicFeature(type=OntologyClass(id="HP:0100309", label="Subdural hemorrhage")),
    PhenotypicFeature(type=OntologyClass(id="HP:0003150", label="Glutaric aciduria")),
    PhenotypicFeature(type=OntologyClass(id="HP:0001332", label="Dystonia")),
    PhenotypicFeature(
        type=OntologyClass(id="HP:0008494", label="Inferior lens subluxation"), excluded=True
    ),
]

diseases = [Disease(term=OntologyClass(id="OMIM:219700", label="Cystic Fibrosis"))]

phenopacket_files = [
    File(
        uri="test/path/to/test_1.vcf",
        file_attributes={"fileFormat": "vcf", "genomeAssembly": "GRCh37"},
    ),
    File(
        uri="test_1.ped",
        file_attributes={"fileFormat": "PED", "genomeAssembly": "GRCh37"},
    ),
]
phenopacket_metadata = MetaData(
    created_by="pheval-converter",
    resources=[
        Resource(
            id="hp",
            name="human phenotype ontology",
            url="http://purl.obolibrary.org/obo/hp.owl",
            version="hp/releases/2019-11-08",
            namespace_prefix="HP",
            iri_prefix="http://purl.obolibrary.org/obo/HP_",
        )
    ],
    phenopacket_schema_version="2.0",
)

phenopacket = Phenopacket(
    id="test-subject",
    subject=Individual(id="test-subject-1", sex=1),
    phenotypic_features=phenotypic_features_with_excluded,
    interpretations=interpretations,
    diseases=diseases,
    files=phenopacket_files,
    meta_data=phenopacket_metadata,
)


class TestGetListOfPhenotypicFeatures(unittest.TestCase):
    def test_get_list_of_phenotypic_features(self):
        self.assertEqual(get_list_of_phenotypic_features(PhenopacketUtil(phenopacket)),
                         ['HP:0000256', 'HP:0002059', 'HP:0100309', 'HP:0003150', 'HP:0001332'])


class TestCreateCaseIDFromPhenopacket(unittest.TestCase):
    def test_create_case_id_from_phenopacket(self):
        self.assertEqual(create_case_id_from_phenopacket(Path("/path/to/Phenopacket-case-1.json")),
                         "Phenopacket-case-1")


class TestCreateEntryForPhenopacket(unittest.TestCase):
    def test_create_entry_for_phenopacket(self):
        self.assertEqual(create_entry_for_phenopacket(Path("/path/to/Phenopacket-case-1.json"), phenopacket),
                         ['Phenopacket-case-1', 'HP:0000256', 'HP:0002059', 'HP:0100309', 'HP:0003150', 'HP:0001332'])
