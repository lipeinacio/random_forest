'use strict';
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const decimal = (value, digits = 2) => Number(value).toLocaleString('pt-BR', { minimumFractionDigits: digits, maximumFractionDigits: digits });
const pct = value => decimal(value * 100) + '%';
const indexText = value => decimal(value * 100, value > 0 && value < .001 ? 3 : 1);
let info, lastResult, selectedIndex = 0, activeKind = 'normal', mode = 'example', modified = false;
let controller, busy = false, revision = 0;
const emptyResult = $('#result').cloneNode(true);
const labels = { analisar: 'Análise de transações', como: 'Como funciona', evidencias: 'Resultados do modelo' };

function node(tag, className, text) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
}
function showError(message) {
  $('#error').textContent = message;
  $('#error').hidden = !message;
}
function setBusy(value) {
  busy = value;
  $('#predict').disabled = value || !info;
  $('#predict').innerHTML = value ? (mode === 'csv' ? 'Analisando o arquivo…' : 'Analisando a transação…') : mode === 'csv' ? '<span aria-hidden="true">✧</span> Analisar arquivo <span aria-hidden="true">→</span>' : '<span aria-hidden="true">✧</span> Analisar transação <span aria-hidden="true">→</span>';
  $('.output-area').setAttribute('aria-busy', String(value));
  $('#loading-status').hidden = !value;
  $('#loading-status').textContent = value ? 'As árvores estão avaliando os dados…' : '';
}
function invalidate() {
  revision++;
  if (controller) controller.abort();
  controller = null;
  setBusy(false);
  lastResult = null;
  $('#result').replaceChildren(...[...emptyResult.childNodes].map(n => n.cloneNode(true)));
  $('#result-details').hidden = true;
  $('#tree-section').open = false;
  $('#result-badge').textContent = 'Aguardando análise';
  $('#result-badge').classList.remove('ready');
  $('#step-analyze').classList.remove('done');
  $('#step-result').classList.remove('done');
  showError('');
}
function showTab(name) {
  if (!labels[name]) return;
  $$('.tab').forEach(tab => { tab.hidden = tab.id !== name; tab.classList.toggle('active', tab.id === name); });
  $$('.nav-item').forEach(button => {
    const active = button.dataset.tab === name;
    button.classList.toggle('active', active);
    if (active) button.setAttribute('aria-current', 'page'); else button.removeAttribute('aria-current');
  });
  $('#page-label').textContent = labels[name];
  window.scrollTo({ top: 0, behavior: 'instant' });
}
$$('[data-tab]').forEach(button => button.addEventListener('click', () => showTab(button.dataset.tab)));
$$('[data-go]').forEach(button => button.addEventListener('click', () => showTab(button.dataset.go)));

