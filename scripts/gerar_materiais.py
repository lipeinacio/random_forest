"""Gera PDFs e fontes editáveis a partir das evidências executadas.

Dependências de autoria: pip install -r requirements-materiais.txt
Execute: python scripts/gerar_materiais.py
"""
from pathlib import Path
import base64
import csv
import html
import json
import re
import shutil
import sys

from PIL import Image as PILImage
import pandas as pd
import qrcode
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image, KeepTogether

sys.path.insert(0,str(Path(__file__).parent))
from conteudo import PEOPLE, SLIDES, QA

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'entrega_final'
DOC=OUT/'documentos'; PRES=OUT/'apresentacao'; MEDIA=OUT/'divulgacao'; PEOPLE_DIR=OUT/'integrantes'; SOURCES=OUT/'fontes'
for directory in [DOC,PRES,MEDIA,PEOPLE_DIR,SOURCES]:directory.mkdir(parents=True,exist_ok=True)
C=json.loads((ROOT/'results'/'final'/'conclusao.json').read_text(encoding='utf-8'))
TEST=C['test']['Random Forest final']
EXP=pd.read_csv(ROOT/'results'/'final'/'experimentos.csv')
INK=colors.HexColor('#183441'); BLUE=colors.HexColor('#145a73'); ORANGE=colors.HexColor('#c76a38'); PAPER=colors.HexColor('#f5f2eb'); LINE=colors.HexColor('#d3d9d8')
URL='https://github.com/lipeinacio/random_forest'
FONTDIR=Path('C:/Windows/Fonts')
if not (FONTDIR/'arial.ttf').exists():
    import os
    FONTDIR=Path(os.environ['ARIAL_FONT_DIR'])
