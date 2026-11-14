"""Protótipo educacional local. Execute: python src/app.py."""
import csv
import io
import json
from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file

from inferencia import FEATURES, ROOT, infer, load_bundle

app = Flask(__name__, template_folder=str(ROOT/'web'), static_folder=str(ROOT/'web'/'static'))
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
BUNDLE = load_bundle()


@app.get('/')
def home():
    return render_template('index.html')


@app.get('/api/info')
def info():
    path = ROOT/'results'/'final'/'conclusao.json'
    conclusion = json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
    exp = pd.read_csv(ROOT/'results'/'final'/'experimentos.csv').to_dict('records') if conclusion else []
    sample = ROOT/'demo'/'demo_final.csv'
    data = pd.read_csv(sample if sample.exists() else ROOT/'demo'/'transacoes.csv')
    truth_path = ROOT/'demo'/'gabarito_final.csv'
    truth = pd.read_csv(truth_path) if truth_path.exists() else None
    examples = []
    for i,row in data.iterrows():
        label = f'Exemplo {i+1}'
        if truth is not None:
            t=truth.iloc[i]
            label += f" · {'fraude' if t.Class else 'normal'} no gabarito"
            if t.tipo != 'acerto': label += f' · erro {t.tipo}'
        examples.append({'name':label,'row':row.to_dict()})
    return jsonify({'features':FEATURES, 'configuration':BUNDLE.get('configuration','checkpoint_1'),
                    'threshold':BUNDLE['threshold'], 'conclusion':conclusion, 'experiments':exp,'examples':examples})


@app.post('/api/predict')
def predict():
    try:
        if 'csv' in request.files:
            text = request.files['csv'].read().decode('utf-8-sig')
            headers = next(csv.reader(io.StringIO(text)), [])
            if len(headers) != len(set(headers)):
                raise ValueError('O CSV contém cabeçalhos repetidos.')
            df = pd.read_csv(io.StringIO(text))
            threshold = float(request.form.get('threshold',.5))
        else:
            body=request.get_json(silent=True) or {}
            df=pd.DataFrame(body.get('rows', []))
            threshold=float(body.get('threshold',.5))
        result=infer(df,threshold,BUNDLE)
        X=df[BUNDLE['features']].apply(pd.to_numeric).to_numpy()
        tree_scores=[float(t.predict_proba(X[:1])[:,1][0]) for t in BUNDLE['model'].estimators_]
        return jsonify({'rows':result.to_dict('records'), 'threshold':threshold,
                        'tree_scores_first':tree_scores,'count':len(result),
                        'alerts':int(result.classe_prevista.sum())})
    except (ValueError,TypeError,KeyError,UnicodeDecodeError,pd.errors.ParserError,pd.errors.EmptyDataError) as exc:
        return jsonify({'error':str(exc)}),400


@app.get('/demo.csv')
def demo_csv():
    return send_file(ROOT/'demo'/'demo_final.csv',as_attachment=True,download_name='transacoes_demo.csv')


@app.get('/figures/<name>')
def figure(name):
    allowed={'experimentos.png','teste_matrizes.png','teste_pr.png','permutacao.png'}
    if name not in allowed:
        return jsonify({'error':'Figura inexistente.'}),404
    return send_file(ROOT/'results'/'final'/'figures'/name)


@app.errorhandler(413)
def too_large(_):
    return jsonify({'error':'O arquivo excede o limite de 3 MB.'}),413


if __name__ == '__main__':
    # Serviço apenas local, sem debug e sem recarregador.
    app.run(host='127.0.0.1',port=8501,debug=False)