function matchingExamples(kind = activeKind) {
  return info.examples.map((example, i) => ({ example, i })).filter(({ example }) => kind === 'erros' ? ['FN', 'FP'].includes(example.kind) : example.kind === kind);
}
function syncScenario() {
  const kind = info.examples[selectedIndex].kind;
  activeKind = ['FN', 'FP'].includes(kind) ? 'erros' : kind;
  $$('.scenario').forEach(button => {
    const active = button.dataset.kind === activeKind;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  $('#next-example').disabled = matchingExamples().length < 2;
}
function updatePreview() {
  const amount = $('#f-Amount').value;
  $('#transaction-amount').textContent = amount !== '' && Number.isFinite(Number(amount)) ? decimal(amount) : '—';
  $('#example-label').textContent = modified ? 'Seu cenário exploratório' : 'Transação de exemplo ' + String(selectedIndex + 1).padStart(2, '0');
  $('#sample-tag').textContent = modified ? 'DADOS EDITADOS' : 'DADO REAL';
  $('#example-context').textContent = modified ? 'Sem gabarito para os dados alterados' : 'Valor na unidade da base original';
}
function selectExample(index) {
  selectedIndex = index;
  const example = info.examples[index];
  info.features.forEach(feature => { $('#f-' + feature).value = example.row[feature]; });
  $('#preset').value = String(index);
  modified = false;
  syncScenario();
  updatePreview();
  invalidate();
}
$$('.scenario').forEach(button => button.addEventListener('click', () => {
  if (!info) return;
  const next = matchingExamples(button.dataset.kind)[0];
  if (next) selectExample(next.i);
}));
$('#next-example').addEventListener('click', () => {
  const matches = matchingExamples();
  const at = matches.findIndex(item => item.i === selectedIndex);
  selectExample(matches[(at + 1) % matches.length].i);
});
$('#preset').addEventListener('change', () => selectExample(Number($('#preset').value)));
$('#restore-example').addEventListener('click', () => selectExample(selectedIndex));
$('#try-errors').addEventListener('click', () => {
  showTab('analisar');
  setMode('example');
  if (info) selectExample(matchingExamples('erros')[0].i);
  $('#predict').focus({ preventScroll: true });
});
function setMode(nextMode) {
  mode = nextMode;
  $$('.input-tabs button').forEach(button => {
    const active = button.dataset.mode === mode;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  $('#example-input').hidden = mode !== 'example';
  $('#csv-input').hidden = mode !== 'csv';
  $('#edit-details').hidden = mode !== 'example';
  invalidate();
}
$$('[data-mode]').forEach(button => button.addEventListener('click', () => setMode(button.dataset.mode)));
$('#csv').addEventListener('change', () => {
  const file = $('#csv').files[0];
  $('#file-name').textContent = file ? file.name + ' · ' + decimal(file.size / 1024, 0) + ' KB' : 'Nenhum arquivo selecionado';
  invalidate();
});
function updateThreshold() {
  const cut = Number($('#threshold').value);
  $('#threshold-value').textContent = String(cut);
  $('#sensitivity-summary').textContent = cut === 50 ? 'Padrão' : 'Corte ' + cut;
  invalidate();
}
$('#threshold').addEventListener('input', updateThreshold);
$('#reset-threshold').addEventListener('click', () => { $('#threshold').value = '50'; updateThreshold(); });

function renderTruth(first, isBatch) {
  const example = info.examples[selectedIndex];
  const card = node('div', 'truth-card');
  card.append(node('small', '', isBatch ? 'SOBRE ESTE ARQUIVO' : 'CONFERINDO COM A REALIDADE'));
  if (isBatch || modified || example.actual === null) {
    card.classList.add('neutral');
    card.append(node('strong', '', 'Este resultado não tem gabarito associado.'), node('p', '', isBatch ? 'O arquivo foi analisado sem consultar rótulos de fraude. Os alertas indicam quais linhas merecem revisão.' : 'Os dados foram editados ou não têm rótulo conhecido. Não é possível dizer se o modelo acertou neste cenário.'));
  } else {
    const correct = Number(first.classe_prevista) === example.actual;
    if (!correct) card.classList.add('mismatch');
    card.append(node('strong', '', correct ? 'O modelo acertou este exemplo.' : 'Aqui, o modelo errou.'));
    const text = example.actual ? (correct ? 'O gabarito confirma uma fraude, e a floresta pediu revisão.' : 'O gabarito confirma uma fraude, mas a floresta não gerou alerta. É uma fraude não detectada (falso negativo).') : (correct ? 'O gabarito confirma uma compra legítima, e a floresta não gerou alerta.' : 'O gabarito confirma uma compra legítima, mas a floresta pediu revisão. É um alarme falso (falso positivo).');
    card.append(node('p', '', text));
  }
  return card;
}
function renderBatch(data) {
  const area = $('#batch-results');
  area.replaceChildren();
  area.hidden = mode !== 'csv';
  if (mode !== 'csv') return;
  area.append(node('h3', '', 'O arquivo em um olhar'));
  const summary = node('div', 'batch-summary');
  [[data.count, 'analisadas'], [data.alerts, 'para revisar'], [data.count - data.alerts, 'sem alerta']].forEach(([value, label]) => {
    const item = node('div'); item.append(node('strong', '', value.toLocaleString('pt-BR')), node('small', '', label)); summary.append(item);
  });
  area.append(summary, node('p', 'batch-caption', 'O indicador acima mostra a primeira linha. Abaixo, ' + (data.count > 25 ? 'as primeiras 25 linhas. Baixe o CSV para ver todas.' : 'o resultado de cada linha.')));
  const scroll = node('div', 'batch-table');
  const table = node('table');
  const thead = table.createTHead().insertRow();
  ['Linha', 'Índice / 100', 'Sugestão'].forEach(label => { const th = node('th', '', label); th.scope = 'col'; thead.append(th); });
  const tbody = table.createTBody();
  data.rows.slice(0, 25).forEach((row, i) => {
    const tr = tbody.insertRow();
    [i + 1, indexText(row.score_fraude), row.classe_prevista ? 'Revisar' : 'Sem alerta'].forEach(value => { tr.insertCell().textContent = value; });
  });
  scroll.append(table); area.append(scroll);
}
function renderResult(data) {
  lastResult = data;
  const first = data.rows[0], alert = Boolean(first.classe_prevista), isBatch = mode === 'csv';
  const content = node('div', 'result-content' + (alert ? ' is-alert' : ''));
  const symbol = node('span', 'result-symbol', alert ? '!' : '✓'); symbol.setAttribute('aria-hidden', 'true');
  content.append(symbol, node('h3', 'decision', alert ? 'Vale uma segunda análise.' : 'Sem alerta nesta análise.'));
  content.append(node('p', 'result-explanation', alert ? 'A floresta encontrou sinais que justificam uma revisão humana. Isso não confirma uma fraude.' : 'O índice ficou abaixo do ponto de corte. Isso não garante que a transação seja legítima.'));
  const gauge = node('div', 'gauge');
  gauge.style.setProperty('--score', String(Math.min(100, Math.max(0, first.score_fraude * 100))));
  if (alert) gauge.style.setProperty('--gauge-color', '#c29243');
  const score = node('strong', 'score', indexText(first.score_fraude)); score.append(node('small', '', ' / 100'));
  gauge.append(score, node('span', '', 'ÍNDICE DO MODELO'));
  content.append(gauge, node('p', 'score-explainer', 'Quanto maior o índice, mais sinais para revisão.'));
  const comparison = node('div', 'cut-comparison');
  comparison.append(node('span', '', 'Ponto de corte: ' + decimal(data.threshold * 100, 0)), node('strong', '', alert ? 'Índice ≥ corte → revisar' : 'Índice < corte → sem alerta'));
  content.append(comparison, renderTruth(first, isBatch));
  const next = node('p', 'result-next');
  next.append(node('strong', '', 'Experimente agora: '), document.createTextNode(activeKind === 'erros' ? 'mude o ponto de corte e analise novamente. Nem todo erro é resolvido com um corte diferente.' : 'escolha outro caso ou desafie o modelo para ver onde ele pode errar.'));
  if (!isBatch) content.append(next);
  $('#result').replaceChildren(content);
  $('#result-badge').textContent = isBatch ? data.count + ' transações analisadas' : 'Análise concluída';
  $('#result-badge').classList.add('ready');
  $('#trees').replaceChildren();
  data.tree_scores_first.forEach((value, i) => {
    const cell = node('i');
    cell.style.backgroundColor = `hsl(105 26% ${94 - value * 64}%)`;
    cell.title = 'Árvore ' + (i + 1) + ': score ' + decimal(value, 4);
    cell.setAttribute('aria-hidden', 'true');
    $('#trees').append(cell);
  });
  $('#trees').setAttribute('aria-label', data.tree_scores_first.length + ' árvores. Média dos scores: ' + decimal(first.score_fraude, 4));
  $('#tree-caption').textContent = 'Score médio ' + decimal(first.score_fraude, 4) + ' × 100 = índice ' + indexText(first.score_fraude) + '.' + (isBatch ? ' Visualização referente à primeira linha do arquivo.' : '');
  $('#result-details').hidden = false;
  renderBatch(data);
  $('#step-analyze').classList.add('done');
  $('#step-result').classList.add('done');
  showError('');
  if (window.innerWidth <= 760) $('.output-area').scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
}
async function send(options) {
  const currentRevision = revision;
  controller = new AbortController();
  const requestController = controller;
  showError(''); setBusy(true);
  try {
    const response = await fetch('/api/predict', { ...options, signal: requestController.signal });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Não foi possível analisar os dados.');
    if (currentRevision === revision) renderResult(data);
  } catch (error) {
    if (error.name !== 'AbortError' && currentRevision === revision) showError(error instanceof TypeError ? 'Não foi possível conectar. Confira se o servidor está aberto e tente novamente.' : error.message);
  } finally {
    if (currentRevision === revision) { controller = null; setBusy(false); }
  }
}
$('#predict').addEventListener('click', () => {
  if (!info || busy) return;
  const threshold = Number($('#threshold').value) / 100;
  if (mode === 'csv') {
    const file = $('#csv').files[0];
    if (!file) { showError('Escolha um arquivo CSV primeiro. Você também pode baixar o exemplo acima.'); $('#csv').focus(); return; }
    if (file.size > 3 * 1024 * 1024) { showError('O arquivo excede 3 MB. Separe suas transações em arquivos menores.'); return; }
    const body = new FormData(); body.append('csv', file); body.append('threshold', threshold);
    send({ method: 'POST', body });
    return;
  }
  const row = {};
  for (const feature of info.features) {
    const el = $('#f-' + feature);
    if (!el.checkValidity() || el.value.trim() === '' || !Number.isFinite(Number(el.value))) {
      showError('Confira o campo ' + feature + ': use um número válido' + (['Time', 'Amount'].includes(feature) ? ', igual ou maior que zero.' : '.'));
      $('#edit-details').open = true;
      const parent = el.closest('details'); if (parent) parent.open = true;
      el.focus(); return;
    }
    row[feature] = Number(el.value);
  }
  send({ method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ rows: [row], threshold }) });
});
$('#download-results').addEventListener('click', () => {
  if (!lastResult) return;
  const cols = ['linha', 'score_fraude', 'classe_prevista', 'decisao'];
  const csv = cols.join(',') + '\n' + lastResult.rows.map((row, i) => [i + 1, row.score_fraude, row.classe_prevista, row.decisao].join(',')).join('\n');
  const url = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
  const link = node('a'); link.href = url; link.download = 'analise_transacoes.csv'; document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
function metricRows(selector, records) {
  const body = $(selector + ' tbody'); body.replaceChildren();
  const names = { sem_pesos: 'Sem pesos (selecionada)', referencia: 'Referência', profundidade_6: 'Profundidade 6', sem_top3: 'Sem V17, V14 e V12', 'Arvore de Decisao': 'Árvore de decisão', 'Random Forest final': 'Random Forest final', 'Sempre normal': 'Sempre normal' };
  Object.entries(records).forEach(([name, record]) => {
    const row = body.insertRow();
    [names[name] || name, pct(record.precision), pct(record.recall), decimal(record.f1, 4), decimal(record.average_precision, 4), record.FP ?? record.confusion_matrix?.[0][1], record.FN ?? record.confusion_matrix?.[1][0]].forEach(value => { row.insertCell().textContent = value; });
  });
}
function renderEvidence() {
  const c = info.conclusion;
  if (!c) return;
  const rf = c.test['Random Forest final'];
  $('#found-frauds').textContent = rf.confusion_matrix[1][1] + ' de 95';
  $('#false-alerts').textContent = String(rf.confusion_matrix[0][1]);
  $('#precision-value').textContent = pct(rf.precision);
  $('#split-summary').textContent = Object.entries(c.splits).map(([name, split]) => `${name}: ${split.rows.toLocaleString('pt-BR')} transações, ${split.frauds} fraudes`).join(' · ');
  metricRows('#experiments', Object.fromEntries(info.experiments.map(record => [record.configuracao, record])));
  metricRows('#test-metrics', c.test);
  $('#selected').textContent = 'Configuração selecionada: sem pesos de classe. Critério: maior F1 na validação, com desempate por AP.';
  Object.entries(c.test).forEach(([name, record]) => {
    const row = $('#simple-comparison tbody').insertRow();
    [name === 'Arvore de Decisao' ? 'Árvore de decisão' : name, record.confusion_matrix[1][1], record.confusion_matrix[1][0], record.confusion_matrix[0][1]].forEach(value => { row.insertCell().textContent = value; });
  });
  c.errors_validation.forEach(record => {
    const row = $('#errors tbody').insertRow();
    [record.linha_original, record.tipo === 'FN' ? 'Fraude não detectada' : 'Alarme falso', decimal(record.Amount), decimal(record.score_rf, 4), record.Class ? 'Fraude' : 'Legítima', record.previsto_rf ? 'Revisar' : 'Sem alerta'].forEach(value => { row.insertCell().textContent = value; });
  });
}
(async function init() {
  try {
    const response = await fetch('/api/info');
    if (!response.ok) throw new Error('Não foi possível carregar os exemplos. Recarregue a página para tentar novamente.');
    const data = await response.json();
    if (!data.examples?.length) throw new Error('Nenhum exemplo disponível. Confira os arquivos na pasta demo.');
    info = data;
    info.features.forEach(feature => {
      const wrap = node('div'), label = node('label', '', feature === 'Time' ? 'Tempo desde o início da base (s)' : feature === 'Amount' ? 'Valor da transação' : feature);
      const input = node('input'); input.id = 'f-' + feature; input.type = 'number'; input.step = 'any'; input.required = true;
      label.htmlFor = input.id;
      if (['Time', 'Amount'].includes(feature)) input.min = '0';
      input.addEventListener('input', () => {
        modified = info.features.some(name => { const value = $('#f-' + name).value; return value.trim() === '' || Number(value) !== Number(info.examples[selectedIndex].row[name]); });
        updatePreview(); invalidate();
      });
      wrap.append(label, input); $(['Time', 'Amount'].includes(feature) ? '#primary-fields' : '#other-fields').append(wrap);
    });
    info.examples.forEach((example, i) => { const option = node('option', '', example.name); option.value = String(i); $('#preset').append(option); });
    const initial = matchingExamples('normal')[0]; selectExample(initial ? initial.i : 0);
    renderEvidence(); setBusy(false);
  } catch (error) { showError(error.message || 'Falha ao carregar a aplicação. Recarregue a página.'); }
})();
