import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
APP=Path(__file__).resolve().parents[1]/'dashboard/dashboard.py'
class ExecutiveAppTests(unittest.TestCase):
    def app(self):return AppTest.from_file(str(APP),default_timeout=45).run()
    def test_initial_load_and_empty_selection(self):
        app=self.app();self.assertEqual(len(app.exception),0)
        self.assertEqual(app.metric[0].value,'31,991')
        by_label={m.label:m.value for m in app.metric}
        self.assertEqual(by_label['Popularidad mediana'],'22.07')
        self.assertEqual(by_label['Calificación con votos'],'6.63 / 10')
        app.multiselect(key='tipos').set_value([]).run()
        self.assertEqual(len(app.exception),0)
        self.assertGreater(len(app.warning),0)
    def test_filter_movies_and_reset(self):
        app=self.app();app.multiselect(key='tipos').set_value(['Película']).run()
        self.assertEqual(len(app.exception),0);self.assertEqual(app.metric[0].value,'16,000')
        app.button(key='limpiar').click().run()
        self.assertEqual(app.metric[0].value,'31,991')
    def test_genre_filter_agrees_with_unique_pbix_count(self):
        app=self.app();app.multiselect(key='generos').set_value(['Drama']).run()
        self.assertEqual(len(app.exception),0);self.assertEqual(app.metric[0].value,'14,769')
    def test_genre_sample_threshold_handles_empty_results(self):
        app=self.app();app.number_input(key='min_genero').set_value(2000).run()
        self.assertEqual(len(app.exception),0)
        app.multiselect(key='tipos').set_value(['Serie']).run()
        app.multiselect(key='generos').set_value(['Documentary']).run()
        self.assertEqual(len(app.exception),0)
        self.assertTrue(any('Ningún género' in x.value for x in app.info))
if __name__=='__main__':unittest.main()
