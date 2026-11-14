"""Validação comum ao protótipo e à previsão em lote."""
from pathlib import Path
import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FEATURES = ['Time'] + [f'V{i}' for i in range(1,29)] + ['Amount']


def load_bundle():
    final = ROOT / 'models' / 'final' / 'random_forest.joblib'
    return joblib.load(final if final.exists() else ROOT / 'models' / 'random_forest.joblib')


def validate(df):
    if df.columns.duplicated().any():
        raise ValueError('Há nomes de colunas repetidos.')
    missing = set(FEATURES)-set(df.columns)
    extra = set(df.columns)-set(FEATURES)
    if missing or extra:
        raise ValueError(f'Informe as 30 entradas. Ausentes: {sorted(missing)}. Extras: {sorted(extra)}. Class é o gabarito, não uma entrada.')
    if df.empty or len(df) > 5000:
        raise ValueError('Informe entre 1 e 5.000 transações por análise.')
    try:
        X = df[FEATURES].apply(pd.to_numeric,errors='raise')
    except (ValueError,TypeError):
        raise ValueError('Todas as entradas devem ser números. Use ponto como separador decimal.') from None
    if not np.isfinite(X.to_numpy(dtype=float)).all():
        raise ValueError('Há campos vazios ou valores não finitos.')
    if (X[['Time','Amount']] < 0).any().any():
        raise ValueError('Time e Amount não podem ser negativos.')
    return X


def infer(df, threshold=.5, bundle=None):
    if not np.isfinite(threshold) or not .01 <= threshold <= .99:
        raise ValueError('O limiar deve ficar entre 0,01 e 0,99.')
    X=validate(df)
    bundle=bundle or load_bundle()
    prob=bundle['model'].predict_proba(X[bundle['features']])[:,1]
    return pd.DataFrame({'score_fraude':prob,'classe_prevista':(prob>=threshold).astype(int),
                         'decisao':np.where(prob>=threshold,'REVISAR','SEM ALERTA')})
