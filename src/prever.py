"""Predicao em CSV externo com as 30 entradas do dataset ULB."""
from pathlib import Path
import argparse
import joblib
import numpy as np
import pandas as pd
from inferencia import infer

ROOT=Path(__file__).resolve().parents[1]

def predict(csv,model_path,output):
    bundle=joblib.load(model_path)  # Carregue somente modelos de origem confiavel.
    df=pd.read_csv(csv)
    out=infer(df,bundle['threshold'],bundle)
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    out.to_csv(output,index=False)
    print(out.to_string(index=False))
    print('Score do modelo nao calibrado; nao representa certeza nem autorizacao de bloqueio.')
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,default=ROOT/'demo'/'demo_final.csv')
    p.add_argument('--modelo',type=Path,default=ROOT/'models'/'final'/'random_forest.joblib')
    p.add_argument('--saida',type=Path,default=ROOT/'results'/'previsoes_demo_final.csv')
    a=p.parse_args();predict(a.csv,a.modelo,a.saida)
