import json
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PowerBIArtifactTests(unittest.TestCase):
    def test_pbix_contains_model_and_three_analytic_pages(self):
        with zipfile.ZipFile(ROOT / 'powerbi/StreamView_Contenidos.pbix') as report:
            self.assertIsNone(report.testzip())
            self.assertGreater(len(report.read('DataModel')), 1000000)
            pages = json.loads(report.read('Report/definition/pages/pages.json'))
            names = [json.loads(report.read(f'Report/definition/pages/{name}/page.json'))['displayName'] for name in pages['pageOrder']]
            self.assertEqual(names, ['Contenidos y Adquisición', 'Países y participantes', 'Finanzas para adquisición'])

    def test_finance_measures_keep_paired_data_rule(self):
        model = json.loads((ROOT / 'powerbi/StreamView_Contenidos.SemanticModel/model.bim').read_text(encoding='utf-8'))
        measures = {item['name']: item['expression'] for item in model['model']['tables'][0]['measures']}
        self.assertIn('Catalogo[Finanzas]="Sí"', measures['Presupuesto total'])
        self.assertIn('Catalogo[Finanzas]="Sí"', measures['Ingresos totales'])
        self.assertIn('[Peliculas]', measures['Cobertura financiera'])
        self.assertIn('[Presupuesto total]', measures['ROI agregado'])


if __name__ == '__main__':
    unittest.main()
