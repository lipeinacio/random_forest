"""Download publico do dataset original da ULB no Kaggle, sem credenciais."""
from pathlib import Path
import hashlib
import shutil
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
EXPECTED_SHA256='76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89'

def main():
    data=ROOT/'data';data.mkdir(exist_ok=True)
    csv=data/'creditcard.csv'
    if not csv.exists():
        dest=data/'creditcard.zip'
        print('Baixando a versao original da ULB no Kaggle...',flush=True)
        with urllib.request.urlopen('https://www.kaggle.com/api/v1/datasets/download/mlg-ulb/creditcardfraud',timeout=120) as src, dest.open('wb') as dst:
            shutil.copyfileobj(src,dst)
        with zipfile.ZipFile(dest) as z:
            name=next(n for n in z.namelist() if n.endswith('creditcard.csv'))
            with z.open(name) as src,csv.open('wb') as dst:shutil.copyfileobj(src,dst)
        dest.unlink()
    actual=hashlib.sha256(csv.read_bytes()).hexdigest()
    if actual!=EXPECTED_SHA256:
        raise ValueError('Arquivo diferente da versao analisada. Confira a origem e a versao antes de prosseguir.')
    print(f'Verificado: {csv}\nSHA-256: {actual}')

if __name__=='__main__':main()
