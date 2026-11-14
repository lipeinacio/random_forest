"""Experimentos finais com seleção na validação e teste intocado até a decisão.

Execute uma vez: python src/finalizar.py. Uma execução concluída é reutilizada.
O pipeline de Checkpoint 1 e seus resultados permanecem preservados.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import time
from datetime import datetime, timezone

import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split

from pipeline import FEATURES, ROOT, SEED, scores, write_json
from baixar_dados import EXPECTED_SHA256

OUT = ROOT / 'results' / 'final'
FIG = OUT / 'figures'
PLAN = {
    'seed': SEED, 'threshold': 0.5,
    'selection': 'Maior F1 da classe fraude na validacao com limiar 0.5; desempate por AP e ID.',
    'frozen_test': 'Somente modelo escolhido e baseline sao avaliados no teste, apos gravar a decisao.',
    'experiments': [
        {'id': 'E1', 'hypothesis': 'Retirar balanced pode reduzir falsos alertas, com possivel perda de recall.',
         'change': 'class_weight: balanced -> None', 'variant': 'sem_pesos'},
        {'id': 'E2', 'hypothesis': 'Profundidade 6 pode reduzir sobreajuste, mas perder fraudes complexas.',
         'change': 'max_depth: 12 -> 6', 'variant': 'profundidade_6'},
        {'id': 'E3', 'hypothesis': 'Remover V17, V14 e V12 pode reduzir F1/AP por retirar sinais destacados na EDA de treino.',
         'change': 'Remover apenas V17, V14 e V12 das entradas', 'variant': 'sem_top3'},
    ],
    'variants': ['referencia', 'sem_pesos', 'profundidade_6', 'sem_top3'],
    'limits': 'Uma semente e uma divisao. Sem busca exaustiva, calibracao ou validacao temporal.'
}


def wilson(k, n):
    z = 1.959963984540054
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n))/d
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return [float(c-h), float(c+h)]


def run(output_dir=None, model_dir=None, export_demo=True):
    global OUT, FIG
    if output_dir is not None:
        OUT = Path(output_dir).resolve()
        FIG = OUT / 'figures'
    if (OUT / 'conclusao.json').exists():
        print('Execucao final ja concluida. Reutilizando resultados, sem nova selecao pelo teste.')
        return
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(exist_ok=True)
    model_dir = Path(model_dir).resolve() if model_dir is not None else ROOT / 'models' / 'final'
    model_dir.mkdir(exist_ok=True)
    plan_path = OUT / 'plano_pre_execucao.json'
    if not plan_path.exists():
        write_json(plan_path, {**PLAN, 'registered_at_utc': datetime.now(timezone.utc).isoformat()})
    else:
        prior = json.loads(plan_path.read_text(encoding='utf-8'))
        assert prior['experiments'] == PLAN['experiments'], 'Plano mudou. Nao reutilize teste para refinar o plano.'
    path = ROOT / 'data' / 'creditcard.csv'
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256, 'Dataset diferente da versao registrada.'
    raw = pd.read_csv(path)
    clean = raw.drop_duplicates().copy()
    assert list(clean.columns) == FEATURES + ['Class']
    assert np.isfinite(clean.to_numpy()).all()
    X, y = clean[FEATURES], clean.Class
    train_id, test_id = train_test_split(clean.index, test_size=.20, random_state=SEED, stratify=y)
    train_id, val_id = train_test_split(train_id, test_size=.25, random_state=SEED, stratify=y.loc[train_id])
    hashes = [set(pd.util.hash_pandas_object(X.loc[ix], index=False)) for ix in [train_id, val_id, test_id]]
    assert all(not(hashes[i] & hashes[j]) for i in range(3) for j in range(i+1, 3))
    common = dict(n_estimators=100, max_depth=12, min_samples_leaf=2,
                  class_weight='balanced', random_state=SEED, n_jobs=4)
    configs = {
        'referencia': (common, FEATURES),
        'sem_pesos': ({**common, 'class_weight': None}, FEATURES),
        'profundidade_6': ({**common, 'max_depth': 6}, FEATURES),
        'sem_top3': (common, [f for f in FEATURES if f not in ['V17', 'V14', 'V12']]),
    }
    models, validation, rows = {}, {}, []
    for ident, (params, features) in configs.items():
        print(f'Treinando {ident}...', flush=True)
        started = time.perf_counter()
        model = RandomForestClassifier(**params).fit(X.loc[train_id, features], y.loc[train_id])
        prob = model.predict_proba(X.loc[val_id, features])[:, 1]
        result = scores(y.loc[val_id], (prob >= .5).astype(int), prob)
        result.update(train_seconds=time.perf_counter()-started, features=features, params=params)
        models[ident] = model
        validation[ident] = result
        tn, fp, fn, tp = np.asarray(result['confusion_matrix']).ravel()
        rows.append({'configuracao': ident, **{k: result[k] for k in ['precision','recall','f1','average_precision']},
                     'TN': int(tn), 'FP': int(fp), 'FN': int(fn), 'TP': int(tp)})
    original = json.loads((ROOT / 'results' / 'metricas_validacao.json').read_text(encoding='utf-8'))
    for metric in ['precision', 'recall', 'f1', 'average_precision']:
        assert abs(validation['referencia'][metric]-original['Random Forest'][metric]) < 1e-10, f'Reproducao divergente: {metric}'
    write_json(OUT / 'validacao.json', validation)
    pd.DataFrame(rows).to_csv(OUT / 'experimentos.csv', index=False)
    selected = sorted(validation, key=lambda k: (-validation[k]['f1'], -validation[k]['average_precision'], k))[0]
    features = configs[selected][1]
    winner = models[selected]
    decision = {'selected': selected, 'threshold': .5, 'selection_set': 'validacao',
                'selected_at_utc': datetime.now(timezone.utc).isoformat(),
                'test_evaluated_at_selection': False, 'features': features,
                'plan_sha256': hashlib.sha256(plan_path.read_bytes()).hexdigest(),
                'criterion': PLAN['selection']}
    write_json(OUT / 'decisao_antes_do_teste.json', decision)
    bundle = {'model': winner, 'features': features, 'threshold': .5, 'seed': SEED,
              'sklearn_version': sklearn.__version__, 'configuration': selected}
    joblib.dump(bundle, model_dir / 'random_forest.joblib', compress=3)
    # Somente agora o teste e avaliado. Nenhum ajuste posterior usa seus resultados.
    tree_bundle = joblib.load(ROOT / 'models' / 'arvore.joblib')
    tests, predictions = {}, {}
    for name, model, fs in [('Random Forest final', winner, features),
                            ('Arvore de Decisao', tree_bundle['model'], tree_bundle['features'])]:
        prob = model.predict_proba(X.loc[test_id, fs])[:, 1]
        pred = (prob >= .5).astype(int)
        tests[name] = scores(y.loc[test_id], pred, prob)
        predictions[name] = prob
    tests['Sempre normal'] = scores(y.loc[test_id], np.zeros(len(test_id),dtype=int), np.zeros(len(test_id)))
    rf = tests['Random Forest final']
    tn, fp, fn, tp = np.array(rf['confusion_matrix']).ravel()
    rf['precision_ci95_wilson'] = wilson(tp, tp+fp)
    rf['recall_ci95_wilson'] = wilson(tp, tp+fn)
    # Bootstrap estratificado do teste para incerteza, sem retreino e sem selecao.
    rng = np.random.default_rng(SEED)
    yy = y.loc[test_id].to_numpy()
    pp = predictions['Random Forest final']
    groups = [np.flatnonzero(yy == c) for c in [0, 1]]
    f1s = []
    for _ in range(1000):
        ix = np.concatenate([rng.choice(g, len(g), replace=True) for g in groups])
        truth, pred = yy[ix], pp[ix] >= .5
        bt = np.sum((truth == 1) & pred); bf = np.sum((truth == 0) & pred); bn = np.sum((truth == 1) & ~pred)
        f1s.append(2*bt/(2*bt+bf+bn))
    rf['f1_ci95_bootstrap_stratified'] = np.quantile(f1s, [.025, .975]).tolist()
    write_json(OUT / 'teste.json', tests)
    # Casos concretos da validacao, para explicacao e demonstracao (nao e teste).
    prob = winner.predict_proba(X.loc[val_id, features])[:, 1]
    evaluated = clean.loc[val_id].copy()
    evaluated.insert(0, 'linha_original', val_id)
    evaluated['score_rf'] = prob
    evaluated['previsto_rf'] = (prob >= .5).astype(int)
    evaluated['tipo'] = np.select([(evaluated.Class==1)&(prob<.5),(evaluated.Class==0)&(prob>=.5)], ['FN','FP'], default='acerto')
    cases = pd.concat([evaluated[evaluated.tipo=='FN'].sort_values('score_rf').head(2),
                       evaluated[evaluated.tipo=='FP'].sort_values('score_rf',ascending=False).head(2)])
    cases.to_csv(OUT / 'casos_erros.csv', index=False)
    sample = pd.concat([evaluated[(evaluated.Class==0)&(evaluated.previsto_rf==0)].head(3),
                        evaluated[(evaluated.Class==1)&(evaluated.previsto_rf==1)].head(3), cases.head(4)])
    if export_demo:
        sample[FEATURES].to_csv(ROOT / 'demo' / 'demo_final.csv', index=False)
        sample[['linha_original','Class','score_rf','previsto_rf','tipo']].to_csv(ROOT / 'demo' / 'gabarito_final.csv', index=False)
    pd.Series(winner.feature_importances_, index=features).sort_values(ascending=False).rename('importancia_impureza').to_csv(OUT / 'importancia_impureza.csv')
    # Importancia por permutacao na validacao completa. Mede perda em AP, sem dar causalidade.
    perm = permutation_importance(winner, X.loc[val_id, features], y.loc[val_id],
                                  scoring='average_precision', n_repeats=3, random_state=SEED, n_jobs=1)
    importance = pd.DataFrame({'variavel':features, 'queda_AP_media':perm.importances_mean,
                               'desvio_3_repeticoes':perm.importances_std}).sort_values('queda_AP_media',ascending=False)
    importance.to_csv(OUT / 'importancia_permutacao.csv', index=False)
    plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':11, 'figure.dpi':180,
                         'axes.spines.top':False, 'axes.spines.right':False})
    f,a = plt.subplots(figsize=(9,4.4))
    vals = pd.DataFrame(rows)
    pos = np.arange(len(vals)); w=.25
    for i,(col,label,color) in enumerate([('precision','Precisão','#145a73'),('recall','Recall','#cc6c38'),('f1','F1','#287b68')]):
        a.bar(pos+(i-1)*w, vals[col], w, label=label, color=color)
    a.set_xticks(pos, ['Referência','Sem pesos','Profundidade 6','Sem V17/V14/V12'])
    a.set_ylim(0,1.12); a.set_ylabel('Classe fraude'); a.legend(ncol=3,frameon=False)
    a.set_title('Experimentos controlados na validação'); f.tight_layout(); f.savefig(FIG/'experimentos.png'); plt.close(f)
    f,axes = plt.subplots(1,2,figsize=(9,4.2))
    for a,name in zip(axes,['Arvore de Decisao','Random Forest final']):
        cm=np.array(tests[name]['confusion_matrix']); a.imshow(np.log1p(cm),cmap='Blues')
        for (i,j),v in np.ndenumerate(cm): a.text(j,i,str(v),ha='center',va='center',fontsize=15,color='white' if v>1000 else '#18323d')
        a.set_xticks([0,1],['Normal','Fraude']); a.set_yticks([0,1],['Normal','Fraude']); a.set_xlabel('Previsto');a.set_ylabel('Real');a.set_title(name)
    f.suptitle('Avaliação final no teste reservado');f.tight_layout();f.savefig(FIG/'teste_matrizes.png');plt.close(f)
    f,a=plt.subplots(figsize=(8,4.2))
    for name,color in [('Arvore de Decisao','#cc6c38'),('Random Forest final','#145a73')]:
        p,r,_=precision_recall_curve(yy,predictions[name]);a.step(r,p,where='post',label=f'{name} (AP={tests[name]["average_precision"]:.3f})',color=color)
    a.set(xlabel='Recall',ylabel='Precisão',xlim=(0,1.01),ylim=(0,1.03));a.legend(frameon=False);a.set_title('Precision–Recall no teste');f.tight_layout();f.savefig(FIG/'teste_pr.png');plt.close(f)
    top=importance.head(10).sort_values('queda_AP_media')
    f,a=plt.subplots(figsize=(8,4.2));a.barh(top.variavel,top.queda_AP_media,xerr=top.desvio_3_repeticoes,color='#145a73')
    a.set_xlabel('Queda de Average Precision ao embaralhar a variável');a.set_title('Importância por permutação na validação');f.tight_layout();f.savefig(FIG/'permutacao.png');plt.close(f)
    conclusion = {'selection':decision, 'raw_rows':len(raw), 'clean_rows':len(clean), 'sha256':digest,
        'splits':{k:{'rows':len(ix),'frauds':int(y.loc[ix].sum())} for k,ix in [('treino',train_id),('validacao',val_id),('teste',test_id)]},
        'validation':validation[selected], 'test':tests, 'errors_validation':cases[['linha_original','Class','Amount','score_rf','previsto_rf','tipo']].to_dict('records'),
        'environment':{'python':platform.python_version(),'sklearn':sklearn.__version__,'numpy':np.__version__,'pandas':pd.__version__},
        'completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'reference_reproduced':True, 'test_used_for_selection':False,
        'uncertainty':'Wilson 95% para precisao/recall. Bootstrap estratificado 1000 repeticoes para F1, condicional a esta divisao e modelo fixos. Nao mede drift ou variacao entre treinos.'}
    write_json(OUT/'conclusao.json',conclusion)
    print(f'Selecionado somente pela validacao: {selected}',flush=True)
    print(json.dumps(tests,ensure_ascii=False,indent=2),flush=True)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--saida',type=Path,help='Diretorio separado para reproduzir as mesmas decisoes.')
    parser.add_argument('--modelos',type=Path,help='Diretorio separado para modelos reproduzidos.')
    parser.add_argument('--nao-exportar-demo',action='store_true',help='Preservar os exemplos da entrega.')
    args=parser.parse_args()
    if args.saida is not None and args.modelos is None:
        parser.error('Ao reproduzir com --saida, informe --modelos para preservar o modelo entregue.')
    run(args.saida,args.modelos,not args.nao_exportar_demo)
