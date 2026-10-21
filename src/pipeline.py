"""Checkpoint 1: auditoria, EDA, treino e avaliacao reproduziveis.

Execute da raiz do projeto: python src/pipeline.py --data data/creditcard.csv
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
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, average_precision_score, confusion_matrix,
                             f1_score, precision_recall_curve, precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

FEATURES = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
ROOT = Path(__file__).resolve().parents[1]
SEED = 42

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def scores(y, pred, probability):
    return dict(precision=float(precision_score(y,pred,zero_division=0)),
                recall=float(recall_score(y,pred,zero_division=0)),
                f1=float(f1_score(y,pred,zero_division=0)),
                average_precision=float(average_precision_score(y,probability)),
                accuracy=float(accuracy_score(y,pred)),
                confusion_matrix=confusion_matrix(y,pred,labels=[0,1]).tolist())

def run(path):
    out=ROOT/'results'; fig=out/'figures'; models=ROOT/'models'; demo=ROOT/'demo'
    for p in [out,fig,models,demo]: p.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(path)
    assert list(raw.columns)==FEATURES+['Class'], 'Esquema diferente do dataset original.'
    assert set(raw.Class.unique())=={0,1}, 'Rotulos inesperados.'
    assert raw.isna().sum().sum()==0, 'Valores ausentes exigem uma decisao de tratamento.'
    assert np.isfinite(raw.to_numpy()).all(), 'Valores nao finitos.'
    duplicate_mask=raw.duplicated(keep='first')
    # Decisao conservadora: remove copias identicas antes de dividir, evitando
    # a mesma observacao em treino e avaliacao. Nao identifica clientes/cartoes.
    clean=raw.loc[~duplicate_mask].copy()
    X=clean[FEATURES]; y=clean.Class
    train_id, test_id=train_test_split(clean.index,test_size=.20,random_state=SEED,stratify=y)
    train_id, val_id=train_test_split(train_id,test_size=.25,random_state=SEED,stratify=y.loc[train_id])
    ids={'treino':train_id,'validacao':val_id,'teste':test_id}
    assert not(set(train_id)&set(test_id) or set(train_id)&set(val_id) or set(val_id)&set(test_id))
    hashes={k:set(pd.util.hash_pandas_object(X.loc[v],index=False).tolist()) for k,v in ids.items()}
    assert not(hashes['treino']&hashes['teste'] or hashes['treino']&hashes['validacao'] or hashes['validacao']&hashes['teste'])
    pd.DataFrame([{'linha_original':int(i),'conjunto':k} for k,v in ids.items() for i in v]).to_csv(out/'divisao.csv',index=False)
    # EDA apenas no treino. Teste permanece reservado aos experimentos finais.
    tr=clean.loc[train_id]
    tr.describe().to_csv(out/'estatisticas_treino.csv')
    tr.groupby('Class').Amount.describe().to_csv(out/'amount_por_classe_treino.csv')
    q1,q3=tr[FEATURES].quantile(.25),tr[FEATURES].quantile(.75)
    iqr=q3-q1
    flags=(tr[FEATURES].lt(q1-1.5*iqr)|tr[FEATURES].gt(q3+1.5*iqr)).sum()
    flags.rename('fora_limites_1_5_IQR').to_csv(out/'outliers_treino.csv')
    standardized_gap=((tr[tr.Class==1][FEATURES].mean()-tr[tr.Class==0][FEATURES].mean())/tr[FEATURES].std()).abs().sort_values(ascending=False)
    standardized_gap.rename('diferenca_medias_em_desvios_treino').to_csv(out/'diferencas_classes_treino.csv')
    corr=tr[FEATURES].corr()
    mask=np.triu(np.ones(corr.shape,dtype=bool),k=1)
    pairs=corr.where(mask).stack().sort_values(key=lambda s:s.abs(),ascending=False)
    pairs.rename('correlacao_pearson').to_csv(out/'correlacoes_treino.csv')
    amount={str(int(c)):{'n':int(len(g)),'media':float(g.Amount.mean()),'mediana':float(g.Amount.median()),
                       'p95':float(g.Amount.quantile(.95)),'maximo':float(g.Amount.max())}
            for c,g in tr.groupby('Class')}
    audit=dict(raw_rows=len(raw),raw_columns=len(raw.columns),input_features=len(FEATURES),
               raw_class_counts={str(int(k)):int(v) for k,v in raw.Class.value_counts().items()},
               missing_values=int(raw.isna().sum().sum()),duplicates_removed=int(duplicate_mask.sum()),
               duplicates_removed_by_class={str(int(k)):int(v) for k,v in raw.loc[duplicate_mask].Class.value_counts().items()},
               clean_rows=len(clean),clean_class_counts={str(int(k)):int(v) for k,v in clean.Class.value_counts().items()},
               categorical_features=[],normalization='Nao aplicada: ambos os modelos dividem cada variavel por limiares; escala considerada.',
               outlier_policy='Investigar por IQR no treino; preservar extremos, pois podem ser sinais de fraude.',
               amount_train=amount,top_class_gaps=standardized_gap.head(5).to_dict(),
               largest_correlation=dict(feature_a=pairs.index[0][0],feature_b=pairs.index[0][1],value=float(pairs.iloc[0])),
               time_range_seconds=[float(raw.Time.min()),float(raw.Time.max())],
               splits={k:{'rows':len(v),'frauds':int(y.loc[v].sum())} for k,v in ids.items()},
               sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),
               leakage_checks={'target_excluded':True,'row_ids_disjoint':True,'feature_hashes_disjoint':True,'eda_train_only':True,
                               'test_evaluated':False,'original_pca_fit_scope':'Nao informado pelos autores; transformacao ja fornecida.'})
    write_json(out/'auditoria.json',audit)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':160})
    f,a=plt.subplots(figsize=(7,3.5)); counts=raw.Class.value_counts().sort_index()
    a.bar(['Normal','Fraude'],counts,color=['#35658a','#b34d46']);a.set_yscale('log');a.set_ylabel('Transações (escala log)')
    for i,v in enumerate(counts): a.text(i,v*1.12,f'{v:,}'.replace(',','.'),ha='center')
    a.set_ylim(100,1_000_000);a.set_title('Fraudes são uma pequena fração da base original');f.tight_layout();f.savefig(fig/'01_classes.png');plt.close(f)
    f,a=plt.subplots(figsize=(7,3.5))
    for c,label,color in [(0,'Normal','#35658a'),(1,'Fraude','#b34d46')]:
        a.hist(np.log1p(tr.loc[tr.Class==c,'Amount']),bins=45,density=True,alpha=.50,label=label,color=color)
    a.set_xlabel('log(1 + Amount)');a.set_ylabel('Densidade por classe');a.set_title('Valores das transações no treino');a.legend();f.tight_layout();f.savefig(fig/'02_amount.png');plt.close(f)
    top=standardized_gap.head(6).sort_values()
    f,a=plt.subplots(figsize=(7,3.5));a.barh(top.index,top,color='#35658a');a.set_xlabel('|Diferença das médias| / desvio padrão do treino');a.set_title('Diferenças descritivas entre classes no treino');f.tight_layout();f.savefig(fig/'03_variaveis.png');plt.close(f)
    estimators={
        'Sempre normal':DummyClassifier(strategy='most_frequent'),
        'Arvore de Decisao':DecisionTreeClassifier(max_depth=12,min_samples_leaf=2,class_weight='balanced',random_state=SEED),
        'Random Forest':RandomForestClassifier(n_estimators=100,max_depth=12,min_samples_leaf=2,class_weight='balanced',random_state=SEED,n_jobs=4)
    }
    results={}; predictions={}; rf=None
    for name,model in estimators.items():
        print(f'Treinando {name}...',flush=True)
        start=time.perf_counter();model.fit(X.loc[train_id],y.loc[train_id]);elapsed=time.perf_counter()-start
        prob=model.predict_proba(X.loc[val_id])[:,1]; pred=model.predict(X.loc[val_id])
        results[name]={**scores(y.loc[val_id],pred,prob),'train_seconds':elapsed,'params':model.get_params()}
        predictions[name]=(prob,pred)
        if name=='Random Forest':
            rf=model
            joblib.dump({'model':model,'features':FEATURES,'threshold':.5,'seed':SEED,'sklearn_version':sklearn.__version__},models/'random_forest.joblib',compress=3)
        elif name=='Arvore de Decisao':
            joblib.dump({'model':model,'features':FEATURES,'threshold':.5,'seed':SEED,'sklearn_version':sklearn.__version__},models/'arvore.joblib',compress=3)
    write_json(out/'metricas_validacao.json',results)
    rows=[]
    for name,v in results.items():
        tn,fp,fn,tp=np.array(v['confusion_matrix']).ravel()
        rows.append(dict(modelo=name,precision=v['precision'],recall=v['recall'],f1=v['f1'],average_precision=v['average_precision'],accuracy=v['accuracy'],TN=int(tn),FP=int(fp),FN=int(fn),TP=int(tp),treino_segundos=v['train_seconds']))
    pd.DataFrame(rows).to_csv(out/'metricas_validacao.csv',index=False)
    f,axes=plt.subplots(1,2,figsize=(8,3.5))
    for a,name in zip(axes,['Arvore de Decisao','Random Forest']):
        cm=np.array(results[name]['confusion_matrix']);a.imshow(np.log1p(cm),cmap='Blues')
        for (i,j),v in np.ndenumerate(cm):a.text(j,i,str(v),ha='center',va='center',color='white' if v>1000 else 'black',fontsize=12)
        a.set_xticks([0,1],['Normal','Fraude']);a.set_yticks([0,1],['Normal','Fraude']);a.set_xlabel('Previsto');a.set_ylabel('Real');a.set_title(name)
    f.suptitle('Matrizes de confusão na validação');f.tight_layout();f.savefig(fig/'04_matrizes.png');plt.close(f)
    f,a=plt.subplots(figsize=(7,3.5))
    for name in ['Arvore de Decisao','Random Forest']:
        p,r,_=precision_recall_curve(y.loc[val_id],predictions[name][0]);a.step(r,p,where='post',label=f'{name} (AP={results[name]["average_precision"]:.3f})')
    a.set_xlabel('Recall');a.set_ylabel('Precisão');a.set_xlim(0,1.01);a.set_ylim(0,1.05);a.legend();a.set_title('Precision–Recall na validação');f.tight_layout();f.savefig(fig/'05_precision_recall.png');plt.close(f)
    pd.Series(rf.feature_importances_,index=FEATURES).sort_values(ascending=False).rename('importancia_impureza').to_csv(out/'importancia_rf.csv')
    prob,pred=predictions['Random Forest']
    evaluated=clean.loc[val_id].copy();evaluated.insert(0,'linha_original',val_id);evaluated['score_rf']=prob;evaluated['previsto_rf']=pred
    evaluated['tipo']=np.select([(evaluated.Class==1)&(pred==0),(evaluated.Class==0)&(pred==1)],['FN','FP'],default='acerto')
    evaluated.to_csv(out/'predicoes_validacao.csv',index=False)
    cases=pd.concat([evaluated[evaluated.tipo=='FN'].head(2),evaluated[evaluated.tipo=='FP'].head(2)])
    cases.to_csv(out/'casos_erros.csv',index=False)
    demo_rows=pd.concat([evaluated[evaluated.Class==0].head(5),evaluated[evaluated.Class==1].head(5)]).sort_values('linha_original')
    demo_rows[FEATURES].to_csv(demo/'transacoes.csv',index=False)
    demo_rows[['linha_original','Class','score_rf','previsto_rf','tipo']].to_csv(demo/'gabarito.csv',index=False)
    loaded=joblib.load(models/'random_forest.joblib')
    assert np.allclose(loaded['model'].predict_proba(demo_rows[FEATURES])[:,1],demo_rows.score_rf)
    env={'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,'scikit-learn':sklearn.__version__,
         'matplotlib':matplotlib.__version__,'joblib':joblib.__version__,'seed':SEED,
         'executed_at_utc':datetime.now(timezone.utc).isoformat(),'evaluation_set':'validacao','test_reserved':True}
    write_json(out/'ambiente.json',env)
    print(pd.DataFrame(rows).to_string(index=False),flush=True)
    print('Concluido. Teste final preservado, sem avaliacao.',flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--data',type=Path,default=ROOT/'data'/'creditcard.csv')
    run(parser.parse_args().data)
