"""Verificações de entrada, isolamento do alvo e métricas publicadas."""
import io
import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
from app import app
from inferencia import infer, load_bundle


class PrototypeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df=pd.read_csv(ROOT/'demo'/'demo_final.csv')
        cls.bundle=load_bundle()
        cls.client=app.test_client()

    def test_saved_prediction_and_order(self):
        got=infer(self.df, bundle=self.bundle)
        expected=pd.read_csv(ROOT/'demo'/'gabarito_final.csv')
        np.testing.assert_allclose(got.score_fraude,expected.score_rf,rtol=1e-10,atol=1e-12)
        np.testing.assert_allclose(infer(self.df[self.df.columns[::-1]],bundle=self.bundle).score_fraude,got.score_fraude)

    def test_reject_target_missing_and_nonfinite(self):
        for df in [self.df.assign(Class=0),self.df.drop(columns='V1'),self.df.assign(Amount=np.nan),self.df.assign(Time=-1)]:
            with self.assertRaises(ValueError):infer(df,bundle=self.bundle)

    def test_threshold_monotonicity(self):
        low=infer(self.df,.1,self.bundle).classe_prevista
        high=infer(self.df,.9,self.bundle).classe_prevista
        self.assertTrue((low>=high).all())

    def test_endpoint_and_csv(self):
        r=self.client.post('/api/predict',json={'rows':self.df.head(1).to_dict('records'),'threshold':.5})
        self.assertEqual(r.status_code,200)
        result=r.get_json()
        self.assertAlmostEqual(np.mean(result['tree_scores_first']),result['rows'][0]['score_fraude'])
        r=self.client.post('/api/predict',data={'csv':(io.BytesIO(self.df.to_csv(index=False).encode()),'teste.csv')})
        self.assertEqual(r.status_code,200)
        r=self.client.post('/api/predict',json={'rows':self.df.assign(Class=0).head(1).to_dict('records')})
        self.assertEqual(r.status_code,400)
        self.assertIn('Class',r.get_json()['error'])

    def test_duplicate_headers_and_invalid_threshold(self):
        r=self.client.post('/api/predict',data={'csv':(io.BytesIO(b'Time,Time\n1,2'),'duplicado.csv')})
        self.assertEqual(r.status_code,400)
        self.assertIn('repetidos',r.get_json()['error'])
        r=self.client.post('/api/predict',json={'rows':self.df.head(1).to_dict('records'),'threshold':3})
        self.assertEqual(r.status_code,400)

    def test_published_metrics(self):
        c=json.loads((ROOT/'results'/'final'/'conclusao.json').read_text(encoding='utf-8'))
        self.assertFalse(c['test_used_for_selection'])
        self.assertFalse(c['selection']['test_evaluated_at_selection'])
        for m in c['test'].values():
            tn,fp,fn,tp=np.array(m['confusion_matrix']).ravel()
            self.assertEqual(tn+fp+fn+tp,56746)
            self.assertEqual(tp+fn,95)
            self.assertAlmostEqual(m['recall'],tp/(tp+fn))
            self.assertAlmostEqual(m['f1'],2*tp/(2*tp+fp+fn))


if __name__=='__main__':unittest.main()