for name,file in [('Arial','arial.ttf'),('Arial-Bold','arialbd.ttf'),('Arial-Italic','ariali.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTDIR/file)))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='Arial-Bold',italic='Arial-Italic',boldItalic='Arial-Bold')
ST={
 'title':ParagraphStyle('title',fontName='Arial-Bold',fontSize=20,leading=24,spaceAfter=17,textColor=colors.black),
 'h':ParagraphStyle('h',fontName='Arial-Bold',fontSize=13,leading=17,spaceBefore=13,spaceAfter=7,textColor=colors.black,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='Arial',fontSize=10.5,leading=15,spaceAfter=9,textColor=colors.black),
 'small':ParagraphStyle('small',fontName='Arial',fontSize=9,leading=12,spaceAfter=6,textColor=colors.black),
 'cell':ParagraphStyle('cell',fontName='Arial',fontSize=9,leading=12,spaceAfter=2),
 'summary':ParagraphStyle('summary',fontName='Arial',fontSize=10,leading=12,spaceAfter=8,alignment=TA_JUSTIFY),
 'summary_center':ParagraphStyle('summary_center',fontName='Arial',fontSize=10,leading=12,spaceAfter=8,alignment=TA_CENTER),
}
ST['time']=ParagraphStyle('time',parent=ST['body'],keepWithNext=True)
ST['guide']=ParagraphStyle('guide',parent=ST['body'],fontSize=10,leading=13,spaceAfter=7)
ST['guide_time']=ParagraphStyle('guide_time',parent=ST['guide'],keepWithNext=True)
ST['guide_h']=ParagraphStyle('guide_h',parent=ST['h'],fontSize=12,leading=16,spaceBefore=10,spaceAfter=6)


def esc(s):return html.escape(str(s))
def p(s,style='body'):
    s=str(s)
    for char in '\u2010\u2011\u2012\u2013\u2014\u2015':s=s.replace(char,'-')
    return Paragraph(s,ST[style])
def pct(v):return f'{100*v:.2f}%'.replace('.',',')
def n(v):return f'{v:.4f}'.replace('.',',')


def footer(c,doc):
    c.setFont('Arial',8);c.setFillColor(colors.HexColor('#53656c'))
    c.drawString(2.1*cm,1.25*cm,'FIB  |  Inteligência Artificial II  |  Grupo 3')
    c.drawRightString(doc.pagesize[0]-2.1*cm,1.25*cm,str(doc.page))


def pdf_doc(filename,story,pagesize=A4):
    doc=SimpleDocTemplate(str(filename),pagesize=pagesize,rightMargin=2.1*cm,leftMargin=2.1*cm,topMargin=2*cm,bottomMargin=2*cm,
                         title=filename.stem.replace('_',' '),author='Grupo 3 - Inteligência Artificial II')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)


def table(rows,widths,header=True):
    data=[[p(esc(x),'cell') for x in row] for row in rows]
    tab=Table(data,colWidths=widths,hAlign='LEFT',repeatRows=1 if header else 0)
    cmds=[('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
          ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]
    if header:
        cmds += [('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e2e9ec')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f5f7f8')])]
    tab.setStyle(TableStyle(cmds));return tab


def markdown_pdf(text,path,compact=False):
    story=[]
    for line in text.split('\n\n'):
        line=line.strip()
        if not line.strip():continue
        if line.startswith('# '):story.append(p(esc(line[2:]),'title'))
        elif line.startswith('## '):story.append(p(esc(line[3:]),'guide_h' if compact else 'h'))
        else:
            style='guide' if compact else 'body'
            if line.startswith('Tempo sugerido:'):style='guide_time' if compact else 'time'
            if line.startswith('Fontes e evidências:'):style='small'
            story.append(p(esc(line).replace('\n','<br/>'),style))
    pdf_doc(path,story)


def draw_paragraph(c,text,x,y,width,font='Arial',size=20,leading=None,color=INK):
    for char in '\u2010\u2011\u2012\u2013\u2014\u2015':text=text.replace(char,'-')
    style=ParagraphStyle('draw',fontName=font,fontSize=size,leading=leading or size*1.25,textColor=color)
    obj=Paragraph(text,style); w,h=obj.wrap(width,2000)
    obj.drawOn(c,x,y-h)
    return y-h


def slides():
    assert abs(sum(s['minutes'] for s in SLIDES)-40)<1e-8
    width,height=960,540
    c=canvas.Canvas(str(PRES/'01_Apresentacao.pdf'),pagesize=(width,height))
    c.setTitle('Caçador de Fraudes com Random Forest');c.setAuthor('Grupo 3 - FIB')
    sections=[]
    for i,s in enumerate(SLIDES,1):
        c.setFillColor(PAPER);c.rect(0,0,width,height,fill=1,stroke=0)
        c.setFillColor(BLUE);c.setFont('Arial-Bold',10);c.drawString(55,502,'RANDOM FOREST  /  CAÇADOR DE FRAUDES')
        top=draw_paragraph(c,esc(s['title']),55,463,850,'Arial-Bold',36,42)
        fig=s.get('figure')
        if fig:
            y=top-22
            for item in s['body']:
                y=draw_paragraph(c,esc(item),55,y,285,size=18,leading=23)-16
            image=ROOT/fig
            iw,ih=PILImage.open(image).size
            maxw,maxh=535,min(330,top-65)
            scale=min(maxw/iw,maxh/ih)
            c.drawImage(str(image),375,70+(maxh-ih*scale)/2,iw*scale,ih*scale,mask='auto')
        else:
            y=top-34
            for item in s['body']:
                y=draw_paragraph(c,esc(item),55,y,835,size=25 if i==1 else 24,leading=31)-23
        if y < 43:raise ValueError(f'Slide {i} ultrapassou o rodapé: {y}')
        c.setFillColor(colors.HexColor('#53656c'));c.setFont('Arial',10)
        c.drawString(55,25,f"FIB · IA II · Grupo 3   |   {s['speaker']}")
        c.drawRightString(905,25,f'{i:02d} / {len(SLIDES):02d}')
        c.showPage()
        asset=''
        if fig:
            b64=base64.b64encode((ROOT/fig).read_bytes()).decode()
            asset=f'<img src="data:image/png;base64,{b64}" alt="{esc(s["title"])}">'
        sections.append(f'<section class="slide {"with-figure" if fig else ""}" aria-label="Slide {i}"><div class="eyebrow">RANDOM FOREST / CAÇADOR DE FRAUDES</div><h1>{esc(s["title"])}</h1><div class="content"><ul>'+''.join(f'<li>{esc(x)}</li>' for x in s['body'])+f'</ul>{asset}</div><footer>FIB · IA II · Grupo 3 · {s["speaker"]}<span>{i:02d}/{len(SLIDES):02d}</span></footer><aside class="notes">{esc(s["notes"])} Fontes: {esc(s["sources"])}</aside></section>')
    c.save()
    viewer='''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Caçador de Fraudes · Apresentação</title><style>
*{box-sizing:border-box}body{margin:0;background:#183441;font-family:Arial,sans-serif;color:#183441}#stage{padding:32px 0}.slide{display:none;background:#f5f2eb;width:min(96vw,1280px);aspect-ratio:16/9;margin:auto;padding:4% 4%;position:relative;overflow:hidden}.slide.active{display:block}.eyebrow{font-size:12px;font-weight:700;letter-spacing:1px;color:#145a73}h1{font-size:clamp(24px,3.5vw,48px);line-height:1.12;margin:25px 0 30px;max-width:95%}ul{list-style:none;padding:0;margin:0}li{font-size:clamp(15px,2.2vw,32px);line-height:1.3;margin:0 0 24px}.content{display:flex;align-items:center;gap:4%}.with-figure ul{width:34%}.with-figure li{font-size:clamp(13px,1.6vw,24px);margin-bottom:15px}.content img{width:62%;max-height:360px;object-fit:contain}footer{position:absolute;bottom:20px;left:4%;right:4%;font-size:12px;color:#53656c}footer span{float:right}.notes{display:none}#controls{padding:8px;text-align:center;color:white;font-size:12px}button{background:transparent;color:white;border:1px solid #8ca2ab;border-radius:3px;padding:8px 15px;margin:3px;cursor:pointer}#speaker{display:none;max-width:1120px;margin:20px auto;color:#183441;background:#fff;padding:25px;font-size:17px;line-height:1.6}@media print{body{background:white}#stage{padding:0}.slide{display:block!important;width:100%;height:100vh;break-after:page;margin:0}#controls,#speaker{display:none!important}}@page{size:landscape;margin:0}
</style></head><body><div id="stage">SECTIONS</div><div id="controls"><button id="prev">Anterior</button><span id="counter"></span><button id="next">Próximo</button><button id="full">Tela cheia</button><button id="show-notes">Roteiro do apresentador</button><p>Setas navegam · F abre tela cheia · N mostra o roteiro · Esc sai da tela cheia</p></div><div id="speaker"></div><script>let i=0;const ss=[...document.querySelectorAll('.slide')];function show(){ss.forEach((s,j)=>s.classList.toggle('active',i===j));document.querySelector('#counter').textContent=(i+1)+' / '+ss.length;document.querySelector('#speaker').textContent=ss[i].querySelector('.notes').textContent}function move(d){i=Math.max(0,Math.min(ss.length-1,i+d));show()}function notes(){const s=document.querySelector('#speaker');s.style.display=s.style.display==='block'?'none':'block'}function full(){if(!document.fullscreenElement)document.documentElement.requestFullscreen();else document.exitFullscreen()}document.querySelector('#prev').onclick=()=>move(-1);document.querySelector('#next').onclick=()=>move(1);document.querySelector('#full').onclick=full;document.querySelector('#show-notes').onclick=notes;document.onkeydown=e=>{if(e.key==='ArrowRight'||e.key===' ')move(1);if(e.key==='ArrowLeft')move(-1);if(e.key.toLowerCase()==='n')notes();if(e.key.toLowerCase()==='f')full()};show();</script></body></html>'''
    (PRES/'02_Apresentacao_editavel.html').write_text(viewer.replace('SECTIONS','\n'.join(sections)),encoding='utf-8')
    (SOURCES/'slides_e_falas.json').write_text(json.dumps(SLIDES,ensure_ascii=False,indent=2),encoding='utf-8')


def summary():
    identification=json.loads((ROOT/'scripts'/'identificacao.json').read_text(encoding='utf-8'))
    professor=identification.get('professor','').strip();email=identification.get('email_apresentador','').strip();email_prof=identification.get('email_professor','').strip()
    authors='Felipe Inácio de Paula; Gabriel Damante Frias; Maicon Manoel Rodrigues dos Santos; André Luiz Jeremias Pereira Junior; Lavinia Zanata Alves'
    if professor:authors+='; '+professor
    story=[p('<b>DETECÇÃO DE TRANSAÇÕES FRAUDULENTAS COM RANDOM FOREST</b>','summary_center'),p(esc(authors),'summary_center')]
    if email:story.append(p('Felipe Inácio de Paula - Ciência da Computação - Faculdades Integradas de Bauru - FIB - '+esc(email),'summary_center'))
    if professor:story.append(p(esc(professor)+' - Professor orientador - Faculdades Integradas de Bauru - FIB'+(' - '+esc(email_prof) if email_prof else ''),'summary_center'))
    sections1=[
    ('Grupo de trabalho','Ciência da Computação.'),
    ('Palavras-chave','Random Forest; detecção de fraudes; desbalanceamento; classificação; avaliação de modelos.'),
    ('Introdução','A detecção de fraudes exige reconhecer uma classe rara sem gerar alertas excessivos sobre transações legítimas. O desbalanceamento e a mudança dos padrões limitam avaliações simplistas (Dal Pozzolo et al., 2014). Random Forest combina árvores construídas com aleatoriedade (Breiman, 2001), utilizando amostras bootstrap relacionadas ao bagging (Breiman, 1996). O estudo compara a técnica com uma árvore isolada e comunica os resultados por meio de um protótipo educacional.'),
    ('Objetivos','Investigar o efeito de pesos de classe, profundidade e remoção de componentes sobre a detecção de fraudes. Comparar Random Forest com uma Árvore de Decisão e disponibilizar uma aplicação para inspeção de scores, alertas e falhas.'),
    ('Relevância do Estudo','Um falso positivo aumenta a carga de revisão; um falso negativo deixa uma fraude passar. O projeto relaciona escolhas metodológicas a esses dois tipos de erro, sem inferir impacto financeiro não medido.'),
    ('Material e Métodos','Utilizou-se Credit Card Fraud Detection, da ULB/Worldline, com 284.807 transações de dois dias de setembro de 2013 e 492 fraudes. Há 30 entradas: Time, Amount e V1 a V28, componentes de PCA fornecidos pelos autores; Class é o alvo e foi excluído das entradas. Removeram-se 1.081 cópias completas adicionais, restando 283.726 registros e 473 fraudes. A divisão estratificada, com semente 42, reservou 60% para treino, 20% para validação e 20% para teste. A exploração detalhada foi restrita ao treino. Valores extremos foram preservados e não se aplicou nova normalização. O baseline é uma árvore com profundidade 12, duas amostras mínimas por folha e pesos balanced. A floresta de referência mantém esses parâmetros, com 100 árvores e max_features=sqrt. A implementação utiliza scikit-learn (Pedregosa et al., 2011).')]
    for h,t in sections1:story.append(p(f'<b>{h}:</b> '+esc(t),'summary'))
    story.append(PageBreak())
    sections2=[
    ('Material e Métodos','Registraram-se previamente três hipóteses: retirar pesos poderia reduzir falsos alertas; limitar a profundidade poderia simplificar o modelo; remover V17, V14 e V12 poderia retirar informação útil. Cada comparação alterou um fator em relação à referência. Selecionou-se a configuração de maior F1 da classe fraude na validação, com limiar 0,50 e AP para desempate. A AP complementa a análise da classe rara (Saito; Rehmsmeier, 2015). O teste foi avaliado após salvar a decisão, sem ajustes posteriores.'),
    ('Resultados e discussões','Na validação, a referência obteve F1 de 0,8466. Sem pesos, os falsos positivos caíram de 15 para 8, os falsos negativos subiram de 14 para 17 e o F1 aumentou para 0,8603. A profundidade 6 elevou recall a 88,30%, mas gerou 138 falsos positivos, com F1 de 0,5270. A remoção dos três componentes manteve recall em 85,11%, elevou F1 a 0,8511 e reduziu AP de 0,8611 para 0,8540, contrariando uma piora uniforme. Selecionou-se a configuração sem pesos. No teste reservado, com 56.746 transações e 95 fraudes, a floresta identificou 68 fraudes, perdeu 27 e gerou 4 falsos positivos: precisão 94,44%, recall 71,58%, F1 0,8144 e AP 0,7867. A árvore identificou 71, perdeu 24 e gerou 256 falsos positivos, com F1 0,3365. Os intervalos de Wilson de 95% foram 86,57–97,82% para precisão e 61,81–79,67% para recall da floresta. Foram examinados quatro erros reais da validação. O protótipo permite entrada manual, CSV e exploração do limiar.'),
    ('Conclusão','A floresta apresentou maior precisão, F1 e AP que a árvore neste protocolo, com recall menor. O resultado favorece uma triagem mais seletiva e não demonstra superioridade em todas as métricas. A base antiga, a divisão aleatória, a ausência de identificação de titulares e os scores sem calibração impedem generalizar para uso operacional. Validação temporal, calibração e custos reais são próximos passos. A aplicação é educacional e mantém a revisão humana.')]
    for h,t in sections2:story.append(p(f'<b>{h}:</b> '+esc(t),'summary'))
    story.append(p('<b>Referências</b>','summary'))
    refs=[
      'BREIMAN, L. Random Forests. Machine Learning, v. 45, p. 5–32, 2001. DOI: 10.1023/A:1010933404324.',
      'BREIMAN, L. Bagging predictors. Machine Learning, v. 24, p. 123–140, 1996. DOI: 10.1007/BF00058655.',
      'DAL POZZOLO, A. et al. Learned lessons in credit card fraud detection from a practitioner perspective. Expert Systems with Applications, v. 41, p. 4915–4928, 2014. DOI: 10.1016/j.eswa.2014.02.026.',
      'PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. JMLR, v. 12, p. 2825–2830, 2011.',
      'SAITO, T.; REHMSMEIER, M. The Precision-Recall Plot Is More Informative than the ROC Plot When Evaluating Binary Classifiers on Imbalanced Datasets. PLOS ONE, v. 10, e0118432, 2015. DOI: 10.1371/journal.pone.0118432.',
      'ULB; WORLDLINE. Credit Card Fraud Detection. Kaggle. Disponível em: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud. Acesso em: 13 nov. 2026.'
    ]
    for r in refs:story.append(p(esc(r),'summary'))
    def header(c,doc):
        w,h=A4;c.setFont('Arial',10);c.setFillColor(colors.black)
        logo=ROOT/'scripts'/'assets'/'logo_fib.png'
        if logo.exists():c.drawImage(str(logo),2.5*cm,h-2.95*cm,width=2.86*cm,height=1.77*cm,mask='auto')
        for i,line in enumerate(['XXI Jornada Científica','Faculdades Integradas de Bauru - FIB','ISSN 2358-6044','2026']):c.drawCentredString(w/2+1.2*cm,h-1.45*cm-i*12,line)
        c.setStrokeColor(colors.black);c.setLineWidth(.5);c.line(2.5*cm,h-3.2*cm,w-2.5*cm,h-3.2*cm)
    doc=SimpleDocTemplate(str(DOC/'01_Resumo_expandido.pdf'),pagesize=A4,leftMargin=2.5*cm,rightMargin=2.5*cm,topMargin=3.9*cm,bottomMargin=2.5*cm,title='Detecção de transações fraudulentas com Random Forest',author=authors)
    doc.build(story,onFirstPage=header,onLaterPages=header)
    txt='# Detecção de transações fraudulentas com Random Forest\n\n'+authors+'\n\n'+'\n\n'.join('## '+h+'\n\n'+t for h,t in sections1+sections2)+'\n\n## Referências\n\n'+'\n\n'.join(refs)
    (SOURCES/'resumo_expandido.md').write_text(txt,encoding='utf-8')


def model_card():
    fields=[
      ('Solução e objetivo','Caçador de Fraudes. Apoio educacional à triagem de transações para revisão humana.'),
      ('Técnica','RandomForestClassifier, scikit-learn 1.9.1. 100 árvores, max_depth=12, min_samples_leaf=2, max_features=sqrt, bootstrap=True, class_weight=None, seed=42. Limiar oficial 0,50.'),
      ('Dados e preparação','ULB/Worldline, dois dias de setembro de 2013. 284.807 transações e 492 fraudes na origem. Após remover 1.081 cópias completas: 283.726 registros e 473 fraudes. Divisão estratificada 60/20/20; treino apenas no primeiro conjunto. Sem normalização nova ou remoção automática de extremos.'),
      ('Entradas e saída','Time, Amount e V1 a V28 numéricos e finitos. Class nunca é entrada. A saída contém score sem calibração e sugestão de revisão. V1 a V28 já são PCA e não possuem semântica comercial disponível.'),
      ('Seleção e métrica principal','Maior F1 da fraude na validação, com AP como desempate e limiar 0,50. Configuração sem pesos: F1 0,8603 na validação. Decisão gravada antes de avaliar o teste.'),
      ('Resultado final no teste','56.746 transações, 95 fraudes. TP=68, FN=27, FP=4, TN=56.647. Precisão 94,44%; recall 71,58%; F1 0,8144; AP 0,7867. Wilson 95%: precisão 86,57–97,82%; recall 61,81–79,67%.'),
      ('Baseline e troca observada','Árvore isolada: TP=71, FN=24, FP=256, F1 0,3365 no mesmo teste. A floresta reduz falsos alertas e melhora F1, porém tem recall menor.'),
      ('Limitações e riscos','Base antiga e curta; divisão aleatória; poucos positivos; sem independência conhecida por titular; escopo da PCA original desconhecido; sem calibração ou validação temporal. Não foi estimado custo monetário. Alertas podem gerar revisão indevida, e fraudes podem passar.'),
      ('Quando não utilizar','Não usar para bloquear compras, decidir sobre pessoas ou operar sem avaliação atual, supervisão e validação apropriada. Não fornecer compras brutas sem a mesma transformação de dados. Cenários editados no protótipo podem não representar transações reais.'),
      ('Reprodução e responsáveis','Grupo 3, IA II, FIB. Código e evidências: '+URL+'. Script src/finalizar.py; plano, decisão e métricas em results/final/. Modelos salvos em models/final/.')]
    story=[p('Model Card do Caçador de Fraudes','title')]
    for h,t in fields:story.append(p('<b>'+esc(h)+'.</b> '+esc(t),'body'))
    pdf_doc(DOC/'02_Model_Card.pdf',story)
    (SOURCES/'model_card.md').write_text('# Model Card do Caçador de Fraudes\n\n'+'\n\n'.join('## '+h+'\n\n'+t for h,t in fields),encoding='utf-8')


def experiments():
    rows=[['Exp.','Hipótese e alteração','Resultado na validação','Interpretação']]
    records=[
      ['E1','Retirar pesos pode reduzir FP, com possível perda de recall. Alteração: balanced para None.','Precisão 90,59%; recall 81,91%; F1 0,8603; AP 0,8748. FP=8; FN=17. Referência: FP=15; FN=14.','Hipótese compatível com a observação. Configuração mais seletiva. Maior F1 entre as quatro configurações, escolhida antes do teste.'],
      ['E2','Profundidade 6 pode simplificar a árvore e reduzir sobreajuste, mas perder padrões complexos. Alteração: max_depth 12 para 6.','Precisão 37,56%; recall 88,30%; F1 0,5270; AP 0,8164. FP=138; FN=11.','Recall cresceu, mas precisão e F1 caíram. Não houve melhora geral. A causa em termos de sobreajuste não foi isolada por curva de aprendizagem.'],
      ['E3','Retirar componentes destacados pode prejudicar a predição. Alteração: remover V17, V14 e V12, selecionados pela EDA do treino.','Precisão 85,11%; recall 85,11%; F1 0,8511; AP 0,8540. FP=14; FN=14.','Efeito misto: AP caiu, F1 subiu levemente e recall ficou igual. Não sustenta piora uniforme nem inutilidade dos componentes.']]
    rows+=records
    story=[p('Ficha de experimentos controlados','title'),p('André Luiz Jeremias Pereira Junior · Grupo 3 · IA II'),
      p('Comparações com a referência: 100 árvores, profundidade 12, duas amostras mínimas por folha, pesos balanced e max_features sqrt. Semente 42, mesmos dados e limiar 0,50. Um fator alterado por experimento. Hipóteses registradas antes de executar.'),
      table(rows,[1.1*cm,7*cm,7.3*cm,9.1*cm]),Spacer(1,14),
      p('Seleção e avaliação final','h'),p('Critério pré-definido: maior F1 na validação, desempate por AP. Selecionada a configuração sem pesos. No teste reservado: precisão 94,44%, recall 71,58%, F1 0,8144 e AP 0,7867. A árvore teve F1 0,3365 e recall 74,74%. A floresta reduziu falsos alertas de 256 para 4, mas perdeu três fraudes adicionais.'),
      p('Evidências: results/final/plano_pre_execucao.json, decisao_antes_do_teste.json, experimentos.csv, teste.json e conclusao.json. Limites: uma semente, uma divisão e ausência de validação temporal. O teste não foi usado para ajustar parâmetros.','small')]
    pdf_doc(DOC/'03_Ficha_experimentos.pdf',story,landscape(A4))
    EXP.to_csv(SOURCES/'ficha_experimentos.csv',index=False)


def guides():
    order=['Lavinia','Maicon','Gabriel','André','Felipe']
    schedule=[];elapsed=0
    for name in order:
        indices=[i for i,s in enumerate(SLIDES,1) if s['speaker']==name]
        duration=sum(s['minutes'] for s in SLIDES if s['speaker']==name)
        schedule.append((name,indices[0],indices[-1],elapsed,elapsed+duration));elapsed+=duration
    alltext='# Roteiro da apresentação do Caçador de Fraudes\n\nNúcleo de aproximadamente 40 minutos, com cinco integrantes. Os tempos incluem leitura dos gráficos, interação e demonstração. As falas são um roteiro de estudo. O grupo precisa ensaiar, explicar com suas palavras e conferir o tempo real. Os slides 24 e 25 são apêndices.\n\n'
    alltext+='## Distribuição e transições\n\n'+'\n'.join(f'{name}: slides {first} a {last}, de {start:g} a {end:g} minutos. Material: {PEOPLE[name][1]}.' for name,first,last,start,end in schedule)+'\n\n'
    for name,first,last,start,end in schedule:
        title=f'Guia de apresentação de {name}'
        text=f'# {title}\n\n{PEOPLE[name][0]}. Responsabilidade de material: {PEOPLE[name][1]}. Tema de fala: {PEOPLE[name][2]}. Slides {first} a {last}, aproximadamente {end-start:g} minutos.\n\n'
        text+='## O que conferir antes do ensaio\n\nAbra os slides e as evidências citadas. Leia sua parte, confira os números e ensaie a passagem para o próximo integrante. Estude também o objetivo geral, a separação dos dados, os três experimentos e os limites. A divisão distribui a condução da fala, não o conhecimento obrigatório.\n\n'
        for i,s in enumerate(SLIDES,1):
            if s['speaker']!=name:continue
            block=f"## Slide {i} {s['title']}\n\nTempo sugerido: {s['minutes']:g} min.\n\n{s['notes']}\n\nFontes e evidências: {s['sources']}\n\n"
            text+=block;alltext+=block
        text+='## Perguntas que você deve dominar\n\n'
        chosen={'Lavinia':[0,1,12,18],'Maicon':[5,6,8,9],'Gabriel':[0,1,2,10],'André':[2,3,4,11,14,16],'Felipe':[3,4,13,15,17,18]}[name]
        for index in chosen:
            q,a=QA[index];text+=f'## {q}\n\n{a}\n\n'
        slug={'André':'Andre','Lavinia':'Lavinia','Maicon':'Maicon','Gabriel':'Gabriel','Felipe':'Felipe'}[name]
        (PEOPLE_DIR/f'{slug}_roteiro.md').write_text(text.rstrip()+'\n',encoding='utf-8')
        markdown_pdf(text,PEOPLE_DIR/f'{slug}_roteiro.pdf',compact=True)
    alltext+='## Perguntas e respostas para o grupo\n\n'
    for q,a in QA:alltext+=f'## {q}\n\n{a}\n\n'
    alltext+='## Plano B da demonstração\n\nInstale as dependências antes de ir à sala. A inferência usa o modelo já salvo e não exige internet nem a base completa. Abra o servidor antes da fala. Mantenha o vídeo, o PDF dos slides e as capturas disponíveis localmente. Se mostrar a gravação, identifique-a como gravação. Para uma pergunta sem evidência, explique o limite e como faria o experimento.\n\n'
    (PRES/'03_Roteiro_completo.md').write_text(alltext.rstrip()+'\n',encoding='utf-8')
    markdown_pdf(alltext,PRES/'03_Roteiro_completo.pdf')


def folder():
    qr=qrcode.make(URL);qr.save(MEDIA/'qr_projeto.png')
    w,h=landscape(A4);c=canvas.Canvas(str(MEDIA/'01_Folder_dobravel.pdf'),pagesize=(w,h))
    c.setTitle('Folder Caçador de Fraudes');c.setAuthor('Grupo 3 - FIB')
    c.setFillColor(PAPER);c.rect(0,0,w,h,fill=1,stroke=0)
    panel=w/3;pad=22
    for x in [panel,2*panel]:c.setStrokeColor(LINE);c.setDash(3,4);c.line(x,18,x,h-18)
    c.setDash()
    draw_paragraph(c,'IA PARA REVISÃO DE TRANSAÇÕES',pad,h-30,panel-2*pad,'Arial-Bold',10,color=BLUE)
    y=draw_paragraph(c,'Caçador<br/>de Fraudes',pad,h-70,panel-2*pad,'Arial-Bold',30,35)
    y=draw_paragraph(c,'Como reconhecer fraudes sem gerar alertas demais?',pad,y-28,panel-2*pad,'Arial-Bold',17,22)-20
    y=draw_paragraph(c,'Uma floresta reúne 100 árvores que analisam padrões diferentes. A média dos scores orienta quais transações merecem revisão humana.',pad,y,panel-2*pad,size=11,leading=16)
    draw_paragraph(c,'Dados públicos ULB/Worldline.<br/>Projeto educacional de IA II.<br/>FIB · Grupo 3 · 2026',pad,75,panel-2*pad,size=9,leading=13)
    x=panel+pad
    draw_paragraph(c,'O QUE DESCOBRIMOS',x,h-30,panel-2*pad,'Arial-Bold',10,color=BLUE)
    y=draw_paragraph(c,'4 falsos alertas',x,h-75,panel-2*pad,'Arial-Bold',27,32)-18
    y=draw_paragraph(c,'No teste reservado, a floresta encontrou 68 das 95 fraudes. Deixou 27 passarem. A árvore isolada encontrou 71, mas gerou 256 falsos alertas.',x,y,panel-2*pad,size=11,leading=16)-18
    y=draw_paragraph(c,'Precisão 94,44%<br/>Recall 71,58%<br/>F1 0,8144',x,y,panel-2*pad,'Arial-Bold',14,21)-18
    draw_paragraph(c,'A melhora em precisão veio com recall menor. Um alerta é um convite à revisão, sem comprovação de fraude.',x,y,panel-2*pad,size=10,leading=15)
    screenshot=ROOT/'docs'/'img'/'prototipo.png'
    if screenshot.exists():c.drawImage(str(screenshot),x,35,width=panel-2*pad,height=150,preserveAspectRatio=True,anchor='c',mask='auto')
    x=2*panel+pad
    draw_paragraph(c,'EXPLORE O PROJETO',x,h-30,panel-2*pad,'Arial-Bold',10,color=BLUE)
    y=draw_paragraph(c,'Veja o código<br/>e os materiais',x,h-75,panel-2*pad,'Arial-Bold',24,29)
    c.drawImage(str(MEDIA/'qr_projeto.png'),x+40,y-145,130,130,mask='auto')
    y-=164
    y=draw_paragraph(c,'O QR leva ao repositório. Para testar a aplicação, siga as instruções de execução local no README.',x,y,panel-2*pad,size=10,leading=14)-18
    y=draw_paragraph(c,'Uma base antiga de apenas dois dias não demonstra desempenho em fraudes atuais. Os componentes são anonimizados e os scores não foram calibrados.',x,y,panel-2*pad,size=10,leading=14)-18
    draw_paragraph(c,'Lavinia Zanata Alves<br/>Maicon Manoel Rodrigues dos Santos<br/>Gabriel Damante Frias<br/>André Luiz Jeremias Pereira Junior<br/>Felipe Inácio de Paula',x,y,panel-2*pad,size=8.8,leading=13)
    c.showPage();c.save()
    (SOURCES/'folder_texto.md').write_text('# Folder dobrável\n\nFormato A4 paisagem, uma face, três painéis. Dobre nas duas linhas tracejadas.\n\nCaçador de Fraudes. Como reconhecer fraudes sem gerar alertas demais? Uma floresta reúne 100 árvores. No teste, encontrou 68 de 95 fraudes, deixou 27 passarem e gerou 4 falsos alertas. A árvore encontrou 71 e gerou 256 falsos alertas. Precisão 94,44%, recall 71,58%, F1 0,8144. O resultado depende dos dados de dois dias de 2013. QR para o repositório e instruções locais. Grupo 3, IA II, FIB.',encoding='utf-8')


def instagram():
    cards=[
      ('Uma IA consegue encontrar fraudes?','Nosso grupo investigou como um Random Forest pode ajudar na revisão de transações.','Caçador de Fraudes · Grupo 3 · IA II · FIB'),
      ('99,83% de acurácia pode enganar','Na validação, responder “normal” para tudo acerta 99,83% das transações. E encontra zero fraudes.','Por isso, analisamos precisão, recall e F1 da fraude.'),
      ('Os dados vêm antes do modelo','A base ULB/Worldline contém 284.807 transações e 492 fraudes de dois dias de 2013. Removemos cópias completas e separamos treino, validação e teste.','Time, Amount e 28 componentes anonimizados de PCA.'),
      ('Uma floresta de 100 árvores','Cada árvore aprende com uma amostra diferente do treino e considera subconjuntos de variáveis. A média dos scores é comparada com um limiar.','A analogia é uma equipe de revisores com perspectivas diferentes.'),
      ('Menos alertas falsos, com uma troca','No teste reservado, a floresta gerou 4 falsos alertas e encontrou 68 de 95 fraudes. A árvore gerou 256 falsos alertas e encontrou 71.','Precisão 94,44% · Recall 71,58% · F1 0,8144'),
      ('Explore e questione o resultado','O protótipo permite analisar exemplos, alterar entradas e observar o efeito do limiar. Uma base antiga não garante desempenho futuro.','QR para código e instruções locais. Score sem calibração. Revisão humana.')]
    c=canvas.Canvas(str(MEDIA/'02_Carrossel_Instagram.pdf'),pagesize=(540,675))
    c.setTitle('Carrossel Caçador de Fraudes');c.setAuthor('Grupo 3 - FIB')
    for i,(title,body,foot) in enumerate(cards,1):
        c.setFillColor(PAPER);c.rect(0,0,540,675,fill=1,stroke=0)
        draw_paragraph(c,'CAÇADOR DE FRAUDES  /  RANDOM FOREST',40,630,460,'Arial-Bold',10,color=BLUE)
        y=draw_paragraph(c,esc(title),40,568,460,'Arial-Bold',35,41)-33
        y=draw_paragraph(c,esc(body),40,y,460,size=21,leading=30)-28
        if i==6:
            c.drawImage(str(MEDIA/'qr_projeto.png'),40,83,112,112,mask='auto')
            draw_paragraph(c,esc(foot),175,190,325,size=13,leading=19)
        else:draw_paragraph(c,esc(foot),40,min(y,155),460,'Arial-Bold',14,20,color=BLUE)
        c.setFont('Arial',10);c.setFillColor(INK);c.drawString(40,30,'FIB · Inteligência Artificial II · Grupo 3');c.drawRightString(500,30,f'{i}/6');c.showPage()
    c.save()
    caption='''Uma IA pode ajudar a encontrar fraudes sem gerar alertas demais? Investigamos essa pergunta com Random Forest e uma árvore de decisão.

No teste reservado, com 56.746 transações e 95 fraudes, a floresta identificou 68 fraudes, deixou 27 passarem e gerou 4 falsos alertas. A árvore identificou 71 e gerou 256 falsos alertas. A floresta teve precisão de 94,44%, recall de 71,58% e F1 de 0,8144.

A configuração foi escolhida pela validação. O teste não foi usado para ajustar parâmetros. A base é de dois dias de 2013, as variáveis são parcialmente anonimizadas e os scores não foram calibrados. O protótipo é educacional e mantém revisão humana.

Conheça o código, os experimentos e as instruções para executar a aplicação: https://github.com/lipeinacio/random_forest

Grupo 3 · Inteligência Artificial II · FIB
Lavinia Zanata Alves; Maicon Manoel Rodrigues dos Santos; Gabriel Damante Frias; André Luiz Jeremias Pereira Junior; Felipe Inácio de Paula.

#InteligenciaArtificial #RandomForest #CienciaDeDados #FIB #AprendizadoDeMaquina
'''
    (MEDIA/'03_Legenda_Instagram.txt').write_text(caption,encoding='utf-8')
    (SOURCES/'carrossel_texto.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf-8')


def checklist():
    text='''# Checklist de entrega e ensaio

O pacote reúne código, evidências e materiais. As verificações humanas abaixo permanecem como ações reais do grupo. Prazo da disciplina: 17/11/2026 às 17h. Apresentação do Grupo 3: 17/11/2026, primeiro tema do dia.

## Materiais produzidos

Protótipo local com entrada manual, CSV, inspeção de scores e limiar. Baseline e modelo principal. Três experimentos controlados executados. Teste reservado avaliado após a escolha. Quatro erros da validação documentados. Importância por permutação e intervalos de confiança. Slides em PDF e HTML. Roteiro completo e cinco guias individuais. Resumo de duas páginas. Model Card de uma página. Ficha de experimentos. Folder de uma página com dobra. Seis imagens para Instagram e legenda. Vídeo demonstrativo com narração sintética. Código e tabelas reproduzíveis.

## Conferências que o grupo precisa realizar

[ ] Completar ou confirmar orientador e e-mail do apresentador em scripts/identificacao.json e regenerar o resumo. Esses dados não foram inventados.
[ ] Conferir as normas e a identificação do resumo antes de enviar à disciplina ou à Jornada.
[ ] Cada integrante ler, revisar e conseguir explicar sua parte e o projeto completo.
[ ] Realizar um ensaio cronometrado de aproximadamente 40 minutos com transições.
[ ] Executar a aplicação no computador e no navegador que serão usados em sala.
[ ] Testar instalação em outra máquina. A validação automatizada nesta entrega não equivale a esse teste humano.
[ ] Abrir os arquivos, conferir o vídeo com áudio e testar o QR no celular.
[ ] Confirmar acesso do professor ao repositório e escolher os arquivos exigidos no portal.
[ ] Fazer o envio pelo canal indicado pelo professor. A preparação deste pacote não realiza a submissão.
[ ] Registrar participação, reflexão e verificação reais no Diário de IA.

## Preparação da demonstração

Instale as dependências antes da apresentação. Para inferência, não é necessário baixar a base completa. Inicie python src/app.py e abra http://127.0.0.1:8501. Mantenha demo/demo_final.csv e o gabarito separados. Analise normal, fraude, falso negativo e falso positivo. Convide a plateia a escolher uma alteração ou fornecer CSV no esquema esperado. Explique entradas rejeitadas sem improvisar variáveis comerciais para V1 a V28.

## Plano B

A aplicação funciona localmente após instalação. Leve o PDF dos slides, o vídeo, as capturas e os dados de demonstração. Se o servidor falhar, use a gravação identificando que é gravação. Se uma pergunta exceder a evidência, diga o que não foi medido e proponha um experimento.

## Responsabilidades finais

Lavinia revisa resumo e Instagram. Maicon revisa vídeo e Model Card. Gabriel revisa folder e explicação conceitual. André revisa ficha, métricas e hipóteses. Felipe revisa instalação, repositório, demonstração e organização do envio. Essas são responsabilidades de revisão e apresentação; não descrevem participação passada não verificada.
'''
    (OUT/'00_COMECE_AQUI.md').write_text(text,encoding='utf-8')
    markdown_pdf(text,DOC/'04_Checklist_entrega_e_ensaio.pdf',compact=True)


def diary():
    base=(ROOT/'docs'/'diario_ia.md').read_text(encoding='utf-8')
    addition='''

## Registro 5

Data: 13/11/2026. Etapas: conclusão dos experimentos, protótipo e comunicação. Ferramenta: Codex, OpenAI. Modelo/versão visível ao usuário nesta interação: não informado no registro.

Prompts relevantes enviados pelo usuário: “consegue me trazer tudo pronto?” e “use esse repositorio como exemplo para melhorar qualquer metrica necessaria para a conclusao do nosso seminario!” Referência indicada: https://github.com/ViniciusSilveiraCampos/football-pca-map.

Apoio da IA: leitura do repositório e das exigências; uso do projeto de PCA como referência de organização, sem copiar seus dados ou resultados; implementação de três experimentos com hipóteses previamente gravadas; seleção na validação; avaliação final; protótipo; elaboração dos materiais e roteiros.

Validação técnica: hash da base oficial conferido; reprodução da configuração original; isolamento de registros entre conjuntos; testes automatizados de inferência, rejeição de Class e entradas inválidas; conferência das matrizes e métricas. Resultados e ambiente em results/final/. A seleção foi gravada antes do teste. O recall menor no teste foi preservado na comunicação.

Uso pelo grupo nesta etapa: materiais disponibilizados para leitura, revisão, ensaio e eventual adoção. Não houve declaração de revisão individual ou teste em outro computador nesta interação. Esses fatos só devem ser acrescentados após ocorrerem.

Reflexão dos integrantes e verificação em outra máquina: pendentes de registro real pelo grupo. Não foram simulados depoimentos, participação ou aprovação.
'''
    if '## Registro 5' not in base:
        base+=addition
        (ROOT/'docs'/'diario_ia.md').write_text(base,encoding='utf-8')
    (DOC/'05_Diario_de_IA.md').write_text(base,encoding='utf-8')
    # Blocos de código são mantidos como texto legível no PDF.
    markdown_pdf(base.replace('```text','').replace('```',''),DOC/'05_Diario_de_IA.pdf')


def video_script():
    scenes=[
      ('01_problema', 'Como identificar fraudes sem gerar alertas demais? Nosso projeto usa uma floresta de cem árvores para apoiar a revisão de transações. O resultado é um score, e a comparação com um limiar indica se uma entrada merece análise.'),
      ('02_normal', 'Este é o protótipo funcionando localmente. Selecionamos um exemplo normal da validação e pedimos a análise. A tela mostra o score da primeira transação e a contribuição de cada árvore. O score da floresta é a média desses valores.'),
      ('03_fraude', 'Agora escolhemos uma fraude conhecida da validação. Com limiar de zero vírgula cinquenta, o sistema pode gerar um alerta de revisão. Também podemos editar Time, Amount e os componentes anonimizados. Uma combinação editada não tem gabarito e pode não representar uma compra real.'),
      ('04_falha', 'O modelo também falha. Este exemplo é uma fraude que recebeu score muito baixo e passou sem alerta. Outro caso normal recebeu score alto e gerou um falso positivo. Reduzir o limiar tende a aumentar alertas, mas não garante encontrar todas as fraudes.'),
      ('05_metricas', 'Três experimentos compararam pesos, profundidade e remoção de componentes. A configuração foi escolhida pelo F um na validação, antes do teste. No teste reservado, a floresta encontrou sessenta e oito das noventa e cinco fraudes, perdeu vinte e sete e gerou quatro falsos alertas. A árvore encontrou setenta e uma fraudes e gerou duzentos e cinquenta e seis falsos alertas. A floresta teve precisão de noventa e quatro vírgula quarenta e quatro por cento, recall de setenta e um vírgula cinquenta e oito por cento e F um de zero vírgula oito um quatro quatro.'),
      ('06_limites', 'O ganho em precisão veio com recall menor que o da árvore. A base contém apenas dois dias de dois mil e treze, e os scores não foram calibrados. O protótipo é educacional e mantém revisão humana. O repositório reúne código, resultados e instruções para executar. Grupo três, Inteligência Artificial dois, FIB.')]
    (SOURCES/'narracao_video.json').write_text(json.dumps(scenes,ensure_ascii=False,indent=2),encoding='utf-8')
    (MEDIA/'04_Roteiro_video.md').write_text('# Vídeo demonstrativo\n\nNarração sintética em português, sem imitar a voz de um integrante. Capturas do protótipo executado localmente.\n\n'+'\n\n'.join('## '+a+'\n\n'+b for a,b in scenes),encoding='utf-8')


if __name__=='__main__':
    slides();summary();model_card();experiments();guides();folder();instagram();checklist();diary();video_script()
    print('Materiais gerados em',OUT)
