"""Predicao em CSV externo com as 30 entradas do dataset ULB."""
from pathlib import Path
import argparse
import joblib
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]

def predict(csv,model_path,output):
    bundle=joblib.load(model_path)  # Carregue somente modelos de origem confiavel.
    df=pd.read_csv(csv);features=bundle['features']
    missing=set(features)-set(df.columns)
    extras=set(df.columns)-set(features)
    if missing or extras: raise ValueError(f'Colunas ausentes: {sorted(missing)}; extras: {sorted(extras)}. Class nao e entrada.')
    X=df[features].apply(pd.to_numeric,errors='raise')
    if X.empty or not np.isfinite(X.to_numpy()).all(): raise ValueError('CSV vazio ou com valores ausentes/nao finitos.')
    prob=bundle['model'].predict_proba(X)[:,1]
    out=pd.DataFrame({'score_fraude':prob,'classe_prevista':(prob>=bundle['threshold']).astype(int)})
    out['decisao']=np.where(out.classe_prevista==1,'POSSIVEL FRAUDE','TRANSACAO NORMAL')
    out.to_csv(output,index=False)
    print(out.to_string(index=False))
    print('Score do modelo nao calibrado; nao representa certeza nem autorizacao de bloqueio.')
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,default=ROOT/'demo'/'transacoes.csv')
    p.add_argument('--modelo',type=Path,default=ROOT/'models'/'random_forest.joblib')
    p.add_argument('--saida',type=Path,default=ROOT/'results'/'previsoes_demo.csv')
    a=p.parse_args();predict(a.csv,a.modelo,a.saida)
