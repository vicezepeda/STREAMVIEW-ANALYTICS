import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.prep import load_clean,explode,load_raw,clean
from src.metrics import kpis_financieros,top_generos,kpis_catalogo,rated_catalog
from src.filters import filter_catalog

class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.df=load_clean()
    def test_key_preserves_movies_and_series(self):
        self.assertEqual(len(self.df),31991)
        self.assertFalse(self.df.duplicated(['tipo','show_id']).any())
        self.assertEqual((self.df.tipo=='Película').sum(),16000)
    def test_raw_sources_reproduce_the_delivered_catalog(self):
        import pandas as pd
        rebuilt, log = clean(*load_raw())
        self.assertEqual(log['duplicados_tipo_showid_eliminados'], 9)
        pd.testing.assert_frame_equal(rebuilt, self.df, check_dtype=False, rtol=1e-10)
    def test_finance_has_paired_population_and_original_denominator(self):
        values=kpis_financieros(self.df)
        self.assertEqual(values['n'],3523)
        self.assertAlmostEqual(values['cobertura_pct'],22.01875)
        self.assertAlmostEqual(values['roi_agregado_pct'],191.6822340116041)
    def test_series_have_no_finance(self):
        self.assertEqual(kpis_financieros(filter_catalog(self.df,types=['Serie']))['n'],0)
    def test_explode_counts_unique_titles_in_category(self):
        g=top_generos(self.df).set_index('genres')
        self.assertEqual(g.loc['Drama','titulos'],14769)
        self.assertFalse(explode(self.df,'genres').duplicated(['tipo','show_id','genres']).any())
    def test_country_filter_is_exact_not_substring(self):
        self.assertTrue(filter_catalog(self.df,countries=['United']).empty)
        self.assertEqual(len(filter_catalog(self.df,countries=['United States of America'])),10955)
    def test_empty_type_selection_is_safe(self):
        self.assertTrue(filter_catalog(self.df,types=[]).empty)
    def test_rating_excludes_unrated_titles_and_popularity_uses_median(self):
        k = kpis_catalogo(self.df)
        self.assertEqual(k['calificacion_n'],27414)
        self.assertEqual(k['calificacion_cero'],4564)
        self.assertAlmostEqual(k['calificacion_media'],6.634187021230028)
        self.assertAlmostEqual(k['popularidad_mediana'],22.071)
        self.assertAlmostEqual(k['calificacion_con_votos_suficientes'],6.651343051266214)
    def test_unrated_subset_does_not_produce_a_false_zero_rating(self):
        missing=self.df[self.df.votos.eq(0)]
        self.assertTrue(rated_catalog(missing).empty)

if __name__=='__main__': unittest.main()
