"""Empacota código e materiais, sem .git, ambiente virtual ou dataset completo."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
TEXT={'.py','.md','.json','.csv','.txt','.ps1','.bat','.html','.css','.js','.cjs','.yml','.yaml'}


def content(path):
    data=path.read_bytes()
    return data.replace(b'\r\n',b'\n') if path.suffix.lower() in TEXT or path.name in {'.gitignore','.gitattributes'} else data


def main():
    result=subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=ROOT,capture_output=True,check=True)
    names=sorted(set(x for x in result.stdout.decode('utf-8').split('\0') if x and x!='manifesto_sha256.json'))
    payload={name:content(ROOT/name) for name in names if (ROOT/name).is_file()}
    manifest={'normalizacao':'CRLF para LF nos arquivos de texto, igual ao pacote ZIP e ao checkout Git em LF.',
              'arquivos':{name:hashlib.sha256(data).hexdigest() for name,data in payload.items()}}
    path=ROOT/'manifesto_sha256.json'
    path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    archive=ROOT.parent/'Pacote_Final_Random_Forest.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,data in payload.items():z.writestr('random_forest/'+name,data)
        z.write(path,'random_forest/manifesto_sha256.json')
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,digest in manifest['arquivos'].items():
            assert hashlib.sha256(z.read('random_forest/'+name)).hexdigest()==digest,name
    print(f'Pacote verificado: {archive} ({archive.stat().st_size:,} bytes, {len(payload)+1} arquivos)')


if __name__=='__main__':main()
